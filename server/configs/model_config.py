# -*- coding:UTF-8 -*-
# @Time : 2024/3/6 14:12
# @Author : 寻梦
# @File : model_config
# @Project : langchain-ChatBA
import os
from typing import Dict

# 可以指定一个绝对路径，统一存放所有的Embedding和LLM模型。
# 每个模型可以是一个单独的目录，也可以是某个目录下的二级子目录。
# 如果模型目录名称和 MODEL_PATH 中的 key 或 value 相同，程序会自动检测加载，无需修改 MODEL_PATH 中的路径。
# TODO
MODEL_ROOT_PATH = "/opt/data/private/liuteng/model"
# MODEL_ROOT_PATH = "/data/zzk/liuteng/model"

# 选用的 Embedding 名称
EMBEDDING_MODEL = "bge-large-zh"

# Embedding 模型运行设备。设为 "auto" 会自动检测(会有警告)，也可手动设定为 "cuda","mps","cpu","xpu" 其中之一。
EMBEDDING_DEVICE = "auto"

# 选用的reranker模型
RERANKER_MODEL = "bge-reranker-large"
# 是否启用reranker模型
USE_RERANKER = False
RERANKER_MAX_LENGTH = 1024

# 如果需要在 EMBEDDING_MODEL 中增加自定义的关键字时配置
EMBEDDING_KEYWORD_FILE = "keywords.txt"
EMBEDDING_MODEL_OUTPUT_PATH = "output"

# 要运行的 LLM 名称，可以包括本地模型和在线模型。列表中本地模型将在启动项目时全部加载。
# 列表中第一个模型将作为 API 和 WEBUI 的默认模型。
# 在这里，我们使用目前主流的两个离线模型，其中，chatglm3-6b 为默认加载模型。
# 如果你的显存不足，可使用 Qwen-1_8B-Chat, 该模型 FP16 仅需 3.8G显存。

# LLM_MODELS = ["chatglm3-6b", "zhipu-api", "openai-api"]
# LLM_MODELS=["qianfan-api","Llama2-Chinese-7b-Chat-xunmeng","OpenBT5-Flan"]
# LLM_MODELS=["Baichuan2-13B-Chat"]


LLM_MODELS=[
            # "openba2-3b-RCB-QA",
            # "openba2-3b-RCB-Chat",
            # "openba2-3b-RCB-Chat-v2",
            # "chatglm3-6b-RCB-QA",
            # "chatglm3-6b-RCB-Chat",
            # "chatglm3-6b",
            # "Qwen1.5-7B-Chat",
            # "Qwen2-7B-Instruct@1",
            # "Qwen2-7B-Instruct@2",
            # "Qwen2-7B-Instruct@3",
            # "qianfan-api",
            # "gpt-3.5-turbo",
            # "gpt-4-turbo",
            # "CodeLlama-7b-hf",
            # "CodeQwen1.5-7B",
            # "CodeQwen1.5-7B-Chat",
            # "ge-bert",
            # "OpenBA-V2-Chat",
            # "ge-bert-mask",
            "moonshot-v1-8k",
            # "Qwen2-7B-Instruct"
            "Qwen2-0.5B-Instruct"
            # "qwen-plus"
            ]

Agent_MODEL = None

# LLM 模型运行设备。设为"auto"会自动检测(会有警告)，也可手动设定为 "cuda","mps","cpu","xpu" 其中之一。
LLM_DEVICE = "auto"

HISTORY_LEN = 3

MAX_TOKENS = 1024

TEMPERATURE = 0.7

ONLINE_EMBED_MODEL={
#    "bge-large-zh":{
#        "qianfan_ak":"6WLyxot4mslYMO7xpOxWjGe6",
#        "qianfan_sk":"G4o5ZTRc8MzUnztqPnSymQsDj4kh5ZKx",
#        "model":"bge-large-zh"
#    }
}

