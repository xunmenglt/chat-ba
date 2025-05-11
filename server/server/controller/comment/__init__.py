# -*- coding:UTF-8 -*-
# @Time : 2024/3/6 15:35
# @Author : 寻梦
# @File : __init__.py
# @Project : langchain-ChatBA
from .modelController import *
from .promptController import *
from .fileController import * 
from fastapi import APIRouter

comment_app=APIRouter(prefix="/comment",tags=["通用接口api"])

comment_app.include_router(model_app)
comment_app.include_router(prompt_app)
comment_app.include_router(file_app)