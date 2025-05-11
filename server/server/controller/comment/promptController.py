# -*- coding:UTF-8 -*-
# @Time : 2024/3/10 17:27
# @Author : 寻梦
# @File : modelController
# @Project : langchain-ChatBA
from fastapi import APIRouter,Body
from server.controller.utils import BaseResponse

prompt_app=APIRouter(tags=["模板管理api"],prefix="/prompt")

@prompt_app.get("/list",description="获取模型列表")
def list_model(type:str=None)->BaseResponse:
    res=[]
    if type:
        from configs import prompt_config
        import importlib
        importlib.reload(prompt_config)
        PROMPT_TEMPLATES = prompt_config.PROMPT_TEMPLATES
        if PROMPT_TEMPLATES[type]:
            prompts=PROMPT_TEMPLATES[type]
            for key in prompts.keys():
                res.append(key)
    return BaseResponse(data=res)

@prompt_app.get("/info",description="获取模板信息")
def list_prompt_info(type:str=None,prompt_name:str=None)->BaseResponse:
    
    prompt=""
    if type and prompt_name:
        from configs import prompt_config
        import importlib
        importlib.reload(prompt_config)
        PROMPT_TEMPLATES = prompt_config.PROMPT_TEMPLATES
        if PROMPT_TEMPLATES.get(type) and PROMPT_TEMPLATES[type].get(prompt_name):
            prompt=PROMPT_TEMPLATES[type].get(prompt_name)
    return BaseResponse(data=prompt)