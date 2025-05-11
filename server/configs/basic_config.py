# -*- coding:UTF-8 -*-
# @Time : 2024/3/6 14:04
# @Author : 寻梦
# @File : basic_config
# @Project : langchain-ChatBA


import logging
import os
import langchain
import tempfile
import shutil

HF_ENDPOINT="https://hf-mirror.com"
HF_HOME="/opt/data/private/liuteng/huggingface"
# openai_api_base = "https://dashscope.aliyuncs.com/compatible-mode/v1"
# openai_api_key = "sk-7f7dbba9a92f47059f8ff6d9bb58e889"
openai_api_base="https://api.moonshot.cn/v1"
openai_api_key="sk-GxERcpc41AeExR7EK9zXPdZHF8fYh9KuR2fEYlfwwuSuStze"

# 是否显示详细日志
log_verbose = False
langchain.verbose = False


# 通常情况下不需要更改以下内容

# 日志格式
LOG_FORMAT = "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s"
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig(format=LOG_FORMAT)

# 项目目录
PROJECT_DIR=os.path.dirname(os.path.dirname(__file__))
# 日志存储路径
LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
logger.log(logging.INFO,"当前日志文件路径：{}".format(LOG_PATH))


if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)

# 临时文件目录，主要用于文件对话
BASE_TEMP_DIR = os.path.join(tempfile.gettempdir(), "tmp_chat")
logger.log(logging.INFO,"当前聊天缓存目录：{}".format(BASE_TEMP_DIR))


try:
    shutil.rmtree(BASE_TEMP_DIR)
except Exception:
    pass
os.makedirs(BASE_TEMP_DIR, exist_ok=True)