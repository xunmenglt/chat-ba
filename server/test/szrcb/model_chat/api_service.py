import json
import requests
import os
import openai
import time
import numpy as np
import time
import vthread
import re
from tqdm import tqdm

openai.api_key ="sk-sX1tRx7XMWsb9kU7C858F72aF7Fe41F7893f66Ad8aAe64E9"
openai.api_base='https://chatapi.onechats.top/v1'
class API():
    def __init__(self,wait_time):
        self.wait_time=wait_time
        pass

    def calling(self,inputs,output_path,freq_per_second,model_name):
        temp_path="/".join(output_path.split("/")[:-1]+["temp"]+[output_path.split("/")[-1]])
        temp_fout=open(temp_path,"w",encoding="utf-8")
        for i,t in enumerate(tqdm(inputs)):
            self.api_get_tokens(t,model_name,temp_fout,i)
            time.sleep(1/freq_per_second)
        start_time=time.time()
        target_num=len(inputs)*5
        while True:
            fin=open(temp_path,"r",encoding="utf-8")
            lines=fin.readlines()
            if target_num-len(lines)<0.02*target_num or time.time()-start_time>self.wait_time:
                print("done.",len(lines),time.time()-start_time)
                break
            else:
                time.sleep(1)
            fin.close()
        fout=open(output_path,"w",encoding="utf-8")
        eval_lines=[]
        for i,line in enumerate(lines):
            try:
                line=eval(line)
                eval_lines.append(line)
            except:
                continue
        sorted_lines=sorted(eval_lines, key=lambda d: d["index"])
        for line in sorted_lines:
            fout.write(self.dict_to_str(line).replace("\n","\\n")+"\n")
            fout.flush()
        fout.close()
        # os.remove(temp_path)
            
    def dict_to_str(self,d):
        items = []
        for k, v in d.items():
            # 对键和值进行处理
            key_str = f'"{k}"'
            if isinstance(v, str):
                value_str = f'"{v}"'
            else:
                value_str = str(v)
            items.append(f'{key_str}: {value_str}')
        return '{' + ', '.join(items) + '}'

    # @vthread.pool(500)
    def api_get_tokens(self,inputs,model_name,output_fout,index):
        while True:
            try:
                response = openai.ChatCompletion.create(
                                model=model_name,
                                messages=[
                                    # "role": "user", "content": "You will be given input, two outputs, and four choices. You need to judge the quality of two outputs based on the input and choose one of the choices as your response. Input: {} Output: 1. {}; 2.{} Choices: "
                                    #  "以下两个句子都是基于“为以下单词生成同义词。单词:快乐”得到的回答，请从流畅性、连贯性和相关性三个方面判断这两个回答哪个更好，输出结果只能包含：1. 句子1更好；2. 句子2更好；3. 两个句子都好。句子1：快乐的同义词:- 愉快的- 欢乐的- 欣喜的- 愉悦的- 开心的。句子2：愉快、愉快、欢乐、、欢乐、喜悦、喜悦、高兴、欢乐、欣喜、愉悦、快活。", 
                                    {"role": "system", "content": inputs["prompt"],
                                    # "role": "user", "content": "[Question]\n{}\n[Assistant 1]\n{}\n[End of Assistant 1]\n[Assistant 2]\n{}\n[End of Assistant 2]\n{}".format(src_c, tgt_chatmlm_c, tgt_other_c, system_content)
                                    }
                                ],
                                temperature=0,
                            )
                # print(inputs["prompt"])
                ans=response.choices[0].message.content.replace("\n","").split("\n")[0]
                # print(ans)
                pattern = re.compile(r"\{\s*'question':\s*'([^']+)',\s*'answer':\s*'([^']+)'\s*\}")
                matches = pattern.findall(ans)
                results = [{'question': question, 'answer': answer} for question, answer in matches]
                for result in results:
                    result["index"]=index
                    result["chapter_index"]=inputs["chapter_index"]
                    result["item_index"]=inputs["item_index"]
                    result["prompt"]=inputs["prompt"].replace("\n","\\n")
                    output_fout.write(self.dict_to_str(result)+"\n")
                    output_fout.flush()
                # return [(input + r['text']) for r, input in zip(response['choices'], input_texts)], [r['text'] for r in
                #                                                                                      response['choices']]
                break
            except Exception as e:
                print(e)
                # print(index,time.asctime( time.localtime(time.time()) ),e)
                time.sleep(2)
                continue