# -*- coding:UTF-8 -*-
# @Time : 2024/3/9 18:23
# @Author : 寻梦
# @File : history_test
# @Project : langchain-ChatBA


from langchain.prompts import ChatPromptTemplate,ChatMessagePromptTemplate
from langchain_core.messages import HumanMessage,AIMessage
from langchain.memory import ChatMessageHistory

prompt=ChatPromptTemplate.from_template(
    '''请参考下面的历史对话，来回答我的问题。其中历史对话开始符号为<history>，结束符号为</history>。问题标志符为question。
    
<history>
    
{history}
    
</history>
    
    
question:{query}'''
)

print(prompt.invoke({"history":"a","query":"v"}).to_string())


from transformers import AutoTokenizer, AutoModel
model = AutoModel.from_pretrained()
model.stream_chat()