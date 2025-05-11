from fastapi import FastAPI
from server.controller import all_api
from configs import API_SERVER,NLTK_DATA_PATH
import nltk
nltk.data.path = [NLTK_DATA_PATH] + nltk.data.path

def create_app(run_mode:str=None):
    app=FastAPI(
        title="ChatBA服务接口",
        version="1.0",
        description="ChatBA为你实现多模型接入",
    )
    app.include_router(all_api)
    return app
    