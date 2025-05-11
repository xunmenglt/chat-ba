import json
import tqdm
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    # HfArgumentParser,
)

model_path="/opt/data/private/liuteng/model/Qwen/Qwen2-7B-Instruct"
tokenizer=AutoTokenizer.from_pretrained(model_path,trust_remote_code=True)
model=AutoModelForCausalLM.from_pretrained(model_path, trust_remote_code=True,device_map="auto").half()
model.eval()

def chat(model,tokenizer,prompt,temperature=0.7,top_p=0.9,max_tokens=512):
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

def create_message(messages,tokenizer):
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    return text

def call_with_prompt(query):
    messages = [
        {"role": "user", "content": query}
    ]
    prompt=create_message(messages,tokenizer)
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
            except Exception as e:
                print(e)
                continue
            new_data={
                "input":query,
                "output":output.split("assistant\n")[-1],
                "index":json_data["index"]
            }
            nf.write(json.dumps(new_data,ensure_ascii=False)+"\n")
    nf.close()

if __name__=="__main__":
    while True:
        query=input("Human：")
        print('---------------------------------')
        answer=parse_response_to_answer(call_with_prompt(query))
        print("QWen：",answer)
        print('=================================')
    input_key="input"
    output_key="output"
    # 对话数据
    # old_file='/public/home/ljt/liuteng/model_chat/data/evaluation_v2/gpt4_verification_dialog_data.jsonl'
    # new_file='/public/home/ljt/liuteng/model_chat/data/evaluation_v2/qianwen7b_verification_dialog_data.jsonl'
    # create_model_qa_data(old_file,new_file)
    # 问答对生成数据
    # old_file='/public/home/ljt/liuteng/model_chat/data/gpt4_verification_qa_creation_data.jsonl'
    # new_file='/public/home/ljt/liuteng/model_chat/data/evaluation/qianwen7b_verification_qa_creation_data.jsonl'
    # create_model_qa_data(old_file,new_file)

