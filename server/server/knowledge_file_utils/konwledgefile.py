# -*- coding:UTF-8 -*-
# @Time : 2024/3/7 15:22
# @Author : 寻梦
# @File : konwledgefile
# @Project : langchain-ChatBA
import importlib
import os.path

import langchain

from langchain.docstore.document import Document
from langchain.text_splitter import TextSplitter
from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path
from typing import List, Union,Dict, Tuple, Generator

from server.utils import get_file_path,run_in_thread_pool
from configs import log_verbose,logger,text_splitter_dict,TEXT_SPLITTER_NAME,CHUNK_SIZE,OVERLAP_SIZE
import chardet

LOADER_DICT = {
               "PDFPlumberLoader":['.pdf'],
               "UnstructuredWordDocumentLoader": ['.docx', '.doc'],
               "CustomJSONLFileLoader":[".jsonl"],
               "TextLoader":[".txt"]
               }
SELF_LOADER=["CustomJSONLFileLoader"]
def get_LoaderClass(file_extension):
    for LoaderClass, extensions in LOADER_DICT.items():
        if file_extension in extensions:
            return LoaderClass
SUPPORTED_EXTS = [ext for sublist in LOADER_DICT.values() for ext in sublist]


"""
====================================================================================
"""

def get_loader(loader_name: str, file_path: str):
    loader_kwargs={}
    try:
        if loader_name in SELF_LOADER:
            document_loaders_module=importlib.import_module("document_loaders")
        else:
            document_loaders_module=importlib.import_module("langchain.document_loaders")
        DocumentLoader=getattr(document_loaders_module, loader_name)
    except Exception as e:
        msg = f"为文件{file_path}查找加载器{loader_name}时出错：{e}"
        logger.error(f'{e.__class__.__name__}: {msg}',
                     exc_info=e if log_verbose else None)
        document_loaders_module = importlib.import_module("langchain.document_loaders")
        DocumentLoader = getattr(document_loaders_module, "UnstructuredFileLoader")

    if loader_name=="UnstructuredFileLoader":
        loader_kwargs.setdefault("autodetect_encoding", True)
    elif loader_name=="CSVLoader":
        if not loader_kwargs.get("encoding"):
            # 如果未指定 encoding，自动识别文件编码类型，避免langchain loader 加载文件报编码错误
            with open(file_path, 'rb') as struct_file:
                encode_detect = chardet.detect(struct_file.read())
            if encode_detect is None:
                encode_detect = {"encoding": "utf-8"}
            loader_kwargs["encoding"] = encode_detect["encoding"]

    elif loader_name == "JSONLoader":
        loader_kwargs.setdefault("jq_schema", ".")
        loader_kwargs.setdefault("text_content", False)
    elif loader_name == "JSONLinesLoader":
        loader_kwargs.setdefault("jq_schema", ".")
        loader_kwargs.setdefault("text_content", False)
    loader = DocumentLoader(file_path, **loader_kwargs)
    return loader


"""
=======================================================
"""
def make_text_splitter(splitter_name:str=TEXT_SPLITTER_NAME,
                       chunk_size:int=CHUNK_SIZE,
                       chunk_overlap=OVERLAP_SIZE):
    """
    根据参数获取特地的分词器
    """
    splitter_name = splitter_name or "SpacyTextSplitter"
    try:
        if splitter_name == "MarkdownHeaderTextSplitter":  # MarkdownHeaderTextSplitter特殊判定
            headers_to_split_on = text_splitter_dict[splitter_name]['headers_to_split_on']
            text_splitter = langchain.text_splitter.MarkdownHeaderTextSplitter(
                headers_to_split_on=headers_to_split_on)
        else:
            try:    ## 优先使用用户自定义的text_splitter
                text_splitter_module= importlib.import_module('text_splitter')
                TextSplitter=getattr(text_splitter_module,splitter_name)
            except:     ## 否则使用langchain的text_splitter
                text_splitter_module=importlib.import_module("langchain.text_splitter")
                TextSplitter=getattr(text_splitter_module,splitter_name)
            try:
                text_splitter = TextSplitter(
                    pipeline="zh_core_web_sm",
                    chunk_size=chunk_size,
                    chunk_overlap=chunk_overlap
                )
            except:
                text_splitter = TextSplitter(
                    chunk_size=chunk_size,
                    chunk_overlap=chunk_overlap
                )


    except Exception as e:
        print(e)
        text_splitter_module = importlib.import_module('langchain.text_splitter')
        TextSplitter = getattr(text_splitter_module, "RecursiveCharacterTextSplitter")
        text_splitter = TextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter









