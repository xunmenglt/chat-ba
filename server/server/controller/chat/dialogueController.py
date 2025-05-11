# -*- coding:UTF-8 -*-
# @Time : 2024/3/9 14:16
# @Author : 寻梦
# @File : dialogueController
# @Project : langchain-ChatBA
import asyncio
import logging
import json
import os
from typing import List,Union,Optional,AsyncIterable,Awaitable
from fastapi import APIRouter,Body
from sse_starlette.sse import EventSourceResponse
from configs import LLM_MODELS,TEMPERATURE,MAX_TOKENS
from langchain_core.messages import SystemMessage
from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from server.services.chat.chat_utils import ChatType,add_message_service,process_history,process_history_messages,get_prompt_template
from server.callback_handler.conversation_callback_handler import ConversationCallBackHandler
from configs import logger,log_verbose,PROJECT_DIR
from pool.model_pool import model_pool

dialogue_app=APIRouter()


async def wrap_done(fn: Awaitable, event: asyncio.Event):
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


@dialogue_app.post("/dialogue",description="用户对话接口")
async def dialogue(query:str=Body(...,description="用户输入",examples=["血热的表现是什么？"]),
                   conversation_id:str=Body(...,description="对话框ID"),
                   history_len:int=Body(-1,description="获取历史对话消息的数量"),
                   history:Union[int,List]=Body([],
                                                description="历史对话，设为一个整数可以从数据库中读取历史信息",
                                                examples=[[
                                                             {"input": "我们来玩成语接龙，我先来，生龙活虎",
                                                              "output": "虎头虎脑"}]]
                                                ),
                   stream:bool=Body(False,description="流式输出"),
                   model_name:str=Body(LLM_MODELS[0],description="LLM 模型名称"),
                   temperature:float=Body(TEMPERATURE,description="LLM 采样温度",ge=0.0,le=2.0),
                   top_p:float=Body(0.9,description="top_p"),
                   max_tokens:Optional[int]=Body(MAX_TOKENS,description="限制LLM生成的tokens数量"),
                   prompt_name:str=Body("default",description="使用的prompt模板名称")):
    async def chat_iterator()->AsyncIterable[str]:
        nonlocal history, max_tokens,query
        callback=AsyncIteratorCallbackHandler()
        callbacks=[callback]

        # 保存用户消息
        message_id=add_message_service(chat_type=ChatType.DIALOGUE,query=query,conversation_id=conversation_id)

        # llm处理完毕保存消息回调
        conversation_callback=ConversationCallBackHandler(conversation_id=conversation_id,
                                                          message_id=message_id,
                                                          chat_type=ChatType.DIALOGUE,
                                                          query=query)
        callbacks.append(conversation_callback)
        if isinstance(max_tokens,int) and max_tokens<=0:
            max_tokens=MAX_TOKENS

        # todo 添加模型创建方法
        model,_=model_pool.load_model(model_name=model_name,
                            streaming=stream,
                            temperature=temperature,
                            top_p=top_p,
                            max_tokens=max_tokens,
                            callbacks=callbacks)

        prompt_template=get_prompt_template(ChatType.DIALOGUE,prompt_name)
        history_str=process_history(historys=history,history_len=history_len,conversation_id=conversation_id)
        history_messages=process_history_messages(historys=history,history_len=history_len,conversation_id=conversation_id,prompt_template=prompt_template)
        if "moon" in model_name.lower() or "qwen" in model_name.lower():
            echarts_system_prompt = os.path.join(PROJECT_DIR,"configs/echarts_system_prompt.txt")
            with open(echarts_system_prompt,'r',encoding="utf-8") as fp:
                content=fp.read()
                history_messages.insert(0,content)
        prompt=ChatPromptTemplate.from_messages(
            history_messages,
            template_format="mustache"
        )
        
        chain= LLMChain(prompt=prompt,llm=model)
        
        # Begin a task that runs in the background.
        task = asyncio.create_task(wrap_done(
            chain.acall({"history":history_str,"input":query}),
            callback.done),
        )

        if stream:
            async for token in callback.aiter():
                # Use server-sent-events to stream the response
                yield json.dumps(
                    {"answer": token, "message_id": message_id},
                    ensure_ascii=False)
        else:
            answer = ""
            async for token in callback.aiter():
                answer += token
            yield json.dumps(
                    {"answer": answer, "message_id": message_id},
                    ensure_ascii=False)

        await task

    return EventSourceResponse(chat_iterator())