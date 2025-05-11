import json
import asyncio
import logging
from fastapi import APIRouter,Body
from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from datetime import datetime
from sse_starlette.sse import EventSourceResponse
from typing import List,Dict,Optional,AsyncIterable,Awaitable
from model.chatglm import ChatGLM3_LLM

model_app=APIRouter(tags=["大语模型管理控制层"],prefix="/model")



MODEL_PATH="/opt/data/private/liuteng/model/THUDM/glm-4-9b-chat"
HISTORY_LEN=3
chatmodel=ChatGLM3_LLM(model_path=MODEL_PATH,history_len=3)
# chatmodel=None
async def wrap_done(fn: Awaitable, event: asyncio.Event):
    """Wrap an awaitable with a event to signal when it's done or an exception is raised."""
    try:
        await fn
    except Exception as e:
        logging.exception(e)
        msg = f"Caught exception: {e}"
        print(msg)
    finally:
        # Signal the aiter to stop.
        event.set()
     

@model_app.post("/chat",description="聊天接口")
async def model_chat(
                   model:str=Body("glm4-chat",description="模型名称",examples=["chatglm3-6b","OpenBA-3B"]),
                   messages:List[Dict]=Body(...,description="用户输入",examples=["血热的表现是什么?"]),
                   temperature:float=Body(0.95,description="LLM 采样温度",ge=0.0,le=2.0),
                   top_p:float=Body(0.7,description="最低匹配词的概率",ge=0.0,le=1.0),
                   stream:bool=Body(False,description="流式输出"),
                   max_new_tokens:Optional[int]=Body(512,description="输出最大token数")):
    async def chat_iterator()->AsyncIterable[str]:
            nonlocal max_new_tokens
            callback=AsyncIteratorCallbackHandler()
            callbacks=[callback]
            task = asyncio.create_task(wrap_done(
                chatmodel.ainvoke(
                    input=messages,
                    messages=messages,
                    top_p=top_p,
                    temperature=temperature,
                    max_new_tokens=max_new_tokens,
                    config={
                        "callbacks":callbacks
                    }),
                callback.done),
            )
            answer = ""
            if stream:
                async for token in callback.aiter():
                    # Use server-sent-events to stream the response
                    answer += token
                    yield json.dumps(
                        {"answer": token,},
                        ensure_ascii=False)
            else:
                async for token in callback.aiter():
                    answer += token
                yield json.dumps(
                    {"answer": answer},
                    ensure_ascii=False)

            await task
            
    
    return EventSourceResponse(chat_iterator())

