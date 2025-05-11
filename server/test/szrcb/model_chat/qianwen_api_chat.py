from http import HTTPStatus
import dashscope
from dashscope.api_entities.dashscope_response import GenerationResponse
import tqdm
import json
dashscope.save_api_key("sk-d5cf551d62f74e2497aa5642dbadeae5")
def call_with_prompt(query)->GenerationResponse:
    response = dashscope.Generation.call(
        model=dashscope.Generation.Models.qwen_turbo,
        prompt=query,
        max_tokens=2000
    )
    # 如果调用成功，则打印模型的输出
    if response.status_code == HTTPStatus.OK:
        return response
    # 如果调用失败，则打印出错误码与失败信息
    else:
        print(response.code)
        print(response.message)

def parse_response_to_answer(response:GenerationResponse):
    return response.output.text

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
    input_key="input"
    output_key="output"
    # 对话数据
    old_file='/public/home/ljt/liuteng/model_chat/data/evaluation_v2/gpt4_verification_dialog_data.jsonl'
    new_file='/public/home/ljt/liuteng/model_chat/data/evaluation_v2/qianwen_verification_dialog_data.jsonl'
    create_model_qa_data(old_file,new_file)
    # 问答对生成数据
    # old_file='/public/home/ljt/liuteng/model_chat/data/gpt4_verification_qa_creation_data.jsonl'
    # new_file='/public/home/ljt/liuteng/model_chat/data/evaluation/qianwen_verification_qa_creation_data.jsonl'
    # create_model_qa_data(old_file,new_file)
    