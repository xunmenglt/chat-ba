# -*- coding:UTF-8 -*-
# @Time : 2024/3/9 11:38
# @Author : 寻梦
# @File : conversation_mapper
# @Project : langchain-ChatBA
import time
import uuid
from server.db.session import with_session
from server.db.models import ConversationModel,MessageModel
from sqlalchemy.orm import Session
from typing import List,Dict


@with_session
def create_conversation_to_db(session:Session,name:str,chat_type:str):
    # 先获取是否包含该对话框
    conversation=(session.query(ConversationModel)
                  .filter(ConversationModel.name.ilike(name))
                  .filter(ConversationModel.chat_type.ilike(chat_type))
                  ).first()
    if conversation:
        return False
    conversation=ConversationModel(id="conversation_"+str(int(time.time())),name=name,chat_type=chat_type)
    session.add(conversation)
    return True

@with_session
def list_conversation_from_db(session:Session,type:str):
    if type is None:
        conversations:List[ConversationModel]=session.query(ConversationModel)
    else:
        conversations:List[ConversationModel] = session.query(ConversationModel).filter(ConversationModel.chat_type.ilike(type))
    return [{"id":conversation.id,"name":conversation.name,"chat_type":conversation.chat_type}for conversation in conversations]


@with_session
def delete_conversation_to_db(session:Session,conversation_id:str):
    conversation=(session.query(ConversationModel).filter(ConversationModel.id.ilike(conversation_id))).first()
    if conversation:
        session.delete(conversation)
        return (True,conversation.name)
    else:
        return (False,None)



@with_session
def get_message_by_id(session:Session,message_id:str):
    message=session.query(MessageModel).filter_by(id=message_id).first()
    return message

@with_session
def get_message_list_by_conversation_id(session:Session,conversation_id:str):
    messageList:List[MessageModel]=session.query(MessageModel).filter_by(conversation_id=conversation_id).order_by(MessageModel.create_time)
    return [{"id":message.id,
             "conversation_id":message.conversation_id,
             "chat_type":message.chat_type,
             "query":message.query,
             "response":message.response,
             "meta_data":message.meta_data,
             "create_time":message.create_time} for message in messageList]

@with_session
def update_message(session:Session,message_id:str,response: str = None, metadata: Dict = None):
    m = get_message_by_id(message_id)
    if m is not None:
        if response is not None:
            m.response = response
        if isinstance(metadata, dict):
            m.meta_data = metadata
        session.add(m)
        session.commit()
        return m.id

@with_session
def add_message_to_db(session, conversation_id: str, chat_type, query, response="", message_id=None,
                      metadata: Dict = {}):
    """
    新增聊天记录
    """
    if not message_id:
        message_id = uuid.uuid4().hex
    m = MessageModel(id=message_id, chat_type=chat_type, query=query, response=response,
                     conversation_id=conversation_id,
                     meta_data=metadata)
    session.add(m)
    session.commit()
    return m.id


@with_session
def filter_message(session, conversation_id: str, limit: int = 10)->List:
    messages = (session.query(MessageModel).filter(MessageModel.conversation_id.ilike(conversation_id)).
                # 用户最新的query 也会插入到db，忽略这个message record
                filter(MessageModel.response != '').
                # 返回最近的limit 条记录
                order_by(MessageModel.create_time.desc()).limit(limit).all())
    # 直接返回 List[MessageModel] 报错
    data = []
    for m in messages:
        data.append({"input": m.query, "output": m.response})
    return data
