# -*- coding:UTF-8 -*-
# @Time : 2024/8/23 21:17
# @Author : 寻梦
# @File : startup
# @Project : ChatBA
import os
import sys
# 包环境路径覆盖
## 导入自定义的第三方工具包
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'lib'))
import subprocess
import asyncio
import multiprocessing
from multiprocessing import Process
import argparse
from datetime import datetime
from typing import List,Dict


# 获取cpu数量
try:
    num_cores=os.cpu_count()
except:
    num_cores=8
os.environ["NUMEXPR_MAX_THREADS"] = str(num_cores)

from configs import (LOG_PATH,logger,log_verbose,FSCHAT_MODEL_WORKERS,FSCHAT_CONTROLLER,API_SERVER,FSCHAT_OPENAI_API,LLM_MODELS,NLTK_DATA_PATH,DEFAULT_BIND_HOST,SERVER_PORT,HF_HOME,HF_ENDPOINT,HTTPX_DEFAULT_TIMEOUT)
from server.utils import (get_httpx_client,get_model_worker_config,fschat_controller_address,fschat_model_worker_address)
from server.db.init_database_script import create_tables

os.environ["HF_ENDPOINT"]=HF_ENDPOINT
os.environ["HF_HOME"]=HF_HOME



from server.utils import(
    MakeFastAPIOffline,FastAPI
)
from pool.model_pool import model_pool


def create_controller_app(
        dispatch_method: str,
        log_level: str = "INFO",
):
    import fastchat.constants
    fastchat.constants.LOGDIR = LOG_PATH
    from fastchat.serve.controller import app, Controller, logger
    logger.setLevel(log_level)
    controller = Controller(dispatch_method)
    # 将controller转化为全局模块
    sys.modules["fastchat.serve.controller"].controller = controller

    MakeFastAPIOffline(app)
    app.title = "FastChat Controller(FastChat 控制类)"
    app._controller = controller
    return app

def create_model_worker_app(log_level: str = "INFO", **kwargs) -> FastAPI:
    """
    kwargs:{
        host:主机地址,
        port:端口号，
        model_names:模型名称，可以为数组，
        controller_address:controller地址
        worker_address:worker地址
        langchain_model:true/false,是否为langchain 模型
        online_api:true/false 是否为线上模型
        worker_class:自定义worker类,
        model_path:模型路径，只正对于本地路径可加
        device:显卡驱动
    }
    """
    import fastchat.constants
    fastchat.constants.LOGDIR = LOG_PATH
    import argparse

    parser = argparse.ArgumentParser()
    args = parser.parse_args([])

    for k, v in kwargs.items():
        setattr(args, k, v)
    if worker_class := kwargs.get("langchain_model"):
        from fastchat.serve.base_model_worker import app
        worker = ""
    # 在线模型API
    elif worker_class := kwargs.get("worker_class"):
        from fastchat.serve.base_model_worker import app

        worker = worker_class(model_names=args.model_names,
                              controller_addr=args.controller_address,
                              worker_addr=args.worker_address)
        sys.modules["fastchat.serve.base_model_worker"].logger.setLevel(log_level)
    # 本地模型
    else:
        from fastchat.serve.model_worker import app, GptqConfig, AWQConfig, ModelWorker, worker_id

        args.gpus = "0"  # GPU的编号,如果有多个GPU，可以设置为"0,1,2,3"
        args.npus = None
        args.max_gpu_memory = None
        args.num_gpus = 1  # model worker的切分是model并行，这里填写显卡的数量
        args.num_npus = 1  # model worker的切分是model并行，这里填写显卡的数量
        args.load_8bit = False
        args.cpu_offloading = None
        args.gptq_ckpt = None
        args.gptq_wbits = 16
        args.gptq_groupsize = -1
        args.gptq_act_order = False
        args.awq_ckpt = None
        args.awq_wbits = 16
        args.awq_groupsize = -1
        args.model_names = [""]
        args.conv_template = None
        args.limit_worker_concurrency = 5
        args.stream_interval = 2
        args.no_register = False
        args.embed_in_truncate = False
        for k, v in kwargs.items():
            setattr(args, k, v)
        gptq_config = GptqConfig(
            ckpt=args.gptq_ckpt or args.model_path,
            wbits=args.gptq_wbits,
            groupsize=args.gptq_groupsize,
            act_order=args.gptq_act_order,
        )
        awq_config = AWQConfig(
            ckpt=args.awq_ckpt or args.model_path,
            wbits=args.awq_wbits,
            groupsize=args.awq_groupsize,
        )

        worker = ModelWorker(
            controller_addr=args.controller_address,
            worker_addr=args.worker_address,
            worker_id=worker_id,
            model_path=args.model_path,
            model_names=args.model_names,
            limit_worker_concurrency=args.limit_worker_concurrency,
            no_register=args.no_register,
            device=args.device,
            num_gpus=args.num_gpus,
            max_gpu_memory=args.max_gpu_memory,
            load_8bit=args.load_8bit,
            cpu_offloading=args.cpu_offloading,
            gptq_config=gptq_config,
            awq_config=awq_config,
            stream_interval=args.stream_interval,
            conv_template=args.conv_template,
            embed_in_truncate=args.embed_in_truncate,
        )
        # sys.modules["fastchat.serve.model_worker"][args.model_names[0]].args = args
        # sys.modules["fastchat.serve.model_worker"][args.model_names[0]].gptq_config = gptq_config
        # # sys.modules["fastchat.serve.model_worker"].worker = worker
        # sys.modules["fastchat.serve.model_worker"][args.model_names[0]].logger.setLevel(log_level)

    MakeFastAPIOffline(app)
    app.title = f"FastChat LLM Server ({args.model_names[0]})"
    app._worker = worker
    return app

