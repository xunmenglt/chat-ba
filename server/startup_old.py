# -*- coding:UTF-8 -*-
# @Time : 2024/3/5 21:17
# @Author : 寻梦
# @File : startup
# @Project : langchain-ChatBA

import os
import sys
import argparse
import platform
import threading
from configs import (logger,NLTK_DATA_PATH,DEFAULT_BIND_HOST,SERVER_PORT,HF_HOME,HF_ENDPOINT,HTTPX_DEFAULT_TIMEOUT)

os.environ["HF_ENDPOINT"]=HF_ENDPOINT
os.environ["HF_HOME"]=HF_HOME

from fastapi import FastAPI
from starlette.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html

from server.controller import all_api
from server.db.init_database_script import create_tables
from fast_chat_use import run_fastchat
import nltk
nltk.data.path = [NLTK_DATA_PATH] + nltk.data.path



app=FastAPI(
    title="LangChain-ChatBA",
    version="1.0",
    description="ChatBA实现多模型接入",
    docs_url=None,
    redoc_url=None,  # 设置 ReDoc 文档的路径
)




app.include_router(all_api)




app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="ChatBA",
        # oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url='/static/swagger/swagger-ui-bundle.js',
        swagger_css_url='/static/swagger/swagger-ui.css',
        swagger_favicon_url='/static/swagger/img.png',
    )


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/swagger/redoc.standalone.js",
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许访问的源
    allow_credentials=True,  # 支持 cookie
    allow_methods=["*"],  # 允许使用的请求方法
    allow_headers=["*"]  # 允许携带的 Headers
)

if __name__=="__main__":
    # 创建数据表格
    create_tables()


    if sys.platform.startswith('win'):
        logger.info('当前系统为 Windows,不启用fastchat')
    else:
        # 初始化fastchat
        run_fastchat()

    import uvicorn

    uvicorn.run(app,
                host=DEFAULT_BIND_HOST,
                port=SERVER_PORT)