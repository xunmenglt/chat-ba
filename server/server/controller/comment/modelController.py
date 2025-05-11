# -*- coding:UTF-8 -*-
# @Time : 2024/3/10 17:27
# @Author : 寻梦
# @File : modelController
# @Project : langchain-ChatBA
from fastapi import APIRouter,Body
from server.controller.utils import BaseResponse
from pool.model_pool import model_pool

model_app=APIRouter(tags=["模型管理api"],prefix="/model")

@model_app.get("/list",description="获取模型列表")
def list_model(type:str=None)->BaseResponse:
    models=[]
    for key in model_pool.get_model_dict().keys():
        models.append(key)
    return BaseResponse(data=models)