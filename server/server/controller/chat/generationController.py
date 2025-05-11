# -*- coding:UTF-8 -*-
# @Time : 2024/3/9 14:16
# @Author : 寻梦
# @File : retrievalController
# @Project : langchain-ChatBA
import json
import time
import asyncio
import logging
import os
import uuid
import tqdm
import re
import csv
from sse_starlette.sse import EventSourceResponse
from typing import List,Dict,Optional,AsyncIterable,Awaitable
from fastapi import APIRouter,Body,Request,UploadFile,File,Form,Path
from fastapi.responses import FileResponse
from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import chain
from langchain_core.prompt_values import (
    PromptValue
)

from server.controller.utils import BaseResponse
from server.utils import run_in_thread_pool
from server.services.chat.chat_utils import ChatType,get_prompt_template
from configs import logger,TEMPERATURE,LLM_MODELS,MAX_TOKENS
from server.tool.pdf_utils import ChapterRegulationTextParser
from server.tool.online_judge import eval_qa_quality
from pool.model_pool import model_pool


generation_app=APIRouter()


# @konwledge_doc_app.post("/upload_files",description="上传文件")
'''
多线程保存文件
'''


def save_qa_result_to_file(qa_box_id:str,all_qa_list:List[Dict]):
    file_id=uuid.uuid1().hex
    if qa_box_id and all_qa_list and len(all_qa_list)>0:    
        file_dir=os.path.join("data/tmp/qa_result",qa_box_id)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        file_path=os.path.join(file_dir,f"{file_id}.jsonl")
        with open(file_path,'w',encoding="utf-8") as fp:
            for qa in all_qa_list:
                fp.write(json.dumps(qa,ensure_ascii=False))
                fp.write("\n")
        return file_id
    else:
        return None

def get_qa_result_file_score(qa_box_id:str,file_id:str):
    if not qa_box_id:
        return ([],-1)
    # 获取qa_box_id对应的答案结果
    file_dir=os.path.join("data/tmp/qa_result",qa_box_id)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    file_path=os.path.join(file_dir,f"{file_id}.jsonl")
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        return ([],-2)
    with open(file_path,'r',encoding="utf-8") as fp:
        lines=fp.readlines()
        tmp_qa_list=[json.loads(line) for line in lines]
    if not tmp_qa_list or len(tmp_qa_list)<=0:
        return([],0)
    try:
        qa_every_score,average=eval_qa_quality(model_type='gpt',qa_list=tmp_qa_list)
    except Exception as e:
        print(e)
        return ([],-3)
    return qa_every_score,average



def parse_model_output_to_qa(context)->List[Dict]:
    result=[]
    # 用于匹配问答对
    pattern = re.compile(r"\{[.\s]*[\"']question[\"']:[.\s]*[\"']([^'\"]+)[\"'],[.\s]*[\"']answer[\"']:[.\s][\"']([^'\"]+)[\"'][.\s]*\}")
    matches = pattern.findall(context)
    if matches and len(matches)>0:
        result = [{'question': question, 'answer': answer} for question, answer in matches]
    return result
    
def save_files_in_thread(files: List[UploadFile],
                        dir_path:str):

    def save_file(file: UploadFile, dir_path:str) -> dict:
        '''
        保存单个文件。
        '''
        try:
            filename = file.filename
            file_path = os.path.join(dir_path,file.filename)
            file_content = file.file.read()
            if not os.path.isdir(os.path.dirname(file_path)):
                os.makedirs(os.path.dirname(file_path))
            with open(file_path, "wb") as f:
                f.write(file_content)
            return filename
        except Exception as e:
            return None

    params = [{"file": file, "dir_path":dir_path} for file in files]
    for result in run_in_thread_pool(save_file, params=params):
        yield result


@generation_app.post("/generation/uploadfile",description="上传文件")
def uploadfile(
    files:List[UploadFile]=File(...,description="上传文件，支持多个文件"),
)->BaseResponse:
    upload_id=uuid.uuid1().hex
    # 创建文件路径
    success_files=set() # 成功上传的文件
    save_dir=os.path.join("data/tmp",upload_id)
    for result in save_files_in_thread(files,save_dir):
        filename=result
        if filename:
            success_files.add(filename)
    return BaseResponse(code=200,msg="success",data={
        "upload_id":upload_id,
        "success_files":list(success_files)
    })