def create_openai_api_app(
        controller_address: str,
        api_keys: List = [],
        log_level: str = "INFO",
) -> FastAPI:
    import fastchat.constants
    fastchat.constants.LOGDIR = LOG_PATH
    from fastchat.serve.openai_api_server import app, CORSMiddleware, app_settings
    from fastchat.utils import build_logger
    logger = build_logger("openai_api", "openai_api.log")
    logger.setLevel(log_level)

    sys.modules["fastchat.serve.openai_api_server"].logger = logger
    app_settings.controller_address = controller_address
    app_settings.api_keys = api_keys

    MakeFastAPIOffline(app)
    app.title = "FastChat OpeanAI API Server"
    return app

def _set_app_event(app: FastAPI, started_event: multiprocessing.Event = None,**kwargs):
    # controller启动时
    @app.on_event("startup")
    async def on_startup():
        if started_event is not None:
            started_event.set()

    # controller关闭时
    @app.on_event("shutdown")
    async def on_shutdown():
        if kwargs.get("model_name"):
            model_name=kwargs.get("model_name")
            model_pool.release_model_in_dict(model_name)
        
    
def run_controller(log_level: str = "INFO", started_event: multiprocessing.Event = None):
    import uvicorn
    from fastapi import Body
    import time
    import sys
    from server.utils import set_httpx_config
    set_httpx_config()

    app = create_controller_app(
        dispatch_method=FSCHAT_CONTROLLER.get("dispatch_method"),
        log_level=log_level,
    )
    _set_app_event(app, started_event)

    # add interface to release and load model worker
    @app.post("/release_worker")
    def release_worker(
            model_name: str = Body(..., description="要释放模型的名称", samples=["OpenBA-V2-Chat"]),
            new_model_name: str = Body(None, description="释放后加载该模型"),
            keep_origin: bool = Body(False, description="不释放原模型，加载新模型")
    ) -> Dict:
        # available_models已经注册的模型
        available_models = app._controller.list_models()
        if new_model_name in available_models:
            msg = f"要切换的LLM模型 {new_model_name} 已经存在"
            logger.info(msg)
            return {"code": 500, "msg": msg}

        if new_model_name:
            logger.info(f"开始切换LLM模型:从 {model_name} 到 {new_model_name}")
        else:
            logger.info(f"即将停止LLM模型: {model_name}")

        if model_name not in available_models:
            msg = f"the model {model_name} is not available"
            logger.error(msg)
            return {"code": 500, "msg": msg}

        worker_address = app._controller.get_worker_address(model_name)
        if not worker_address:
            msg = f"can not find model_worker address for {model_name}"
            logger.error(msg)
            return {"code": 500, "msg": msg}
        
        with get_httpx_client() as client:
            r = client.post(worker_address + "/release",
                            json={"new_model_name": new_model_name, "keep_origin": keep_origin})
            if r.status_code != 200:
                msg = f"failed to release model: {model_name}"
                logger.error(msg)
                return {"code": 500, "msg": msg}

        if new_model_name:
            timer = HTTPX_DEFAULT_TIMEOUT  # wait for new model_worker register
            while timer > 0:
                models = app._controller.list_models()
                if new_model_name in models:
                    break
                time.sleep(1)
                timer -= 1
            if timer > 0:
                msg = f"sucess change model from {model_name} to {new_model_name}"
                logger.info(msg)
                return {"code": 200, "msg": msg}
            else:
                msg = f"failed change model from {model_name} to {new_model_name}"
                logger.error(msg)
                return {"code": 500, "msg": msg}
        else:
            msg = f"sucess to release model: {model_name}"
            logger.info(msg)
            return {"code": 200, "msg": msg}

    host = FSCHAT_CONTROLLER["host"]
    port = FSCHAT_CONTROLLER["port"]

    if log_level == "ERROR":
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    uvicorn.run(app, host=host, port=port, log_level=log_level.lower())

