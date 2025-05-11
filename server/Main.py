import os
import multiprocessing
from multiprocessing import Process
import time
import sys
import torch
import asyncio


def run_on_gpu(gpu,event:multiprocessing.Event):
    os.environ["CUDA_VISIBLE_DEVICES"]=gpu
    print("当前cuda编号",torch.cuda.current_device())
    x=torch.arange(1*1024*1024*1024)
    y=torch.tensor(x)
    y.to(torch.cuda.current_device())
    event.set()
    while True:
        time.sleep(1)


async def loop_main():
    import signal

    def handler(signalname):
        def f(signal_received, frame):
            raise KeyboardInterrupt(f"{signalname} received")

        return f

    signal.signal(signal.SIGINT, handler("SIGINT"))
    signal.signal(signal.SIGTERM, handler("SIGTERM"))
    multiprocessing.set_start_method("spawn")
    
    manager = multiprocessing.Manager()
    worker_started=[]
    for gpu in range(2):
        e = manager.Event()
        worker_started.append(e)
        p=Process(
            target=run_on_gpu,
            kwargs=dict(gpu=str(gpu),event=e),
            daemon=True,
        )
        p.start()
    for worker in worker_started:
        worker.wait()
    while True:
        print("进程正在执行...")
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
    loop.run_until_complete(loop_main())