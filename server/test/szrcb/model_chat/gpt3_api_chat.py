import openai
import json
import tqdm
# 设置API密钥
openai.api_key = 'sk-nzow4TIOo6wZv2hQBf903e1e7eDb496b832cCa242fD58f81'

# 将API请求的基础URL设置为不同的地址
openai.api_base = "https://chatapi.onechats.top/v1"
def call_with_prompt(query,model_name="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=[
            # "role": "user", "content": "You will be given input, two outputs, and four choices. You need to judge the quality of two outputs based on the input and choose one of the choices as your response. Input: {} Output: 1. {}; 2.{} Choices: "
            #  "以下两个句子都是基于“为以下单词生成同义词。单词:快乐”得到的回答，请从流畅性、连贯性和相关性三个方面判断这两个回答哪个更好，输出结果只能包含：1. 句子1更好；2. 句子2更好；3. 两个句子都好。句子1：快乐的同义词:- 愉快的- 欢乐的- 欣喜的- 愉悦的- 开心的。句子2：愉快、愉快、欢乐、、欢乐、喜悦、喜悦、高兴、欢乐、欣喜、愉悦、快活。", 
            {"role": "system", "content": query,
            # "role": "user", "content": "[Question]\n{}\n[Assistant 1]\n{}\n[End of Assistant 1]\n[Assistant 2]\n{}\n[End of Assistant 2]\n{}".format(src_c, tgt_chatmlm_c, tgt_other_c, system_content)
            }
        ],
        temperature=0,
    )
    return response

def parse_response_to_answer(response):
    return response.choices[0].message.content.strip()

def create_model_qa_data(old_file,new_file):
    nf=open(new_file,'w',encoding="utf-8")
    with open(old_file,'r',encoding="utf-8") as fp:
        contents=fp.readlines()
        for content in tqdm.tqdm(contents):
            json_data=json.loads(content)
            query=json_data[input_key]
            try:
                output=parse_response_to_answer(call_with_prompt(query))
            except Exception as e:
                print(e)
                continue
            new_data={
                "input":query,
                "output":output,
                "index":json_data["index"]
            }
            nf.write(json.dumps(new_data,ensure_ascii=False)+"\n")
    nf.close()

if __name__ == '__main__':
    while True:
        query=input("Human：")
        print('---------------------------------')
        answer=parse_response_to_answer(call_with_prompt(query))
        print("GPT3：",answer)
        print('=================================')
    # input_key="input"
    # output_key="output"
    # # 对话数据
    # old_file='/public/home/ljt/liuteng/model_chat/data/evaluation_v2/gpt4_verification_dialog_data.jsonl'
    # new_file='/public/home/ljt/liuteng/model_chat/data/evaluation_v2/gpt3_verification_dialog_data.jsonl'
    # create_model_qa_data(old_file,new_file)
    # # 问答对生成数据
    # old_file='/public/home/ljt/liuteng/model_chat/data/gpt4_verification_qa_creation_data.jsonl'
    # new_file='/public/home/ljt/liuteng/model_chat/data/evaluation/gpt3_verification_qa_creation_data.jsonl'
    # create_model_qa_data(old_file,new_file)