# -*- coding:UTF-8 -*-
import json
import os
import re
from typing import Iterator, List

from langchain_community.document_loaders.base import BaseLoader
from langchain_core.documents import Document
from server.db.mapper import question_answer_mapper
from langchain_text_splitters import RecursiveCharacterTextSplitter
import tqdm

class CustomJSONLFileLoader(BaseLoader):


    def __init__(self,file_path:str,question_key:str="question",answer_key:str="answer",encoding:str="utf-8",**kwargs):
        self.file_path=file_path
        self.question_key=question_key
        self.answer_key=answer_key
        self.encoding=encoding


    def load(self) -> List[Document]:
        documents=[]
        with open(self.file_path,'r',encoding=self.encoding) as fp:
            print("开始加载文件...")
            contents=fp.readlines()
            print("文件加载完成...")
            print("开始生成document")
            sort=0
            for content in tqdm.tqdm(contents):
                sort=sort+1
                json_data=json.loads(content)
                question=json_data[self.question_key]
                answer=json_data[self.answer_key]
                documents.append(Document(page_content=question,metadata={"sort":sort,"source":self.file_path}))
                documents.append(Document(page_content=answer,metadata={"sort":sort,"source":self.file_path}))
                question_answer_mapper.add_qa_to_db(file_path=self.file_path,question=question,answer=answer,sort=sort)
        return documents


    def lazy_load(self) -> Iterator[Document]:
        """A lazy loader for Documents."""
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement lazy_load()"
        )

class LocalJSONLDataSetDatabase:
    """dir_path 如果不知到怎么设置的化最好为绝对路径 """
    def __init__(self,id_key:str,dir_path:str="data",encoding="utf-8"):
        if not os.path.isdir(dir_path):
            raise RuntimeError(f"dataset path {dir_path} is not a dir")
        file_path_list=[]
        for root,dirs,files in os.walk(dir_path):
            for file in files:
                # 数据文件只能是jsonl格式文件
                if re.match("^.*\.jsonl$",file):
                    file_path_list.append(os.path.join(root,file))
        self.store=dict()
        for file_path in file_path_list:
            with open(file_path,'r',encoding=encoding) as fp:
                contents=fp.readlines()
                for content in contents:
                    json_data=json.loads(content)
                    id=json_data[id_key]
                    self.store[id]=json_data

    def __len__(self):
        return len(self.store)

    def __getitem__(self, item):
        return self.store[item]