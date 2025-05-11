import asyncio
import threading
import time
import uvicorn
import torch
import json
from typing import List
from fastapi import FastAPI, Request, BackgroundTasks,Body
from typing import List,Any
from fastapi.responses import StreamingResponse,JSONResponse
import requests
from fastchat.conversation import get_conv_template
from fastapi.middleware.cors import CORSMiddleware
from fastchat.serve.inference import generate_stream
from fastchat.constants import WORKER_HEART_BEAT_INTERVAL
from fastchat.conversation import Conversation
from fastchat.utils import pretty_print_semaphore, build_logger
from transformers import AutoTokenizer,AutoModelForCausalLM
model_path="/opt/data/private/liuteng/model/Qwen/CodeQwen1.5-7B-Chat"
tokenizer = AutoTokenizer.from_pretrained(model_path,trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_path,trust_remote_code=True,device_map="auto").eval()


limit_worker_concurrency=2
semaphore=asyncio.Semaphore(limit_worker_concurrency)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许访问的源
    allow_credentials=True,  # 支持 cookie
    allow_methods=["*"],  # 允许使用的请求方法
    allow_headers=["*"]  # 允许携带的 Headers
)


def heart_beat_worker(obj):
    while True:
        time.sleep(WORKER_HEART_BEAT_INTERVAL)
        obj.send_heart_beat()



def create_background_tasks():
    background_tasks = BackgroundTasks()
    background_tasks.add_task(release_worker_semaphore)
    return background_tasks




def release_worker_semaphore():
    print(f"-----------释放成功---------------")
    semaphore.release()


def acquire_worker_semaphore():
    return semaphore.acquire()


def create_background_tasks():
    background_tasks = BackgroundTasks()
    background_tasks.add_task(release_worker_semaphore)
    return background_tasks

def generate_stream_gate(prompt):
    try:
        for output in generate_stream(
            model=model,
            tokenizer=tokenizer,
            params={
                'model': 'CodeQwen1.5-7B-Chat',
                'prompt': prompt,
                'temperature': 0.75,
                'top_p': 1.0,
                'top_k': -1,
                'presence_penalty': 0.0,
                'frequency_penalty': 0.0,
                'max_new_tokens': 512,
                'echo': False,
                'stop_token_ids': [151643, 151644, 151645],
                'stop': ['<|endoftext|>']
            },
            device="cuda:0",
            context_len=1024,
            stream_interval=2,
        ):
            ret = {
                "content": output["text"],
                "error_code": 0,
            }
            if "usage" in output:
                ret["usage"] = output["usage"]
            if "finish_reason" in output:
                ret["finish_reason"] = output["finish_reason"]
            if "logprobs" in output:
                ret["logprobs"] = output["logprobs"]
            yield json.dumps(ret,ensure_ascii=False).encode() + b"\r\n"
    except torch.cuda.OutOfMemoryError as e:
        ret = {
            "text": f"服务异常\n\n({e})",
            "error_code": 100,
        }
        print(ret)
        yield json.dumps(ret,ensure_ascii=False).encode() + b"\0"
    except (ValueError, RuntimeError) as e:
        ret = {
            "text": f"服务异常\n\n({e})",
            "error_code": 200,
        }
        print(ret)
        yield json.dumps(ret,ensure_ascii=False).encode() + b"\0"
    
count=1

@app.post("/worker_generate_stream")
async def api_generate_stream(
    prompt:Any=Body("写一个冒泡函数",description="输入",alias="input"),
    max_tokens:int=Body(512,description="最大输出")
):
    conv=get_conv_template("qwen-7b-chat")
    conv.append_message("user",prompt)
    prompt=conv.get_prompt()
    await acquire_worker_semaphore()
    generator=generate_stream_gate(prompt)
    background_tasks=create_background_tasks()
    return StreamingResponse(generator,background=background_tasks)

@app.get("/api_one")
async def apione(
):
    return JSONResponse({"code":200,"msg":"api_one"})

@app.get("/api_two")
def apitwo(
):
    return JSONResponse({"code":200,"msg":"api_two"})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7888, log_level="info")