import os
import sys
import json
import re
import atexit
import time
from filelock import FileLock
from contextlib import contextmanager
from typing import Callable,Optional,Dict, Any, List
from uuid import UUID
from langchain.callbacks.base import BaseCallbackHandler
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import QianfanChatEndpoint
from langchain.schema import LLMResult
from configs import (ONLINE_LLM_MODEL,FSCHAT_OPENAI_API)
from server.utils import get_model_worker_config

def get_faschat_server_open_api():
    return f"http://{FSCHAT_OPENAI_API['host']}:{FSCHAT_OPENAI_API['port']}/v1"

"""
model_dict={
    model_name:{
        is_online=False,
        children={
            0:{
                is_used=False
            }
        }
    }
}
"""
# model_dict: Dict[str, Dict] = {}

class SynchronizationModelLoadPool:
    class CallBackEndOfInferenceHandler(BaseCallbackHandler):
            def __init__(self,father,model_name):
                self.model_name=model_name
                self.father=father
            def on_llm_end(
                self, response: LLMResult, **kwargs: Any
            ) -> Any:
                print("释放：",self.model_name)
                self.father.change_model_status(self.model_name,False)
    
    def __init__(self):
        self.base_dir='data/tmp/lock'
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)
        self.lock_path=os.path.join(self.base_dir,"model_pool.txt.lock")
        self.lock=FileLock(self.lock_path)
        self.pool_path=os.path.join(self.base_dir,"model_pool.txt")
        if not os.path.exists(self.pool_path):
            with open(self.pool_path,'w',encoding="utf-8") as fp:
                fp.write(json.dumps({},ensure_ascii=False))
    def __del__(self):
        try:
            os.remove(self.pool_path)
            os.remove(self.lock_path)
        except Exception as e:
            print(e)
    def get_model_dict(self):
        model_dict=dict()
        with self.lock:
            with open(self.pool_path,'r',encoding="utf-8") as fp:
                content=fp.read()
                if content:
                    try:
                        model_dict=json.loads(content)
                    except Exception as e:
                        print(e)
        return model_dict
    
    def write_model_dict(self,model_dict):
        with self.lock:
            with open(self.pool_path,'w',encoding='utf-8') as fp:
                content=""
                try:
                    content=json.dumps(model_dict,ensure_ascii=False)
                except Exception as e:
                    print(e)
                fp.write(content)
    @contextmanager
    def obtain_model_dict(self):
        model_dict=self.get_model_dict()
        try:
            yield model_dict
        except:
            raise
        finally:
            self.write_model_dict(model_dict)


    # 解析模型名称，解析出模型名称和其编号
    def model_name_parse_to_threading(self,model_name:str):
        if not model_name:
            return None
        parrent=re.compile('^\S+@(\d+)$')
        idxs = parrent.findall(model_name)
        if not idxs:
            return (model_name,None)
        model_name=model_name.split(f"@{idxs[-1]}")[0]
        return (model_name,int(idxs[-1]))


    # 注册模型
    def register_model_in_dict(self,model_name):
        # 解析model_name
        model_name,idx=self.model_name_parse_to_threading(model_name)
        with self.obtain_model_dict() as model_dict:
            # 判断模型是否是线上model
            if not model_dict.get(model_name):
                model_dict[model_name]=dict(
                    is_online=False,
                    children={}
                )
            if model_name in ONLINE_LLM_MODEL:
                model_dict[model_name]["is_online"]=True
            if not idx:
                idx=-1
            model_dict[model_name]["children"][str(idx)]=dict(is_used=False)

    # 释放模型
    def release_model_in_dict(self,model_name):
        # 解析model_name
        model_name,idx=self.model_name_parse_to_threading(model_name)
        # 判断模型是否是线上model
        with self.obtain_model_dict() as model_dict:
            if not model_dict.get(model_name):
                return True
            if not idx:
                idx=-1
            del model_dict[model_name]["children"][str(idx)]
            if len(model_dict[model_name]["children"].keys())==0:
                del model_dict[model_name]

    # 判断当前model是否在使用
    def is_used_to_model(self,model_name):
        # 解析model_name
        model_name,idx=self.model_name_parse_to_threading(model_name)
        with self.obtain_model_dict() as model_dict:
            if model_dict[model_name]["is_online"]:
                return False
            if not idx:
                idx=-1
            return model_dict[model_name]["children"][str(idx)]["is_used"]

    # 改变模型
    def change_model_status(self,model_name,is_used):
        is_used=False
        # 解析model_name
        model_name,idx=self.model_name_parse_to_threading(model_name)
        with self.obtain_model_dict() as model_dict:
            if not idx:
                idx=-1
            model_dict[model_name]["children"][str(idx)]["is_used"]=is_used
            

    def get_model_name_in_dict(self,user_input_mode_name):
        with self.obtain_model_dict() as model_dict:
            if user_input_mode_name not in model_dict:
                raise RuntimeError("模型未注册")
            children=model_dict[user_input_mode_name]["children"]
            idxs=children.keys()
            for idx in idxs:
                idx=int(idx)
                if children[str(idx)]["is_used"]:
                    continue
                # TODO:原来是true，现在改成了False
                children[str(idx)]["is_used"]=False
                if idx==-1:
                    return user_input_mode_name
                return f"{user_input_mode_name}@{idx}"
        return None
    
    def load_model(self,model_name: str,
        temperature: float,
        top_p:float,
        max_tokens: int = None,
        streaming: bool = True,
        callbacks: List[Callable] = [],
        verbose: bool = True,
        auto_release_model:bool=True,
        **kwargs: Any
        ):
        model=None
        model_name=self.get_model_name_in_dict(model_name)
        if not model_name: # 模型已被占用
            return None,None
        
        if auto_release_model:
            callbacks.append(self.CallBackEndOfInferenceHandler(self,model_name=model_name))
        config=get_model_worker_config(model_name)    
        model = ChatOpenAI(
                streaming=streaming,
                verbose=verbose,
                callbacks=callbacks,
                openai_api_key=config.get("api_key","EMPTY"),
                openai_api_base=config.get('api_base_url',get_faschat_server_open_api()),
                model_name=model_name,
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens,
                openai_proxy=config.get("openai_proxy"),
                stream_usage=True,
                **kwargs
        )
        return model,model_name

model_pool=SynchronizationModelLoadPool()

atexit.register(model_pool.__del__)