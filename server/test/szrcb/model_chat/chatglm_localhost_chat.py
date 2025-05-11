import json
import tqdm
from transformers import (
    AutoTokenizer,
    AutoModel,
    # HfArgumentParser,
)

model_path="/opt/data/private/liuteng/model/THUDM/glm-4-9b-chat"
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
model = AutoModel.from_pretrained(model_path,trust_remote_code=True).half().cuda()
model.eval()

def chat(model,tokenizer,prompt,temperature=0.5,top_p=0.9,max_tokens=512):
    response, history = model.chat(tokenizer,prompt,max_length=max_tokens,top_p=top_p,temperature=temperature)
    return response


def create_message(messages):
    return messages

def call_with_prompt(query):
    messages = query
    prompt=create_message(messages)
    response = chat(model=model,tokenizer=tokenizer,prompt=prompt)
    return response

def parse_response_to_answer(response):
    return response

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

if __name__=="__main__":
    while True:
        query=input("Human：")
        print('---------------------------------')
        answer=call_with_prompt(query)
        print("ChatGLM：",answer)
        print('=================================')
    # input_key="input"
    # output_key="output"
    # # 对话数据
    # old_file='/public/home/ljt/liuteng/model_chat/data/evaluation_v2/gpt4_verification_dialog_data.jsonl'
    # new_file='/public/home/ljt/liuteng/model_chat/data/evaluation_v2/chatglm_verification_dialog_data.jsonl'
    # create_model_qa_data(old_file,new_file)
    # # # 问答对生成数据
    # old_file='/public/home/ljt/liuteng/model_chat/data/gpt4_verification_qa_creation_data.jsonl'
    # new_file='/public/home/ljt/liuteng/model_chat/data/evaluation/chatglm_ft_verification_qa_creation_data.jsonl'
    # create_model_qa_data(old_file,new_file)

