# -*- coding:UTF-8 -*-
# @Time : 2024/3/10 14:44
# @Author : 寻梦
# @File : fastchat_utils
# @Project : langchain-ChatBA

import subprocess
from configs import logger,FSCHAT_CONTROLLER,FSCHAT_OPENAI_API,FSCHAT_MODEL_WORKERS

def get_worker_address(model_name):
    if (not model_name) or (not FSCHAT_MODEL_WORKERS.get(model_name)) or (not FSCHAT_MODEL_WORKERS.get(model_name).get("port")):
        return "http://localhost:21002"
    args_model=FSCHAT_MODEL_WORKERS[model_name]
    return f"http://{args_model['host']}:{args_model['port']}"
    

def get_fastchat_controller():
    return f"http://{FSCHAT_CONTROLLER['host']}:{FSCHAT_CONTROLLER['port']}"

def get_faschat_server_open_api():
    return f"http://{FSCHAT_OPENAI_API['host']}:{FSCHAT_OPENAI_API['port']}/v1"
def get_gpu_status():
    # 运行nvidia-smi命令
    try:
        output = subprocess.check_output(['nvidia-smi', '--query-gpu=memory.free', '--format=csv,nounits,noheader'])
        # 将输出分割成单独的GPU状态
        gpu_free_memory = output.strip().decode('utf-8').split('\n')
        gpu_status = [int(x.strip()) for x in gpu_free_memory]
        return gpu_status
    except subprocess.CalledProcessError as e:
        print("Error querying GPU status: ", e.output)
        return None


def get_best_gpu():
    gpu_status=get_gpu_status()
    if gpu_status is None:
        return None
    gpus=[(idx,free_memory)for idx,free_memory in enumerate(gpu_status)]
    gpus=sorted(gpus,key=lambda x:-x[1])
    gpu=gpus[0]
    logger.info(f"当前选中的GPU编号为 {gpu[0]} ,GPU内存剩余 {gpu[1]} MB")
    return gpu
