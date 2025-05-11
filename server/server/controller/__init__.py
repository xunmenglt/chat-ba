# -*- coding:UTF-8 -*-
# @Time : 2024/3/6 15:03
# @Author : 寻梦
# @File : __init__.py
# @Project : langchain-ChatBA
from .konwledge_base import *
from .chat import *
from .comment import *
from .report import report_app
from fastapi import APIRouter
all_api=APIRouter(prefix="/api")
all_api.include_router(konwledge_base_app)
all_api.include_router(chat_app)
all_api.include_router(comment_app)
all_api.include_router(report_app)