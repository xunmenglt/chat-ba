# -*- coding:UTF-8 -*-
# @Time : 2024/3/10 11:34
# @Author : 寻梦
# @File : test_fast_controller
# @Project : langchain-ChatBA
import argparse
import datetime
import os.path
import subprocess
import threading
import time
from .fastchat_utils import get_best_gpu,get_fastchat_controller,get_worker_address
from server.embedding.pool.embeding_pool import CachePool
from configs import (logger,
                     FSCHAT_CONTROLLER,
                     FSCHAT_OPENAI_API,
                     LLM_MODELS,
                     ONLINE_LLM_MODEL,
                     MODEL_PATH,
                     MODEL_ROOT_PATH,
                     FSCHAT_MODEL_WORKERS)
fast_thread_map=CachePool()




def run_controller():
    # 获取contoller配置
    host=FSCHAT_CONTROLLER["host"]
    port=FSCHAT_CONTROLLER["port"]
    dispatch_method=FSCHAT_CONTROLLER["dispatch_method"]
    subprocess.run(["python", "-m",
                    "fastchat.serve.controller",
                    "--host", host,
                    "--port",str(port),
                    "--dispatch-method",dispatch_method])

def run_api_server():
    # 获取fast_api第三方服务
    host=FSCHAT_OPENAI_API["host"]
    port=FSCHAT_OPENAI_API["port"]
    subprocess.run(["python", "-m",
                    "fastchat.serve.openai_api_server",
                    "--host",host,
                    "--controller-address",get_fastchat_controller(),
                    "--port", str(port)])


def run_model_worker(model_name):
    model_path = os.path.join(MODEL_ROOT_PATH, MODEL_PATH["llm_model"][model_name])
    host=FSCHAT_MODEL_WORKERS[model_name]["host"]
    port=FSCHAT_MODEL_WORKERS[model_name]["port"]
    load_8bit=FSCHAT_MODEL_WORKERS[model_name]["load_8bit"]
    gpu=get_best_gpu()
    if gpu is None:
        raise RuntimeError("run model need gpus !")

    args=[
            "python", "-m",
            "fastchat.serve.model_worker",
            "--host", host,
            "--port",str(port),
            "--worker-address",get_worker_address(model_name),
            "--controller-address", get_fastchat_controller(),
            "--model-path", model_path,
        ]
    if load_8bit:
        args.append("--load-8bit")
    if FSCHAT_MODEL_WORKERS[model_name].get("num_gpus"):
        num_gpus=FSCHAT_MODEL_WORKERS[model_name].get("num_gpus")
        args.append("--num-gpus")
        args.append(str(num_gpus))
    if FSCHAT_MODEL_WORKERS[model_name].get("gpus"):
        args.append("--gpus")
        args.append(FSCHAT_MODEL_WORKERS[model_name].get("gpus"))
    if FSCHAT_MODEL_WORKERS[model_name].get("conv_template"):
        args.append("--conv-template")
        args.append(FSCHAT_MODEL_WORKERS[model_name].get("conv_template"))

    subprocess.run(args,env={'CUDA_VISIBLE_DEVICES': '1'})

def init_config_model():
    # 获取初始化模型列表
    print("需要加载的模型:",LLM_MODELS)
    for model_name in LLM_MODELS:
        # 判断当前模型是否是在线模型
        if model_name in ONLINE_LLM_MODEL.keys():
            continue
        # 判断当前模型是否是本地模型
        if model_name not in MODEL_PATH["llm_model"].keys():
            logger.info(f"模型 {model_name} 没有进行配置")
            continue
        if fast_thread_map.get(model_name) is None:
            model_worker_thread=threading.Thread(target=run_model_worker,args=(model_name,))
            model_worker_thread.start()
            fast_thread_map.set(model_name,model_worker_thread)
            time.sleep(30)




# to run
def run_fastchat():
    # 启动 controller
    controller_thread=threading.Thread(target=run_controller)
    controller_thread.start()
    logger.info("fast controller is loading...")
    # 等待api服务启动
    time.sleep(10)
    logger.info("fast controller is success")
    fast_thread_map.set("fast_controller",controller_thread)
    # 启动api服务
    logger.info("fast api server is loading...")
    api_server_thread=threading.Thread(target=run_api_server)
    api_server_thread.start()
    logger.info("fast api server is success")
    fast_thread_map.set("fast_api_server", api_server_thread)
    print("====================开始加载LLM模型========================")
    print(LLM_MODELS)
    time.sleep(10)
    init_config_model()



if __name__=="__main__":
    print("开始启动controller",datetime.datetime.now())
    controller_thread = threading.Thread(target=run_controller)
    controller_thread.start()
    # controller_thread.join()
    print("controller启动完成", datetime.datetime.now())

    time.sleep(10)
    print("开始启动model_worker", datetime.datetime.now())
    model_worker_thread = threading.Thread(target=run_model_worker)
    model_worker_thread.start()
    # controller_thread.join()
    print("model_worker启动完成", datetime.datetime.now())

    time.sleep(10)
    print("开始启动api_server", datetime.datetime.now())
    api_server_thread = threading.Thread(target=run_api_server)
    api_server_thread.start()
    # controller_thread.join()
    print("api_server启动完成", datetime.datetime.now())