def run_model_worker(
        model_name: str = LLM_MODELS[0],
        controller_address: str = "",
        log_level: str = "INFO",
        q: multiprocessing.Queue = None,
        started_event: multiprocessing.Event = None,
):  
    model=FSCHAT_MODEL_WORKERS[model_name]
    if model.get('gpus'):
        if model.get('num_gpus') is None:
            model["num_gpus"] = len(model.get('gpus').split(','))
        if len(model.get('gpus').split(",")) < model.get("num_gpus"):
            raise ValueError(
                f"Larger --num-gpus ({model.get('num_gpus')}) than --gpus {model.get('gpus')}!"
            )
        os.environ["CUDA_VISIBLE_DEVICES"] = model["gpus"]
        logger.info(f"当前GPU编号:{model.get('gpus')}，使用数量:{model.get('num_gpus')}")
    if model.get('npus'):
        if model.get('num_npus') is None:
            model["num_gpus"] = len(model.get("npus").split(','))
        if len(model.get("npus").split(",")) < model.get("num_npus"):
            raise ValueError(
                f"Larger --num-npus ({model.get('num_npus')}) than --npus {model.get('npus')}!"
            )
        os.environ["ASCEND_RT_VISIBLE_DEVICES"] = model["npus"]
        logger.info(f"当前NPU编号:{model.get('npus')}，使用数量:{model.get('num_npus')}")
        
    import uvicorn
    from fastapi import Body
    import sys
    from server.utils import set_httpx_config
    set_httpx_config()
    kwargs = get_model_worker_config(model_name)
    host = kwargs.pop("host")
    port = kwargs.pop("port")
    kwargs["model_names"] = [model_name]
    kwargs["controller_address"] = controller_address or fschat_controller_address()
    kwargs["worker_address"] = fschat_model_worker_address(model_name)
    model_path = kwargs.get("model_path", "")
    kwargs["model_path"] = model_path
    app = create_model_worker_app(log_level=log_level, **kwargs)
    _set_app_event(app, started_event)
    if log_level == "ERROR":
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    # add interface to release and load model
    @app.post("/release")
    def release_model(
            new_model_name: str = Body(None, description="释放后加载该模型"),
            keep_origin: bool = Body(False, description="不释放原模型，加载新模型")
    ) -> Dict:
        if keep_origin:
            if new_model_name:
                q.put([model_name, "start", new_model_name])
        else:
            if new_model_name:
                q.put([model_name, "replace", new_model_name])
            else:
                q.put([model_name, "stop", None])
        return {"code": 200, "msg": "done"}

    uvicorn.run(app, host=host, port=port, log_level=log_level.lower())


def run_openai_api(log_level: str = "INFO", started_event: multiprocessing.Event = None):
    import uvicorn
    import sys
    from server.utils import set_httpx_config
    set_httpx_config()

    controller_addr = fschat_controller_address()
    app = create_openai_api_app(controller_addr, log_level=log_level)
    _set_app_event(app, started_event)

    host = FSCHAT_OPENAI_API["host"]
    port = FSCHAT_OPENAI_API["port"]
    if log_level == "ERROR":
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
    uvicorn.run(app, host=host, port=port)