ONLINE_LLM_MODEL = {
    "qianfan-api": {
        "version": "ERNIE-Bot-turbo",  # 注意大小写。当前支持 "ERNIE-Bot" 或 "ERNIE-Bot-turbo"， 更多的见官方文档。
        "qianfan_ak": "6WLyxot4mslYMO7xpOxWjGe6",
        "qianfan_sk": "G4o5ZTRc8MzUnztqPnSymQsDj4kh5ZKx",
        "provider": "QianFanWorker",
    },
    "gpt-3.5-turbo":{
        "openai_api_key":"sk-nzow4TIOo6wZv2hQBf903e1e7eDb496b832cCa242fD58f81",
        "openai_api_base":"https://chatapi.onechats.top/v1",
    },
    "gpt-4-turbo":{
        "openai_api_key":"sk-nzow4TIOo6wZv2hQBf903e1e7eDb496b832cCa242fD58f81",
        "openai_api_base":"https://chatapi.onechats.top/v1",
    },
    "ge-bert":{
        "api_key":"opennlg-openaiapi-keys",
        "api_base_url":"http://localhost:6888/v1",
        "online_api":True,
        "provider":"GeBertModelWorker"
    },
    "ge-bert-mask":{
        "api_key":"opennlg-openaiapi-keys",
        "api_base_url":"http://localhost:6999/v1",
        "online_api":True,
        "provider":"GeBertModelWorker"
    },
    "moonshot-v1-8k":{
        "api_key":"sk-GxERcpc41AeExR7EK9zXPdZHF8fYh9KuR2fEYlfwwuSuStze",
        "api_base_url":"https://api.moonshot.cn/v1",
        "online_api":True,
        "provider":"GeBertModelWorker"
    },
    "qwen-plus":{
        "api_key":"sk-d5cf551d62f74e2497aa5642dbadeae5",
        "api_base_url":"http://113.44.78.192/v1",
        "online_api":True,
        "provider":"GeBertModelWorker"
    },
}

MODEL_PATH = {
    "embed_model": {
        "bge-large-zh": "BAAI/bge-large-zh",
        "bge-large-zh-v1.5":"BAAI/bge-large-zh-v1.5"
    },

    "llm_model": {
        "Baichuan2-13B-Chat-4bits":"Baichuan2-13B-Chat-4bits",
        "Baichuan2-13B-Chat-8bit":"Baichuan2-13B-Chat-8bit",
        "Baichuan2-13B-Chat": "Baichuan2-13B-Chat",
        "Llama2-Chinese-7b-Chat-xunmeng": "Llama2-Chinese-7b-Chat-xunmeng",
        "OpenBT5-Flan": "OpenBT5-Flan",
        "OpenBA-LM":"OpenBA-LM",
        "chat_v5.1_4.8k_hf":"chat_v5.1_4.8k_hf",
        "OpenBA-V2-Chat":"OpenNLG/OpenBA-V2-Chat",
        "chatglm-6b-ft":"chatglm-6b-ft",
        "chatglm3-6b":"chatglm3-6b",
        "checkpoint-1440":"checkpoint-1440",
        "openba2-3b-RCB-QA":"RCB/openba2-3b-RCB-QA",
        "openba2-3b-RCB-Chat":"RCB/openba2-3b-RCB-Chat",
        "openba2-3b-RCB-Chat-v2":"RCB/openba2-3b-RCB-Chat-v2",
        "chatglm3-6b-RCB-QA":"RCB/chatglm3-6b-RCB-QA",
        "chatglm3-6b-RCB-Chat":"RCB/chatglm3-6b-RCB-Chat",
        "Qwen1.5-7B-Chat":"Qwen/Qwen1.5-7B-Chat",
        "Qwen2-7B-Instruct":"Qwen/Qwen2-7B-Instruct",
        "Qwen2-0.5B-Instruct":"Qwen/Qwen2-0.5B-Instruct",
        "Qwen2-7B-Instruct@1":"Qwen/Qwen2-7B-Instruct",
        "Qwen2-7B-Instruct@2":"Qwen/Qwen2-7B-Instruct",
        "Qwen2-7B-Instruct@3":"Qwen/Qwen2-7B-Instruct",
        "Qwen-72B-Chat-Int4":"Qwen-72B-Chat-Int4",
        "CodeQwen1.5-7B":"Qwen/CodeQwen1.5-7B",
        "CodeQwen1.5-7B-Chat":"Qwen/CodeQwen1.5-7B-Chat",
        "CodeLlama-7b-hf":"codellama/CodeLlama-7b-hf"
    }
}

# 通常情况下不需要更改以下内容

# nltk 模型存储路径
NLTK_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "nltk_data")

