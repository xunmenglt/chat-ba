import openai
# 设置API密钥
openai.api_key = 'sk-nzow4TIOo6wZv2hQBf903e1e7eDb496b832cCa242fD58f81'
# 将API请求的基础URL设置为不同的地址
openai.api_base = "https://chatapi.onechats.top/v1"
response=openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role":"system","content":"你是一个知识渊博的AI助手。"},
            {"role": "user", "content": "中国四大发明有哪些？"}
    ],
    temperature=0.75,
    n=2,
    stream=True,
    stream_options={"include_usage": True}
)
# print(response.choices[0].message.content.strip())
for chunk in response:
    print(chunk)
print(response)

# response=openai.ChatCompletion.create(
#     model="gpt-3.5-turbo",
#     messages=[
#             {"role":"system","content":"你是一个知识渊博的AI助手。"},
#             {"role": "user", "content": "中国四大发明有哪些？"}
#     ],
#     stream=True,
#     temperature=0.75,
#     logprobs=True,
# )
# content=""
# for chunk in response:
#     delta = chunk.choices[0].delta
#     if "content" in delta.keys():
#         print(delta.content, end="", flush=True)
# print()