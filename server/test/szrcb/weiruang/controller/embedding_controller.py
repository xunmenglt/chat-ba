from fastapi import APIRouter,Body
import json
import asyncio
import logging
from langchain.embeddings.huggingface import HuggingFaceBgeEmbeddings
from fastapi import APIRouter,Body
from typing import List,Dict,Union

import pydantic
from pydantic import BaseModel
from typing import Any

class BaseResponse(BaseModel):
    code: int = pydantic.Field(200, description="API status code")
    msg: str = pydantic.Field("success", description="API status message")
    data: Any = pydantic.Field(None, description="API data")
    object: Any=pydantic.Field(None,description="object")
    model:str=pydantic.Field(None),
    usage:Any=pydantic.Field(None)
    
    
    class Config:
        schema_extra = {
            "example": {
                "code": 200,
                "msg": "success",
            }
        }

embedding_app=APIRouter(tags=["嵌入式模型管理控制层"],prefix="/embeddings")





MODEL_PATH="/opt/data/private/liuteng/model/BAAI/bge-large-zh-v1.5"
embedding_model=HuggingFaceBgeEmbeddings(model_name=MODEL_PATH,
                                            model_kwargs={'device': "cuda:2"}
                                            )

@embedding_app.post("",description="向量化接口")
async def embedding(
                   model:str=Body("bge-large-zh-v1.5",description="模型名称",examples=["chatglm3-6b","OpenBA-3B"]),
                   inputs:Union[str,list]=Body(...,description="用户输入",example=["天空为什么是蓝色的？"])
                   encoding_format=Body("float")):
    vectors=[]
    if isinstance(inputs,str):
        inputs=[inputs]
    vectors=[{
        "object":"embedding",
        "embedding":embedding_model.embed_query(p),"index":i
    } for i,p in enumerate(inputs)]
    
    return BaseResponse(code=200,msg="success",object="list",model=model,usage={
        "prompt_tokens":8,
        "total_tokens":8},data=vectors)