def run_api_server(started_event: multiprocessing.Event = None, run_mode: str = None):
    from server.api import create_app
    import uvicorn
    from server.utils import set_httpx_config
    set_httpx_config()

    app = create_app(run_mode=run_mode)
    _set_app_event(app, started_event)
    MakeFastAPIOffline(app)
    host = API_SERVER["host"]
    port = API_SERVER["port"]
    import uvicorn
    uvicorn.run(app,
                host=host,
                port=port)




def parse_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--all-api",
        action="store_true",
        help="run fastchat's controller/openai_api/model_worker servers, run api.py",
        dest="all_api",
    )
    parser.add_argument(
        "-n",
        "--model-name",
        type=str,
        nargs="+",
        default=LLM_MODELS,
        help="specify model name for model worker. "
             "add addition names with space seperated to start multiple model workers.",
        dest="model_name",
    )
    parser.add_argument(
        "--api",
        action="store_true",
        help="run api.py server",
        dest="api",
    )
    parser.add_argument(
        "-m",
        "--model-worker",
        action="store_true",
        help="run model worker api",
        dest="model_worker",
    )
    parser.add_argument(
        "-c",
        "--controller",
        type=str,
        help="specify controller address the worker is registered to. default is FSCHAT_CONTROLLER",
        dest="controller_address",
    )
    parser.add_argument(
        "-p",
        "--api-worker",
        action="store_true",
        help="run online model api such as zhipuai",
        dest="api_worker",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="减少fastchat服务log信息",
        dest="quiet",
    )
    args = parser.parse_args()
    return args, parser

