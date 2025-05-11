# -*- coding:UTF-8 -*-
# @Time : 2024/3/6 15:35
# @Author : 寻梦
# @File : __init__.py
# @Project : langchain-ChatBA
from .conversationController import *
from .dialogueController import *
from .retrievalController import *
from .openbaController import *
from .generationController import *
from .modelPkController import *
from fastapi import APIRouter

chat_app=APIRouter(prefix="/chat",tags=["聊天接口api"])

chat_app.include_router(conversation_app)
chat_app.include_router(dialogue_app)
chat_app.include_router(retrieval_app)
chat_app.include_router(openba_app)
chat_app.include_router(generation_app)
chat_app.include_router(pk_app)