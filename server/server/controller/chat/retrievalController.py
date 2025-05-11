# -*- coding:UTF-8 -*-
# @Time : 2024/3/9 14:16
# @Author : 寻梦
# @File : retrievalController
# @Project : langchain-ChatBA
import json
import asyncio
import logging
from sse_starlette.sse import EventSourceResponse
from typing import List,Dict,Optional,AsyncIterable,Awaitable
from fastapi import APIRouter,Body,Request
from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain_core.documents import Document
from configs import VECTOR_SEARCH_TOP_K,LLM_MODELS,TEMPERATURE,MAX_TOKENS,SCORE_THRESHOLD,logger,log_verbose

from server.services.knowledge_base.base import KBServiceFactory
from server.controller.utils import BaseResponse
from server.db.mapper import question_answer_mapper
from server.utils import get_file_path
from server.services.chat.chat_utils import search_docs,get_prompt_template,ChatType
from server.db.mapper.knowledge_file_mapper import get_file_detail
from langchain_core.runnables import chain
from langchain_core.prompt_values import (
    PromptValue
)
from pool.model_pool import model_pool

@chain
def log_text(data:PromptValue):
    print("===============================")
    print(data.to_string())
    print("===============================")


retrieval_app=APIRouter()

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

@retrieval_app.post("/retrieval",description="知识库检索api")
async def retrieval(query: str = Body(..., description="用户输入", examples=["你好"]),
                              factory_name: str = Body(..., description="知识库名称", examples=["samples"]),
                              top_k: int = Body(VECTOR_SEARCH_TOP_K, description="匹配向量数"),
                              top_p: float=Body(0.9, description="top_p"),
                              score_threshold:float=Body(SCORE_THRESHOLD,description="相似度匹配不能低于的分数"),
                              stream: bool = Body(False, description="流式输出"),
                              model_name: str = Body(LLM_MODELS[0], description="LLM 模型名称。"),
                              temperature: float = Body(TEMPERATURE, description="LLM 采样温度", ge=0.0, le=1.0),
                              max_tokens: Optional[int] = Body(
                                  MAX_TOKENS,
                                  description="限制LLM生成Token数量，默认None代表模型最大值"
                              ),
                              qa_score_threshold: Optional[int] = Body(
                                  0.9,
                                  description="问答对阈值"
                              ),
                              prompt_name: str = Body(
                                  "default",
                                  description="使用的prompt模板名称"
                              )
                              ):
    kb = KBServiceFactory.get_service_by_name(factory_name)
    if kb is None:
        return BaseResponse(code=404, msg=f"未找到知识库 {factory_name}")
    async def knowledge_base_chat_iterator(
            query: str,
            top_k: int,
            model_name: str = model_name,
            prompt_name: str = prompt_name,
    ) -> AsyncIterable[str]:
        nonlocal max_tokens
        callback = AsyncIteratorCallbackHandler()
        if isinstance(max_tokens, int) and max_tokens <= 0:
            max_tokens = None
        try:
            model,_ = model_pool.load_model(
                model_name=model_name,
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens,
                callbacks=[callback],
            )
        except Exception:
            yield json.dumps({"answer": "模型获取异常，请更换模型"}, ensure_ascii=False)
            return

        try:
            docs:List[Document] = search_docs(query=query,
                           kb_name=factory_name,
                           top_k=top_k,score_threshold=score_threshold)
        except Exception as e:
            print(e)
            yield json.dumps({"answer": "知识库检索异常，请更换或重试"}, ensure_ascii=False)
            return
        
        # 文件文档
        file_docs=[]
        # 问答对文档
        qa_docs=[]

        # 区分文档内容
        for doc in docs:
            if doc.metadata.get("file_ext") and doc.metadata.get("file_ext").__contains__("json"):
                qa_docs.append(doc)
            else:
                file_docs.append(doc)
        # 拼接文件文档内容
        context = "\n".join([doc.page_content for doc in file_docs])
        # 需要返回给用户的文档内容，里面的文档内容保证唯一性：
        ## 文件文档，去除文件名相同的
        ## 问答对文档，去除问题内容相同的
        source_documents = []

        file_name_set=set()

        qa_flag_set=set()

        # 保证文件名唯一性，只返回文件名
        for file_doc in file_docs:
            file_name=file_doc.metadata.get("file_name")
            if file_name not in file_name_set:
                # 更具meta获取文件id
                fn=file_doc.metadata.get("factory_name")
                fileinfo=get_file_detail(kb_name=fn,filename=file_name)
                file_doc.metadata["id"]=fileinfo["id"]
                source_documents.append(file_doc.metadata)
                file_name_set.add(file_name)
        # 保证问题对中的问题唯一性,并获取最大相似问答的问题和答案
        max_qa_score=0
        best_qa_answer=None
        for qa_doc in qa_docs:
            file_name=qa_doc.metadata.get("file_name")
            sort=qa_doc.metadata.get("sort")
            fn=qa_doc.metadata.get("factory_name")
            qa_score=qa_doc.metadata.get("score")
            qa_flag=file_name+fn+f"_{str(sort)}"
            if qa_flag not in qa_flag_set:
                qa_flag_set.add(qa_flag)
                # 获取文件路径
                qa_file_path=get_file_path(
                    factory_name=fn,
                    doc_name=file_name
                )
                qaList=question_answer_mapper.list_from_db(file_path=qa_file_path,sort=sort)
                qa_answer=""
                if qaList and len(qaList)>0:
                    for qa in qaList:
                        qa_doc.metadata["question"]=qa["question"]
                        qa_answer=qa["answer"]
                source_documents.append(qa_doc.metadata)
                if max_qa_score<qa_score and qa_score>qa_score_threshold:
                    max_qa_score=qa_score
                    best_qa_answer=qa_answer
        
        ## 判断是否可以直接使用检索效果
        if(best_qa_answer):
            yield json.dumps({"answer": best_qa_answer}, ensure_ascii=False)
        else:
            if len(file_docs) == 0:  # 如果没有找到相关文档，使用empty模板
                prompt_template = get_prompt_template(ChatType.RETRIEVAL, "empty")
            else:
                prompt_template = get_prompt_template(ChatType.RETRIEVAL, prompt_name)
            prompt = ChatPromptTemplate.from_messages(
                [("user",prompt_template)],
                template_format="mustache"
            )
            chain = LLMChain(prompt=prompt, llm=model)
            task = asyncio.create_task(wrap_done(
                chain.acall({"context": context, "question": query}),
                callback.done),
            )
            if stream:
                async for token in callback.aiter():
                    # Use server-sent-events to stream the response
                    yield json.dumps({"answer": token}, ensure_ascii=False)
            else:
                answer = ""
                async for token in callback.aiter():
                    answer += token
                yield json.dumps({"answer": answer},
                                ensure_ascii=False)
            await task
        yield json.dumps({"docs": source_documents},ensure_ascii=False)

    return EventSourceResponse(knowledge_base_chat_iterator(query, top_k,model_name,prompt_name))