# -*- coding:UTF-8 -*-
# @Time : 2024/3/6 15:04
# @Author : 寻梦
# @File : knowledgeFactoryController
# @Project : langchain-ChatBA


from fastapi import APIRouter,Body
from fastapi.encoders import jsonable_encoder
from configs import logger,log_verbose
from server.services.knowledge_base.base import KBServiceFactory
from server.db.mapper.knowledge_factory_mapper import get_list_kb_from_db
from server.db.mapper.knowledge_file_mapper import get_file_list_in_db
from configs import EMBEDDING_MODEL,ONLINE_EMBED_MODEL,MODEL_PATH
from server.controller.utils import *
from server.utils import validate_factory_name



konwledge_factory_app=APIRouter(tags=["知识库管理api"],prefix="/konwledge_factory")


'''
知识库控制层
'''

"""
知识库名
知识库简介
向量库类型
嵌入模型名称
"""
@konwledge_factory_app.post("/create",description="创建知识库库")
async def factory_create(
        factory_name:str=Body(...,examples=["myfactory","foods"]),
        vector_store_type:str=Body("qdrant"),
        embed_model:str=Body(EMBEDDING_MODEL),
        info:str=Body("",description="知识库描述")
)->BaseResponse:
    """
    知识库创建api
    """
    if not validate_factory_name(factory_name):
        return BaseResponse(code=403, msg="不要进行危险注入")
    if factory_name is None or factory_name.strip() == "":
        return BaseResponse(code=404, msg="知识库名称不能为空，请重新填写知识库名称")
    kb = KBServiceFactory.get_service_by_name(factory_name)
    if kb is not None:
        return BaseResponse(code=404, msg=f"已存在同名知识库 {factory_name}")

    kb = KBServiceFactory.get_service(factory_name, vector_store_type, embed_model)
    try:
        kb.kb_info=info
        st= kb.create_kb()
        if st==0:
            return BaseResponse(code=500, msg="无法连接远程向量库，向量数据库创建异常")
    except Exception as e:
        msg = f"创建知识库出错： {e}"
        logger.error(f'{e.__class__.__name__}: {msg}',
                     exc_info=e if log_verbose else None)
        return BaseResponse(code=500, msg=msg)

    return BaseResponse(code=200, msg=f"已新增知识库 {factory_name}")








@konwledge_factory_app.get("/list",description="获取知识库库列表")
async def factory_list()->BaseResponse:
    return BaseResponse(code=200, data=get_list_kb_from_db())



@konwledge_factory_app.get("/file_list",description="根据知识库获取知识列表")
async def file_list_in_factory(factory_name:str)->BaseResponse:
    return BaseResponse(code=200,data=get_file_list_in_db(factory_name))


@konwledge_factory_app.post("/delete/{factory_name}",description="删除知识库库")
async def factory_delete(
        factory_name:str
)->BaseResponse:
    factory_obj=KBServiceFactory.get_service_by_name(factory_name)
    status=factory_obj.delete_kb()
    if status:
        return BaseResponse(code=200,msg=f"{factory_name} 知识库删除成功")
    return BaseResponse(code=500,msg=f"{factory_name} 知识库删除失败")

@konwledge_factory_app.get("/embedding_list",description="获取embedding列表")
async def list_embedding(
)->BaseResponse:
    data= set(list(ONLINE_EMBED_MODEL.keys())+list(MODEL_PATH["embed_model"].keys()))
    return BaseResponse(data=data)