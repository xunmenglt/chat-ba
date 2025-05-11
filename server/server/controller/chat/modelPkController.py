# -*- coding:UTF-8 -*-
# @Time : 2024/8/18 14:16
# @Author : 寻梦
# @File : modelPkController
# @Project : langchain-ChatBA
import asyncio
import time
import logging
import json
import math
from typing import List,Dict,Union,Optional,AsyncIterable,Awaitable
from fastapi import APIRouter,Body
from sse_starlette.sse import EventSourceResponse
from configs import LLM_MODELS,TEMPERATURE,MAX_TOKENS
from langchain_core.callbacks import AsyncCallbackHandler
from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from server.controller.utils import BaseResponse
from configs import logger,log_verbose
from pool.model_pool import model_pool
from server.tool.online_judge import eval_muti_qa_quality


pk_app=APIRouter(prefix="/pk")


async def wrap_done(fn: Awaitable, event: asyncio.Event,model_name:str):
    """Wrap an awaitable with a event to signal when it's done or an exception is raised."""
    try:
        await fn
    except Exception as e:
        logging.exception(e)
        msg = f"Caught exception: {e}"
        logger.error(f'{e.__class__.__name__}: {msg}',
                     exc_info=e if log_verbose else None)
    finally:
        # Signal the aiter to stop.
        event.set()
        if model_name:
            model_pool.change_model_status(model_name=model_name,is_used=False)
        
        
class CaculateTokenNumsAsyncCallbackHandler(AsyncCallbackHandler):
    usage={}
    async def on_llm_new_token(self, token: str, **kwargs) -> None:
        if kwargs.get("usage"):
            self.usage=kwargs.get("usage")
    async def getUsage(self):
        return self.usage
    


@pk_app.post("/dialogue",description="用户对话接口")
async def dialogue(history_len:int=Body(-1,description="获取历史对话消息的数量"),
                   messages:Union[int,List]=Body([],
                                                description="历史对话，设为一个整数可以从数据库中读取历史信息",
                                                examples=[[{"role":"user","content":"天空为什么是蓝色的？"},{"role":"assistant","content":"这是由于海洋的反射"}]]
                                                ),
                   stream:bool=Body(False,description="流式输出"),
                   model_name:str=Body(LLM_MODELS[0],description="LLM 模型名称"),
                   temperature:float=Body(TEMPERATURE,description="LLM 采样温度",ge=0.0,le=2.0),
                   top_p:float=Body(0.9,description="top_p"),
                   max_tokens:Optional[int]=Body(MAX_TOKENS,description="限制LLM生成的tokens数量")):
    async def chat_iterator()->AsyncIterable[str]:
        nonlocal messages, max_tokens,history_len,model_name
        callback=AsyncIteratorCallbackHandler()
        caculateTokenNumsHandler = CaculateTokenNumsAsyncCallbackHandler()
        callbacks=[callback,caculateTokenNumsHandler]
        
        if isinstance(max_tokens,int) and max_tokens<=0:
            max_tokens=MAX_TOKENS

        # todo 添加模型创建方法
        model,model_name=model_pool.load_model(model_name=model_name,
                            streaming=stream,
                            temperature=temperature,
                            top_p=top_p,
                            max_tokens=max_tokens,
                            callbacks=callbacks)

        format_messages=[]
        if history_len>0:
            messages=messages[-history_len:]
        for message in messages:
            format_messages.append((message["role"],message["content"]))
        prompt=ChatPromptTemplate.from_messages(
            format_messages
        )

        chain= LLMChain(prompt=prompt,llm=model)
        
        # Begin a task that runs in the background.
        task = asyncio.create_task(wrap_done(
            chain.acall({}),
            callback.done,
            model_name)
        )
        startTime=time.time()*1000
        if stream:
            print("\n")
            async for token in callback.aiter():
                print(token,end="")
                endTime=time.time()*1000
                yield json.dumps(
                    {"answer": token,"startTime":startTime,"endTime":endTime},
                    ensure_ascii=False)
            print("\n")
        else:
            answer = ""
            async for token in callback.aiter():
                answer += token
            yield json.dumps(
                    {"answer": answer,"startTime":startTime},
                    ensure_ascii=False)
        usage= await caculateTokenNumsHandler.getUsage()
        endTime=time.time()*1000
        yield json.dumps(
                {"startTime":startTime,"endTime":endTime,"usage":usage},
                ensure_ascii=False)

        await task
    response=EventSourceResponse(chat_iterator())
    return response

# class ModelBox:
#     id:str=""
#     model_name:str= ""
#     history_len:int=3
#     stream:bool=True
#     temperature:float= 0.95
#     max_tokens:int=512
#     top_p:float=0.9,
#     messages:List[Dict]=[]
    

@pk_app.post("/report",description="pk报告生成")
def dialogue(model_box_list:List[Dict]=Body(...,description="模型结果列表"),
            tig:int=Body(0,description="附加"))->BaseResponse:
    if (not model_box_list) or len(model_box_list)<=0:
         return BaseResponse(code=200,data=[])
    result=[]
    print(model_box_list)
    for model_box in model_box_list:
        model_box=dict(model_box)
        # 模型名称
        model_name=model_box.get('model_name')
        # 温度
        temperature=model_box.get('temperature')
        # top_p
        top_p=model_box.get('top_p')
        # 总输入token
        total_input_tokens=0
        # 总输出token
        total_output_tokens=0
        # 总耗时
        total_time=0
        # 平均token输出率
        avg_token_output_speed=0
        # （GPT-4）评分
        score=-1
        startTime=-1
        endTime=0
        messages=[]
        if model_box.get('messages') and len(model_box.get('messages'))>0:
            messages=model_box.get('messages')
            for message in messages:
                if message.get('usage'):
                    usage=dict(message.get('usage'))
                    total_input_tokens+=usage.get('prompt_tokens') if usage.get('prompt_tokens') else 0
                    total_output_tokens+=usage.get('completion_tokens') if usage.get('completion_tokens') else 0
                    total_time+=math.floor(message.get('endTime')-message.get('startTime'))
            score=eval_muti_qa_quality(messages=messages)
        total_time=total_time/1000
        avg_token_output_speed=math.ceil(total_output_tokens/total_time)
        result.append(dict(
            model_name=model_name,
            temperature=temperature,
            top_p=top_p,
            total_input_tokens=total_input_tokens,
            total_output_tokens=total_output_tokens,
            total_time=total_time,
            avg_token_output_speed=avg_token_output_speed,
            score=score
        ))
    return BaseResponse(code=200,data=result)
    
    