class KnowLedgeFile:
    def __init__(self,
                filename: str,
                factory_name: str,):
        self.factory_name=factory_name
        self.filename=str(Path(filename).as_posix())
        self.ext=os.path.splitext(filename)[-1].lower()
        if self.ext not in SUPPORTED_EXTS:
            raise ValueError(f"暂未支持的文件格式 {self.filename}")
        self.filepath=get_file_path(factory_name,filename)
        self.docs=None
        self.splited_docs = None
        self.document_loader_name = get_LoaderClass(self.ext)
        self.text_splitter_name = TEXT_SPLITTER_NAME

    def file2docs(self,refresh:bool=False):
        # 判断是否要加载文档
        if self.docs is None or refresh:
            loader=get_loader(loader_name=self.document_loader_name,file_path=self.filepath)
            self.docs = loader.load()
        return self.docs

    def docs2texts(self,docs:List[Document]=None,refresh:bool=False,
                   chunk_size:int=CHUNK_SIZE,
                   chunk_overlap:int=OVERLAP_SIZE,
                   text_splitter:TextSplitter=None
                   ):
        docs=docs or self.file2docs(refresh=refresh)
        if not docs:
            return []
        if self.ext not in [".csv"]:
            if text_splitter is None:
                text_splitter=make_text_splitter(splitter_name=self.text_splitter_name,
                                                 chunk_size=chunk_size,
                                                 chunk_overlap=chunk_overlap)
            if self.text_splitter_name=="MarkdownHeaderTextSplitter":
                docs=text_splitter.split_text(docs[0].page_content)
            else:
                docs=text_splitter.split_documents(docs)
        if not docs:
            return []
        print(f"文档切分示例：{docs[0]}")
        self.splited_docs = docs
        return self.splited_docs

    def file2text(self,
                  chunk_size: int = CHUNK_SIZE,
                  chunk_overlap: int = OVERLAP_SIZE,
                  text_splitter: TextSplitter = None,
                  refresh: bool = False):
        if self.splited_docs is None or refresh:
            docs=self.file2docs()
            self.splited_docs=self.docs2texts(
                docs=docs,
                refresh=refresh,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                text_splitter=text_splitter
            )
        return self.splited_docs

    # 判断文件是否存在
    def file_exist(self):
        return os.path.isfile(self.filepath)

    # 获取文件创建时间
    def get_mtime(self):
        return os.path.getmtime(self.filepath)

    # 获取文件大小
    def get_size(self):
        return os.path.getsize(self.filepath)



"""
================================================
"""
def files2docs_in_thread(
        files: List[Union[KnowLedgeFile, Tuple[str, str], Dict]],
        chunk_size: int = CHUNK_SIZE,
        chunk_overlap: int = OVERLAP_SIZE,
)->Generator:
    '''
    利用多线程批量将磁盘文件转换成langchain Document.
    如果传入参数是Tuple，形式为(filename, kb_name)
    生成器返回值为 status, (kb_name, file_name, docs | error)
    '''

    def file2docs(*, file: KnowLedgeFile, **kwargs)->Tuple[bool,Tuple[str,str,Union[List[Document],str]]]:
        try:
            return True,(file.factory_name, file.filename, file.file2text(**kwargs))
        except Exception as e:
            msg = f"从文件 {file.factory_name}/{file.filename} 加载文档时出错：{e}"
            logger.error(f'{e.__class__.__name__}: {msg}',
                         exc_info=e if log_verbose else None)
            return False, (file.factory_name, file.filename, msg)

    kwargs_list=[]
    for i,file in enumerate(files):
        kwargs={}
        try:
            if isinstance(file,tuple) and len(file)==2:
                filename=file[0]
                factory_name=file[1]
                file=KnowLedgeFile(filename=filename,factory_name=factory_name)
            elif isinstance(file,dict):
                filename=file.pop("filename")
                factory_name = file.pop("factory_name")
                file = KnowLedgeFile(filename=filename, factory_name=factory_name)
            kwargs["file"] = file
            kwargs["chunk_size"] = chunk_size
            kwargs["chunk_overlap"] = chunk_overlap
            kwargs_list.append(kwargs)
        except Exception as e:
            yield False, (factory_name, filename, str(e))
    for result in run_in_thread_pool(func=file2docs,params=kwargs_list):
        yield result



