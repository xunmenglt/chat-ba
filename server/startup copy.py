# -*- coding:UTF-8 -*-
# @Time : 2024/8/23 21:17
# @Author : 寻梦
# @File : startup
# @Project : ChatBA
import os
import sys
import asyncio
import multiprocessing
from multiprocessing import Process



from configs import (LLM_MODELS)
from server.utils import (get_model_worker_config)


def run_model_worker(
        model_name: str = LLM_MODELS[0],
        controller_address: str = "",
        log_level: str = "INFO",
        q: multiprocessing.Queue = None,
        started_event: multiprocessing.Event = None,
):  
    import random
    os.environ["CUDA_VISIBLE_DEVICES"] = str(random.randint(0,7))
    import torch
    x=torch.arange(1*1024*1024*1024)
    x.to(torch.cuda.current_device())
    started_event.set()
    import time
    while True:
        time.sleep(0.5)


async def start_main_server():
    import time
    multiprocessing.set_start_method("spawn")
    manager = multiprocessing.Manager()

    queue = manager.Queue()

    processes = {"online_api": {}, "model_worker": {}}


    model_worker_started = []
    for model_name in range(2):
        model_name=str(model_name)
        e=multiprocessing.Event()
        model_worker_started.append(e)
        process = Process(
            target=run_model_worker,
            name=f"model_worker - {model_name}",
            kwargs=dict(model_name=model_name,
                        # controller_address=args.controller_address,
                        log_level="info",
                        q=queue,
                        started_event=e),
            daemon=True,
        )
        processes["model_worker"][model_name] = process

    for model_name, p in processes.get("model_worker", {}).items():
        p.start()
        p.name = f"{p.name} ({p.pid})"
    

    # 等待所有model_worker启动完成
    for e in model_worker_started:
        e.wait()
    while True:
        time.sleep(0.5)


if __name__ == "__main__":
    if sys.version_info < (3, 10):
        loop = asyncio.get_event_loop()
    else:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()

        asyncio.set_event_loop(loop)
    loop.run_until_complete(start_main_server())