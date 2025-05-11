# -*- coding:UTF-8 -*-
# @Time : 2024/3/6 15:33
# @Author : 寻梦
# @File : __init__.py
# @Project : langchain-ChatBA

from fastapi import APIRouter
from .tables_controller import tables_app
from .graph_controller import graphs_app

report_app=APIRouter(prefix="/report")
report_app.include_router(tables_app)
report_app.include_router(graphs_app)