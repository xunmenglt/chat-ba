import json
import os
import sys
import time
import pandas
from langchain_core.documents import Document
from typing import List
from unittest import result

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate
)

# 创建大模型，这里使用kimi
model=ChatOpenAI(
    model="moonshot-v1-128k",
    base_url="https://api.moonshot.cn/v1",
    api_key="sk-GxERcpc41AeExR7EK9zXPdZHF8fYh9KuR2fEYlfwwuSuStze"
)