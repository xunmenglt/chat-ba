from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage

# prompt_template = ChatPromptTemplate.from_messages([
#     ("system", "You are a helpful assistant"),
#     MessagesPlaceholder("msgs")
# ])

# print(prompt_template.invoke({"msgs": [HumanMessage(content="hi!")]}).to_string())

prompt=ChatPromptTemplate.from_messages(
            [("user","请参照文本{{context}}")],
            template_format="mustache"
)