# -*- coding:UTF-8 -*-
# @Time : 2024/3/8 20:21
# @Author : 寻梦
# @File : konwledgeVectorController
# @Project : langchain-ChatBA

from fastapi import APIRouter
from configs import kbs_config
from server.controller.utils import BaseResponse

vector_app=APIRouter(tags=["向量库处理api"],prefix="/vector_store")

@vector_app.get("/list",description="获取向量库列表")
async def vector_store_list():
    return BaseResponse(data=list(kbs_config.keys()))