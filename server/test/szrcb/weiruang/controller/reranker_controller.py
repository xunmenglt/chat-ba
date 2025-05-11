from fastapi import APIRouter,Body
import json
import torch
import uuid
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from typing import List
import pydantic
from pydantic import BaseModel
from typing import Any


class BaseResponse(BaseModel):
    code: int = pydantic.Field(200, description="API status code")
    msg: str = pydantic.Field("success", description="API status message")
    data: Any = pydantic.Field(None, description="API data")
    id:str=pydantic.Field(None)
    results:Any=pydantic.Field(None)
    meta:Any=pydantic.Field(None)
    
    
    class Config:
        schema_extra = {
            "example": {
                "code": 200,
                "msg": "success",
            }
        }


reranker_app=APIRouter(tags=["评分模型管理控制层"],prefix="/rerank")

MODEL_PATH="/opt/data/private/liuteng/model/BAAI/bge-reranker-large"


reranker_tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)
reranker_model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH, trust_remote_code=True)
reranker_model.eval()


@reranker_app.post("/do",description="评分接口")
async def reranker(
                   model:str=Body("bge-reranker-large",description="模型名称",examples=["chatglm3-6b","OpenBA-3B"]),
                   query:str=Body(...,description="参考文本",examples=["What is the capital of the United States?"]),
                   top_n:int=Body(3,description="返回最大相似条目数量"),
                   documents:List[str]=Body(...,description="候选文本")):
    pairs=[[query,candidate] for candidate in documents]
    inputs = reranker_tokenizer(pairs, padding=True, truncation=True, return_tensors='pt', max_length=512)
    scores = reranker_model(**inputs, return_dict=True).logits.view(-1, ).float()
    scores =scores.tolist()
    indexs=[i for i  in range(len(scores))]
    results=[{"index":index,"relevance_score":score,"document":{"text":document}} for document,score,index in  zip(documents,scores,indexs)]
    results=sorted(results,key=lambda res:res["relevance_score"],reverse=True)
    results=results[:min(len(results,top_n))]
    meta={
        "api_version": {
        "version": "string",
        "is_deprecated": True,
        "is_experimental": True
        },
        "billed_units": {
        "input_tokens": 0,
        "output_tokens": 0,
        "search_units": 0,
        "classifications": 0
        },
        "tokens": {
        "input_tokens": 0,
        "output_tokens": 0
        },
        "warnings": [
        "string"
        ]
    }
    return BaseResponse(code=200,msg="success",id=str(uuid.uuid4()),results=results,meta=meta)
