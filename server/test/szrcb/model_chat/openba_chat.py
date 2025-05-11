import json
import tqdm
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    # HfArgumentParser,
)

model_path="/public/home/ljt/dyy/OpenBA-v2-chat/output/openba-v1-chat-adaptation-02/checkpoint-732"
tokenizer=AutoTokenizer.from_pretrained(model_path,trust_remote_code=True)
model=AutoModelForSeq2SeqLM.from_pretrained(model_path, trust_remote_code=True).half().cuda()
model.eval()

def chat(model,tokenizer,prompt,temperature=0.2,top_p=0.9,max_tokens=512):
    inputs = tokenizer(prompt, return_tensors='pt')
    for k in inputs:
        inputs[k] = inputs[k].cuda()
    outputs = model.generate(
                **inputs,
                do_sample=True,
                max_new_tokens=max_tokens,
                temperature = temperature,
                top_p =top_p)
    return outputs

def create_message(messages):
    if not messages:
        messages=[]
    prompt=""
    for message in messages:
        role=message[0]
        if role not in ("Human","Assistant"):
            raise ValueError(f"错误的角色输入：{role}")
        prompt=f"{role}: {message[1]} </s> "
    prompt=prompt+"Assistant: "
    return "<S> "+prompt+" <extra_id_0>"




def call_with_prompt(query):
    messages=[("Human",query)]
    prompt=create_message(messages)
    response = chat(model=model,tokenizer=tokenizer,prompt=prompt)
    return response

def parse_response_to_answer(response):
    return tokenizer.decode(response[0], skip_special_tokens=True)

def create_model_qa_data(old_file,new_file):
    nf=open(new_file,'w',encoding="utf-8")
    with open(old_file,'r',encoding="utf-8") as fp:
        contents=fp.readlines()
        for content in tqdm.tqdm(contents):
            json_data=json.loads(content)
            query=json_data[input_key]
            try:
                output=parse_response_to_answer(call_with_prompt(query))
                print("Human：",query)
                print("---------------------------------")
                print("OpenBA：",output)
                print("=================================")
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
    # while True:
    #     query=input("Human：")
    #     print('---------------------------------')
    #     answer=parse_response_to_answer(call_with_prompt(query))
    #     print("OpenBA：",answer)
    #     print('=================================')
    input_key="input"
    output_key="output"
    # 对话数据
    old_file='/public/home/ljt/liuteng/model_chat/data/evaluation_v2/gpt4_verification_dialog_data.jsonl'
    new_file='/public/home/ljt/liuteng/model_chat/data/evaluation_v2/openba_ft_2_verification_dialog_data.jsonl'
    create_model_qa_data(old_file,new_file)
    # # 问答对生成数据
    # old_file='/public/home/ljt/liuteng/model_chat/data/gpt4_verification_qa_creation_data.jsonl'
    # new_file='/public/home/ljt/liuteng/model_chat/data/evaluation/openba_ft_verification_qa_creation_data.jsonl'
    # create_model_qa_data(old_file,new_file)