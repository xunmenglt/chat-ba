# -*- coding:UTF-8 -*-
# @Time : 2024/6/11 14:27
# @Author : 寻梦
# @File : fileController
# @Project : langchain-ChatBA
import os
from fastapi import APIRouter,Query
from fastapi.responses import FileResponse
from server.controller.utils import BaseResponse
from configs import KB_ROOT_PATH 
from server.services.file import fileService
from server.db.mapper import question_answer_mapper
from server.utils import get_file_path


file_app=APIRouter(tags=["模型管理api"],prefix="/file")


@file_app.get("/view/{file_id}",description="查看pdf文件")
def view_file(file_id:str=None)->FileResponse:
    file=fileService.get_file_by_id(file_id)
    print(file,type(file))
    if file and file["file_ext"] and (file["file_ext"].__contains__('.pdf') or file["file_ext"].__contains__('.doc')):
        file_path=os.path.join(KB_ROOT_PATH,file["kb_name"],"content",file["file_name"])
        # print("当前文件地址：",file_path)
        response=FileResponse(file_path)
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response
    else:
        return None
    
@file_app.get("/qa/list",description="查看pdf文件")
def qa_list(query:str=Query("",description="查询"),
            sort:int=Query(-1,description="排序"),
            file_name:str=Query("NULL",description="文件名"),
            factory_name:str=Query("NULL",description="知识库名")
            )->BaseResponse:
    if not os.path.isabs(file_name):
        file_path=get_file_path(factory_name=factory_name,doc_name=file_name)
    else:
        file_path=file_name
    res=question_answer_mapper.list_from_db(file_path=file_path,sort=sort,query=query)
    return BaseResponse(code=200,msg="SUCCESS",data=res)