# -*- coding:UTF-8 -*-
# @Time : 2024/3/9 11:45
# @Author : 寻梦
# @File : conversation_mapper
# @Project : langchain-ChatBA
from fastapi import APIRouter,Body
from server.controller.utils import BaseResponse
from server.services.chat.chat_utils import get_chat_type,create_conversation_services,list_conversation_service,delete_conversation_services,list_history_message
conversation_app=APIRouter(prefix="/conversation")

@conversation_app.get("/list",description="获取聊天窗口")
def list_conversation(type:str=None)->BaseResponse:
    conversations=list_conversation_service(type)
    return BaseResponse(data=conversations)

@conversation_app.post("/create",description="创建聊天窗口")
def create_conversation(name:str=Body(...,description="聊天窗口名字",examples=["myconversation"]),
                      type:str=Body(...,description="聊天类型",examples=["dialogue","retrieval"])
                      )->BaseResponse:
    chat_type=get_chat_type(type)
    if chat_type is None:
        return BaseResponse(code=500,msg=f"{type} 对话类型暂不支持")
    status=create_conversation_services(name,chat_type)
    if status:
        return BaseResponse(msg="对话框创建成功")
    return BaseResponse(code=500,msg="对话框创建失败")


@conversation_app.post("/delete/{conversation_id}",description="删除聊天窗口")
def delete_conversation(conversation_id:str)->BaseResponse:
    res = delete_conversation_services(conversation_id)
    if res[0]:
        return BaseResponse(msg=f"对话框 {res[1]} 删除成功")
    return BaseResponse(code=500, msg=f"对话框删除失败")

@conversation_app.get('/message/history/list/{conversation_id}',description="获取历史对话列表")
def message_history_list(conversation_id:str)->BaseResponse:
    messageList=[]
    if conversation_id:
        messageList=list_history_message(conversation_id=conversation_id)
    return BaseResponse(data=messageList)
