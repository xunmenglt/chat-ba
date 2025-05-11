import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from langchain.prompts import ChatPromptTemplate
import numpy as np
from tqdm import tqdm
import os
import openai
import time
import re
import ast
from configs import openai_api_base,openai_api_key
from pool.model_pool import model_pool
from langchain_core.output_parsers import StrOutputParser
from typing import Union



def to_qwen_messages():
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system","你是一个公正的评委。"),
            ("user","[指令]\n请担任公正的评委，评估AI助手对下列用户问题所提供的回复的质量。你的评估应考虑回复的简洁性和准确性。开始评估时请提供一个简短的解释。尽量保持客观。在作出解释后，你必须严格按照以下格式在1到10分的范围内对回复进行评分：\"[[得分]]\",例如:\"得分:[[5]]\".\n\n[问题]\n{{question}}\n\n[助手答案开始]\n{{answer}}\n[助手答案结束]")
        ],
        template_format="mustache"
    )
    return prompt


def gpt_chat(qa):
    openai.api_base = openai_api_base
    openai.api_key = openai_api_key
    messages = to_openai_api_messages(qa)
    response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=messages,
                    n=1,
                    temperature=0,
                    max_tokens=2048,
    )
    output = response["choices"][0]["message"]["content"]
    return output

def qwen_chat(qa):
    question = qa['question']
    answer = qa['answer']
    messagesPrompt = to_qwen_messages()
    model,real_model_name = model_pool.load_model(
            model_name="Qwen2-7B-Instruct",
            temperature=0.2,
            top_p=0.95,
            max_tokens=2048,
            callbacks=[],
            streaming=False,
            auto_release_model=True
    )
    chain = messagesPrompt | model | StrOutputParser()
    model_output=chain.invoke({"question":question,"answer":answer})
    print(model_output)
    print("=======================================")
    return model_output





# os.environ["OPENAI_API_KEY"] = "sk-nzow4TIOo6wZv2hQBf903e1e7eDb496b832cCa242fD58f81"
# os.environ["OPENAI_API_BASE"] = "https://chatapi.onechats.top/v1"
# API_MAX_RETRY = 16
# API_RETRY_SLEEP = 10
# API_ERROR_OUTPUT = "$ERROR$"

def to_openai_api_messages(qa):
    """Convert the conversation to OpenAI chat completion format."""
    question = qa['question']
    answer = qa['answer']
    msg = "[指令]\n请担任公正的评委，评估AI助手对下列用户问题所提供的回复的质量。你的评估应考虑回复的简洁性和准确性。开始评估时请提供一个简短的解释。尽量保持客观。在作出解释后，你必须严格按照以下格式在1到10分的范围内对回复进行评分：\"[[得分]]\",例如:\"得分:[[5]]\".\n\n[问题]\n{question}\n\n[助手答案开始]\n{answer}\n[助手答案结束]".format(question=question, answer=answer)
    ret = [{"role": "system", "content": "你是一个乐于助人的助手。"}]
    ret.append({"role": "user", "content": msg})
    return ret
def eval_qa_quality(model_type:Union["gpt","qwen"]='gpt',qa_list=[]):
    output = "$ERROR$" # API_ERROR_OUTPUT
    rating_list = []
    for qa in qa_list:
        for _ in range(16): # API_MAX_RETRY
            try:
                if model_type=='gpt':
                    output=gpt_chat(qa)
                elif model_type=='qwen':
                    output=qwen_chat(qa)
                else:
                    raise ModuleNotFoundError("模型不存在，目前支持gpt、qwen")
                break
            except openai.error.OpenAIError as e:
                print(type(e), e)
                time.sleep(10) # API_RETRY_SLEEP = 10
        ### 抽取评分
        one_score_pattern = re.compile("\[\[(\d+\.?\d*)\]\]")
        one_score_pattern_backup = re.compile("\[(\d+\.?\d*)\]")
        match = re.search(one_score_pattern, output)
        if not match:
            match = re.search(one_score_pattern_backup, output)
        if match:
            rating = ast.literal_eval(match.groups()[0])
        else:
            rating = -1
        rating_list.append(rating)
    average = sum(rating_list) / len(rating_list)
    return rating_list, average

def eval_muti_qa_quality(model_type:Union["gpt","qwen"]='gpt',messages=[]):
    output = "$ERROR$" # API_ERROR_OUTPUT
    for _ in range(16): # API_MAX_RETRY
        try:
            tempPrompt="[指令]\n请担任公正的评委，评估下列AI助手与用户进行多轮对话回复内容的质量。你的评估应考虑回复的简洁性和准确性。开始评估时请提供一个简短的解释。尽量保持客观。在作出解释后，你必须严格按照以下格式在1到10分的范围内对回复进行评分：\"[[得分]]\",例如:\"得分:[[5]]\".\n\n[对话内容开始]"
            for message in messages:
                role=message.get('role') if message.get('role') else 'user'
                if role=='user':
                    tempPrompt+="\n\n用户：\n{content}".format(content=message['content'])
                else:
                    tempPrompt+="\nAI助手：\n{content}".format(content=message['content'])
            msg = tempPrompt+"\n\n[对话内容结束]"
            ret = [{"role": "system", "content": "你是一个乐于助人的助手。"}]
            ret.append({"role": "user", "content": msg})
            openai.api_base = openai_api_base
            openai.api_key = openai_api_key
            messages = ret
            response = openai.ChatCompletion.create(
                            model="gpt-4",
                            messages=messages,
                            n=1,
                            temperature=0,
                            max_tokens=2048,
            )
            output = response["choices"][0]["message"]["content"]
            break
        except openai.error.OpenAIError as e:
            print(type(e), e)
            time.sleep(10) # API_RETRY_SLEEP = 10
    ### 抽取评分
    one_score_pattern = re.compile("\[\[(\d+\.?\d*)\]\]")
    one_score_pattern_backup = re.compile("\[(\d+\.?\d*)\]")
    match = re.search(one_score_pattern, output)
    if not match:
        match = re.search(one_score_pattern_backup, output)
    if match:
        rating = ast.literal_eval(match.groups()[0])
    else:
        rating = -1
    return rating

if __name__ == '__main__':
    qa_list = [
        {
            "role": "user",
            "content":"你是谁?"
        },
        {
            "role":"ai",
            "content":"我是人"
        },
        {
            "role":"user",
            "content":"中午吃的什么"
        },
        {
            "role":"ai",
            "content":"晚上去钓鱼"
        }
    ]
    rating = eval_muti_qa_quality(messages=qa_list)
    print(rating)