@generation_app.post("/generation/downloadqa",description="下载问答对")
def downloadQAFile(
    qa_box_id:str=Body(...,description="对话唯一id"),
    file_id:str=Body(...,description="文件id"),
    qa_ids:List[int]=Body([],description="问答对id"),
)->FileResponse:
    # 获取文件路径
    file_dir=os.path.join("data/tmp/qa_result",qa_box_id)
    file_path=os.path.join(file_dir,f"{file_id}.jsonl")
    if not os.path.exists(file_path):
        raise FileNotFoundError("文件不存在")
    select_list=[]
    with open(file_path,'r',encoding="utf-8") as fp:
        contents=fp.readlines()
        temp_list=[json.loads(content) for content in contents]
        for id in qa_ids:
            for temp in temp_list:
                if id==temp["index"]:
                    select_list.append(temp)
    new_file=os.path.join(file_dir,f"{file_id}_tmp.jsonl")
   
    with open(new_file,'w',encoding="utf-8") as fp:
        csv_writer=csv.writer(fp)
        csv_writer.writerow([
            "编号","问题","答案","提示词","文件名"
        ])
        
        for json_data in select_list:
            csv_writer.writerow(
                [
                    json_data["index"],
                    json_data["question"],
                    json_data["answer"],
                    json_data["prompt"],
                    json_data["filename"]
                ]
            )
    return FileResponse(new_file, media_type="application/octet-stream", filename=f"{file_id}.csv")