async def start_main_server():
    import time
    import signal

    def handler(signalname):
        def f(signal_received, frame):
            raise KeyboardInterrupt(f"{signalname} received")

        return f

    # 当程序接收到 SIGINT (Ctrl+C) 或 SIGTERM (终止进程信号) 时，会触发 handler，并抛出 KeyboardInterrupt 以优雅地退出程序。
    signal.signal(signal.SIGINT, handler("SIGINT"))
    signal.signal(signal.SIGTERM, handler("SIGTERM"))

    multiprocessing.set_start_method("spawn")
    
    # multiprocessing.Manager() 负责创建共享资源，如 进程间通信队列
    manager = multiprocessing.Manager()
    run_mode = None
    
    # 构建进程队列
    queue = manager.Queue()
    
    args, parser = parse_args()

    if not args.all_api:
        return
    if len(sys.argv) > 1:
        logger.info(f"正在启动服务:")
        logger.info(f"如需查看 llm_api 日志，请前往 {LOG_PATH}")

    # 进程存储对象，存储了online_api进程和model_worker进程
    processes = {"online_api": {}, "model_worker": {}}

    # 计算进程数量
    def process_count():
        return len(processes) + len(processes["online_api"]) + len(processes["model_worker"]) - 2

    if args.quiet or not log_verbose:
        log_level = "ERROR"
    else:
        log_level = "INFO"

    # 构建controller启动事件
    controller_started = manager.Event()
    
    # 构建Controller进程
    process = Process(
        target=run_controller,
        name=f"controller",
        kwargs=dict(log_level=log_level, started_event=controller_started),
        daemon=True,
    )
    
    # 存储controller进程
    processes["controller"] = process

    # 构建openai_api进程
    process = Process(
        target=run_openai_api,
        name=f"openai_api",
        daemon=True,
    )
    
    # 存储controller进程
    processes["openai_api"] = process

    model_worker_started = []
    if args.model_worker:
        for model_name in args.model_name:
            config = get_model_worker_config(model_name)
            if not config.get("online_api"):
                e = manager.Event()
                model_worker_started.append(e)
                process = Process(
                    target=run_model_worker,
                    name=f"model_worker - {model_name}",
                    kwargs=dict(model_name=model_name,
                                controller_address=args.controller_address,
                                log_level=log_level,
                                q=queue,
                                started_event=e),
                    daemon=True,
                )
                model_pool.register_model_in_dict(model_name)
                processes["model_worker"][model_name] = process

    if args.api_worker:
        for model_name in args.model_name:
            config = get_model_worker_config(model_name)
            if (config.get("online_api") # 在online_api 模块中
                    and config.get("worker_class")# 在自定义的输出类中
                    and model_name in FSCHAT_MODEL_WORKERS):
                # e = manager.Event()
                # model_worker_started.append(e)
                # process = Process(
                #     target=run_model_worker,
                #     name=f"api_worker - {model_name}",
                #     kwargs=dict(model_name=model_name,
                #                 controller_address=args.controller_address,
                #                 log_level=log_level,
                #                 q=queue,
                #                 started_event=e),
                #     daemon=True,
                # )
                # processes["online_api"][model_name] = process
                model_pool.register_model_in_dict(model_name)
    api_started = manager.Event()
    if args.api:
        process = Process(
            target=run_api_server,
            name=f"API Server",
            kwargs=dict(started_event=api_started, run_mode=run_mode),
            daemon=True,
        )
        processes["api"] = process



    if process_count() == 0:
        parser.print_help()
    else:
        try:
            # 保证任务收到SIGINT后，能够正常退出
            if p := processes.get("controller"):
                p.start()
                p.name = f"{p.name} ({p.pid})"
                controller_started.wait()  # 等待controller启动完成

            if p := processes.get("openai_api"):
                p.start()
                p.name = f"{p.name} ({p.pid})"

            for model_name, p in processes.get("model_worker", {}).items():
                p.start()
                p.name = f"{p.name} ({p.pid})"

            for n, p in processes.get("online_api", []).items():
                p.start()
                p.name = f"{p.name} ({p.pid})"

            

            if p := processes.get("api"):
                p.start()
                p.name = f"{p.name} ({p.pid})"
                api_started.wait()  # 等待api.py启动完成
            # 等待所有model_worker启动完成
            for e in model_worker_started:
                e.wait()
            while True:
                cmd = queue.get()  # 收到切换模型的消息
                e = manager.Event()
                if isinstance(cmd, list):
                    model_name, cmd, new_model_name = cmd
                    if cmd == "start":  # 运行新模型
                        logger.info(f"准备启动新模型进程:{new_model_name}")
                        process = Process(
                            target=run_model_worker,
                            name=f"model_worker - {new_model_name}",
                            kwargs=dict(model_name=new_model_name,
                                        controller_address=args.controller_address,
                                        log_level=log_level,
                                        q=queue,
                                        started_event=e),
                            daemon=True,
                        )
                        process.start()
                        process.name = f"{process.name} ({process.pid})"
                        processes["model_worker"][new_model_name] = process
                        e.wait()
                        model_pool.register_model_in_dict(new_model_name)
                        logger.info(f"成功启动新模型进程:{new_model_name}")
                    elif cmd == "stop":
                        if process := processes["model_worker"].get(model_name):
                            time.sleep(1)
                            process.terminate()
                            process.join()
                            logger.info(f"停止模型进程:{model_name}")
                        else:
                            logger.error(f"未找到模型进程:{model_name}")
                    elif cmd == "replace":
                        if process := processes["model_worker"].pop(model_name, None):
                            logger.info(f"停止模型进程:{model_name}")
                            start_time = datetime.now()
                            time.sleep(1)
                            process.terminate()
                            model_pool.release_model_in_dict(model_name)                        
                            process.join()
                            process = Process(
                                target=run_model_worker,
                                name=f"model_worker - {new_model_name}",
                                kwargs=dict(model_name=new_model_name,
                                            controller_address=args.controller_address,
                                            log_level=log_level,
                                            q=queue,
                                            started_event=e),
                                daemon=True,
                                
                            )
                            model_pool.register_model_in_dict(new_model_name)                        
                            process.start()
                            process.name = f"{process.name} ({process.pid})"
                            processes["model_worker"][new_model_name] = process
                            e.wait()
                            timing = datetime.now() - start_time
                            logger.info(f"成功启动新模型进程:{new_model_name}。用时:{timing}。")
                        else:
                            logger.error(f"未找到模型进程:{model_name}")

        except Exception as e:
            logger.error(e)
            logger.warning("Caught KeyboardInterrupt! Setting stop event...")
        finally:
            for p in processes.values():
                logger.warning("Sending SIGKILL to %s", p)

                if isinstance(p, dict):
                    for process in p.values():
                        process.kill()
                else:
                    p.kill()
            for p in processes.values():
                logger.info("Process status: %s", p)


if __name__ == "__main__":
    create_tables()
    if sys.version_info < (3, 10):
        loop = asyncio.get_event_loop()
    else:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()

        asyncio.set_event_loop(loop)
    loop.run_until_complete(start_main_server())