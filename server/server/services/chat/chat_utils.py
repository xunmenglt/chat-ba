# -*- coding:UTF-8 -*-
# @Time : 2024/3/9 11:25
# @Author : 寻梦
# @File : chat_utils
# @Project : langchain-ChatBA
import re
from typing import Callable,Optional,Dict, Any, List

from server.db.mapper.conversation_mapper import (create_conversation_to_db,
                                                  list_conversation_from_db,
                                                  delete_conversation_to_db,
                                                  add_message_to_db,
                                                  filter_message,
                                                  get_message_list_by_conversation_id)
from configs import (VECTOR_SEARCH_TOP_K,
                     SCORE_THRESHOLD,
                     ONLINE_LLM_MODEL,FSCHAT_OPENAI_API)
from server.services.knowledge_base.base import KBServiceFactory

class ChatType:
    DIALOGUE="dialogue"
    RETRIEVAL="retrieval"
    GENERATION="generation"

def get_chat_type(type:str)->str:
    try:
        chat_type = getattr(ChatType, type.upper())
        return chat_type
    except:
        return None

def get_chat_type_list():
    return ["dialogue","retrieval"]


# 创建聊天窗口
def create_conversation_services(name:str,chat_type:str):
    status=create_conversation_to_db(name,chat_type)
    return status

def list_conversation_service(type:str):
    return list_conversation_from_db(type)

def delete_conversation_services(conversation_id:str):
    return delete_conversation_to_db(conversation_id)


def add_message_service(chat_type:str,query:str,conversation_id:str):
    return add_message_to_db(conversation_id=conversation_id, chat_type=chat_type, query=query)

def list_history_message(conversation_id:str):
    return get_message_list_by_conversation_id(conversation_id=conversation_id)



def process_history(conversation_id:str=None,historys:List[Dict]=[],history_len:int=10)->str:
    tmp = ""
    if len(historys)>0:
        for idx,history in enumerate(historys):
            tmp+="user:"+history["input"]
            tmp+="\n"
            tmp+="assistant:"+history["output"]+"\n"
    elif history_len>0 and conversation_id is not None:
        historys=filter_message(conversation_id=conversation_id,limit=history_len)
        for idx,history in enumerate(historys):
            if (idx!=len(historys)-1 and idx!=0):
                tmp+="\n"
            tmp+="user:"+history["input"]
            tmp+="\n"
            tmp+="assistant:"+history["output"]+"\n"
    return tmp

def process_history_messages(conversation_id:str=None,
                             historys:List[Dict]=[],
                             history_len:int=10,
                             prompt_template:str="{input}"):
    messages = []
    if len(historys)>0:
        for idx,history in enumerate(historys):
            if history.get("input"):
                messages.append(("user",history["input"]))
            if history.get("output"):   
                messages.append(("assistant",history["output"]))
    elif history_len>0 and conversation_id is not None:
        historys=filter_message(conversation_id=conversation_id,limit=history_len)
        historys.reverse()
        for idx,history in enumerate(historys):
            if history.get("input"):
                messages.append(("user",history["input"]))
            if history.get("output"):   
                messages.append(("assistant",history["output"]))
    if prompt_template!=None:
        try:
            messages.append(("user",prompt_template))
        except:
            pass
    return messages


# 更具模板名获取模板
def get_prompt_template(type: str, name: str) -> Optional[str]:
    from configs import prompt_config
    import importlib
    importlib.reload(prompt_config)
    return prompt_config.PROMPT_TEMPLATES[type].get(name)


def search_docs(query:str=None,kb_name=None,top_k=VECTOR_SEARCH_TOP_K,score_threshold=SCORE_THRESHOLD):
    kb=KBServiceFactory.get_service_by_name(kb_name)
    data=[]
    if kb is not None:
        if query:
            data=kb.search_docs(query,top_k,score_threshold)
    return data