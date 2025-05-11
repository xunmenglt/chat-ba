# -*- coding:UTF-8 -*-
# @Time : 2024/3/16 14:36
# @Author : 寻梦
# @File : openbaController
# @Project : ChatBA-Server
import asyncio
import logging
import json
from typing import List,Union,Optional,AsyncIterable,Awaitable
from fastapi import APIRouter,Body
from sse_starlette.sse import EventSourceResponse
from configs import TEMPERATURE,MAX_TOKENS
from langchain_core.prompt_values import PromptValue
from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.prompts import PromptTemplate
from langchain_core.runnables import chain
from langchain.chains import LLMChain
from server.db.mapper.conversation_mapper import filter_message
from server.services.chat.chat_utils import ChatType,add_message_service,process_history,get_prompt_template
from server.callback_handler.conversation_callback_handler import ConversationCallBackHandler
from configs import logger,log_verbose
from pool.model_pool import model_pool

# 定义搜索工具
from langchain_community.utilities import SerpAPIWrapper




openba_app=APIRouter()

@chain
def get_info_in_chain(info):
    print("=======================================")
    print(info)
    print("=======================================\n")
    return info

@chain
def prompt_value_to_string(promptvalue:PromptValue):
    print("******************************************")
    print(promptvalue.to_string())
    print("******************************************\n")
    return promptvalue.to_string()

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


def get_history_from_db(conversation_id:str,historys:List=[],history_len=-1):
    template="Human: {} </s> Assistant: {} </s> "
    input_text=""
    if historys is None and len(historys)>0:
        for history in historys:
            input_text+=template.format(history["input"],history["output"])
    elif conversation_id and history_len>0:
        historys=filter_message(conversation_id=conversation_id,limit = history_len)
        historys.reverse()
        for history in historys:
            input_text+=template.format(history["input"],history["output"])
    return input_text



@openba_app.post("/opeba",description="openba对话接口")
async def openba(query:str=Body(...,description="用户输入",examples=["苏州今天天气怎么样？"]),
                   conversation_id:str=Body(...,description="对话框ID"),
                   history_len:int=Body(-1,description="获取历史对话消息的数量"),
                   history:Union[int,List]=Body([],
                                                description="历史对话，设为一个整数可以从数据库中读取历史信息",
                                                examples=[[
                                                             {"input": "我们来玩成语接龙，我先来，生龙活虎",
                                                              "output": "虎头虎脑"}]]
                                                ),
                   stream:bool=Body(False,description="流式输出"),
                   model_name:str=Body("OpenBA-Chat-3B",description="LLM 模型名称"),
                   temperature:float=Body(TEMPERATURE,description="LLM 采样温度",ge=0.0,le=2.0),
                   max_tokens:Optional[int]=Body(MAX_TOKENS,description="限制LLM生成的tokens数量"),
                   prompt_name:str=Body("OpenBA",description="使用的prompt模板名称")):

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

        model,_=model_pool.load_model(model_name=model_name,
                            temperature=temperature,
                            max_tokens=max_tokens,
                            callbacks=callbacks)

        prompt_template=get_prompt_template(ChatType.DIALOGUE,prompt_name)

        prompt=PromptTemplate.from_template(template=prompt_template)

        history_str=get_history_from_db(conversation_id=conversation_id,historys=history,history_len=history_len)
        model.invoke(prompt.invoke({"history":history_str,"input":query}).to_string())
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