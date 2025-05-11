# -*- coding:UTF-8 -*-
# @Time : 2024/3/6 15:33
# @Author : 寻梦
# @File : __init__.py
# @Project : langchain-ChatBA

from .knowledgeFactoryController import konwledge_factory_app
from .konwledgeDocController import konwledge_doc_app
from .konwledgeVectorController import vector_app
from fastapi import APIRouter

konwledge_base_app=APIRouter(prefix="/konwledge_base")
konwledge_base_app.include_router(konwledge_factory_app)
konwledge_base_app.include_router(konwledge_doc_app)
konwledge_base_app.include_router(vector_app)