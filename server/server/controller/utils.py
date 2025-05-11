# -*- coding:UTF-8 -*-
# @Time : 2024/3/6 15:15
# @Author : 寻梦
# @File : utils
# @Project : langchain-ChatBA
import os
import pydantic
from pydantic import BaseModel
from typing import Any,List
from configs import KB_ROOT_PATH

class BaseResponse(BaseModel):
    code: int = pydantic.Field(200, description="API status code")
    msg: str = pydantic.Field("success", description="API status message")
    data: Any = pydantic.Field(None, description="API data")

    class Config:
        schema_extra = {
            "example": {
                "code": 200,
                "msg": "success",
            }
        }


class ListModelResponse(BaseResponse):
    data: List[BaseModel] = pydantic.Field(..., description="List of model")

    class Config:
        schema_extra = {
            "example": {
                "code": 200,
                "msg": "success",
                "data": "[{},{}]",
            }
        }


class ListResponse(BaseResponse):
    data: List[str] = pydantic.Field(..., description="List of names")

    class Config:
        schema_extra = {
            "example": {
                "code": 200,
                "msg": "success",
                "data": ["doc1.docx", "doc2.pdf", "doc3.txt"],
            }
        }