@generation_app.post("/generation/qa_generation",description="问答数据生成")
async def generation(input: str = Body(..., description="用户输入"),
                    top_p: float=Body(0.9, description="top_p"),
                    temperature: float = Body(TEMPERATURE, description="LLM 采样温度", ge=0.0, le=1.0),
                    model_name: str = Body(LLM_MODELS[0], description="LLM 模型名称。"),
                    max_tokens: Optional[int] = Body(
                                  MAX_TOKENS,
                                  description="限制LLM生成Token数量，默认None代表模型最大值"
                    ),
                    prompt_name: str = Body(
                                  "default",
                                  description="使用的prompt模板名称"
                    ),
                    query_type=Body("input",description="查询类型", examples=["input","file"]),
                    upload_id=Body("NULL",description="文件上传id"),
                    file_name=Body("NULL",description="文件名称"),
                    qa_count=Body(3,description="生成问答对数量"),
                    qa_box_id:str=Body(...,description="对话唯一id"),
                    do_split:bool=Body(False,description="是否对文档进行拆分")
                ):
    def qa_generation_iterator():
        """
        code:
            0:表示开始生成
            1:表示生成中
            2:生成的答案
            3:生成结束
            4:异常
            5:重试次数
        """
        nonlocal max_tokens
        if isinstance(max_tokens, int) and max_tokens <= 0:
            max_tokens = 1024
        try:
            model,real_model_name = model_pool.load_model(
                model_name=model_name,
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens,
                streaming=False,
                auto_release_model=False
            )
        except Exception as e:
            print(e)
            yield json.dumps({"answer": {"msg":'模型获取异常，请更换模型'},"flag":4}, ensure_ascii=False)
            return
        if not model:
            yield json.dumps({"answer": {"msg":'当前访问量过大，请稍后访问'},"flag":4}, ensure_ascii=False)
            return
        prompt_template = get_prompt_template(ChatType.GENERATION, prompt_name)
        prompt = ChatPromptTemplate.from_messages(
            [("user",prompt_template)],
            template_format="mustache"
        )
        
        chain = prompt | model | StrOutputParser()

        if query_type=='file':
            # todo 解析quey
            file_path=os.path.join("data/tmp",upload_id,file_name)
            if not os.path.exists(file_path):
                yield json.dumps({"answer": {"msg":'文件不存在'},"flag":4}, ensure_ascii=False)
                # 释放模型
                model_pool.change_model_status(model_name=real_model_name,is_used=False)
                return
            try:
                text_parser=ChapterRegulationTextParser(file_path=file_path,do_split=do_split)
            except Exception as e:
                print(e)
                yield json.dumps({"answer": {"msg":'文件解析异常，请使用指定格式'},"flag":4}, ensure_ascii=False)
                model_pool.change_model_status(model_name=real_model_name,is_used=False)
                return
            title="".join(file_name.split(".pdf")[0:-1])
        else:
            if not input:
                yield json.dumps({"answer": {"msg":'输入不能为空'},"flag":4}, ensure_ascii=False)
                # 释放模型
                model_pool.change_model_status(model_name=real_model_name,is_used=False)
                return
        yield json.dumps({"answer": {"msg":'正在生成'},"flag":0}, ensure_ascii=False)
        current_qa_count=1
        max_try=qa_count*2
        all_qa_list=[]
        while max_try>0 and current_qa_count<=qa_count:
            yield json.dumps({"answer": {"msg":'重试次数',"max_try":max_try},"flag":5}, ensure_ascii=False)
            if query_type=="file":
                if do_split:
                    try:
                        mixed_content=text_parser.mixed2regulation()
                        chapter_01=mixed_content["chapter_01"]
                        item_01=mixed_content["item_01"]
                        chapter_02=mixed_content["chapter_02"]
                        item_02=mixed_content["item_02"]
                        context=title+"\n"+chapter_01+"\n"+item_01+"\n"+chapter_02+"\n"+item_02
                    except Exception as e:
                        print(e)
                        yield json.dumps({"answer": {"msg":'文件解析异常，请使用指定格式'},"flag":4}, ensure_ascii=False)
                        model_pool.change_model_status(model_name=real_model_name,is_used=False)
                        return
                else:
                    context=text_parser.content
            else:
                context=input
            current_prompt=prompt.format_messages(context=context,count=qa_count)[0].content
            model_output=chain.invoke({"context":context,"count":qa_count})
            # to do 编写将模型输出解析为问答对的数据
            print(context)
            print("==========================")
            print(model_output)
            print("=============================")
            qa_list=parse_model_output_to_qa(model_output)
            print(qa_list)
            if qa_list and len(qa_list)>0:
                for qa_json in qa_list:
                    qa_json["index"]=current_qa_count
                    qa_json["filename"]=file_path.split('/')[-1]
                    if current_qa_count>qa_count:
                        break
                    all_qa_list.append(qa_json)
                    yield json.dumps({"answer": {"msg":'success',"data":qa_json,"index":current_qa_count},"flag":2}, ensure_ascii=False)
                    qa_json["prompt"]=current_prompt
                    current_qa_count+=1
            max_try-=1
        # 释放模型
        model_pool.change_model_status(model_name=real_model_name,is_used=False)
        # todo 去保存问答对
        file_id=save_qa_result_to_file(qa_box_id,all_qa_list)
        yield json.dumps({"answer": {"msg":'文件id',"data":{"qa_box_id":qa_box_id,"file_id":file_id}},"flag":6}, ensure_ascii=False)
        yield json.dumps({"answer": {"msg":'结束'},"flag":3}, ensure_ascii=False)

        
    generater=qa_generation_iterator()
    return EventSourceResponse(generater)


@generation_app.get("/generation/qa_score/{qa_box_id}/{file_id}",description="问答数据评分")
def evalQAScore(
    qa_box_id:str=Path(...,description="对话唯一id"),
    file_id:str=Path(...,description="文件唯一id")
)->BaseResponse:
    qa_every_score,average=get_qa_result_file_score(qa_box_id=qa_box_id,file_id=file_id)
    if average==-1:
        return BaseResponse(code=500,msg="qa_box_id 为空")
    if average==-2:
        return BaseResponse(code=500,msg=f"qa_box_id:{qa_box_id}对话未生成问答对")
    if average==-3:
        return BaseResponse(code=500,msg=f"评分服务异常")
    print(qa_every_score,average)
    return BaseResponse(code=200,msg="success",data={
        "qa_every_score":qa_every_score,
        "average":average
    })
    
