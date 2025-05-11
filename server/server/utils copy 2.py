# -*- coding:UTF-8 -*-
# @Time : 2024/3/7 11:21
# @Author : 寻梦
# @File : utils
# @Project : langchain-ChatBA
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List,Literal,Optional
from langchain.embeddings.base import Embeddings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import (
    TYPE_CHECKING,
    Literal,
    Optional,
    Callable,
    Generator,
    Dict,
    Any,
    Awaitable,
    Union,
    Tuple
)
import httpx

from configs import (LLM_MODELS,LLM_DEVICE,logger,log_verbose,HTTPX_DEFAULT_TIMEOUT)

# 主要的作用是将FastAPi中的swagger文档设置成本地链接，放置访问外网
def MakeFastAPIOffline(
        app: FastAPI,
        static_dir=Path(__file__).parent / "static",
        static_url="/static",
        docs_url: Optional[str] = "/docs",
        redoc_url: Optional[str] = "/redoc",
) -> None:
    """patch the FastAPI obj that doesn't rely on CDN for the documentation page"""
    from fastapi import Request
    from fastapi.openapi.docs import (
        get_redoc_html,
        get_swagger_ui_html,
        get_swagger_ui_oauth2_redirect_html,
    )
    from fastapi.staticfiles import StaticFiles
    from starlette.responses import HTMLResponse

    openapi_url = app.openapi_url
    swagger_ui_oauth2_redirect_url = app.swagger_ui_oauth2_redirect_url

    # 移除路径
    def remove_route(url: str) -> None:
        '''
        remove original route from app
        '''
        index = None
        for i, r in enumerate(app.routes):
            if r.path.lower() == url.lower():
                index = i
                break
        if isinstance(index, int):
            app.routes.pop(index)

    # Set up static file mount
    app.mount(
        static_url,
        StaticFiles(directory=Path(static_dir).as_posix()),
        name="static",
    )

    if docs_url is not None:
        remove_route(docs_url)
        remove_route(swagger_ui_oauth2_redirect_url)

        @app.get(docs_url, include_in_schema=False)
        async def custom_swagger_ui_html(request: Request) -> HTMLResponse:
            root = request.scope.get("root_path")
            favicon = f"{root}{static_url}/favicon.png"
            swagger_ui_html= get_swagger_ui_html(
                openapi_url=f"{root}{openapi_url}",
                title=app.title + " - Swagger UI",
                oauth2_redirect_url=swagger_ui_oauth2_redirect_url,
                swagger_js_url=f"{root}{static_url}/swagger-ui-bundle.js",
                swagger_css_url=f"{root}{static_url}/swagger-ui.css",
                swagger_favicon_url=favicon,
            )
            return swagger_ui_html

        @app.get(swagger_ui_oauth2_redirect_url, include_in_schema=False)
        async def swagger_ui_redirect() -> HTMLResponse:
            return get_swagger_ui_oauth2_redirect_html()

    if redoc_url is not None:
        remove_route(redoc_url)

        @app.get(redoc_url, include_in_schema=False)
        async def redoc_html(request: Request) -> HTMLResponse:
            root = request.scope.get("root_path")
            favicon = f"{root}{static_url}/favicon.png"

            return get_redoc_html(
                openapi_url=f"{root}{openapi_url}",
                title=app.title + " - ReDoc",
                redoc_js_url=f"{root}{static_url}/redoc.standalone.js",
                with_google_fonts=False,
                redoc_favicon_url=favicon,
            )
    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
def llm_device(device: str = None) -> Literal["cuda", "gpu","npu","mps", "cpu"]:
    device = device or LLM_DEVICE
    if device not in ["cuda", "gpu","npu","mps", "cpu"]:
        device = detect_device()
    return device
    

def get_model_worker_config(model_name: str = None) -> dict:
    '''
    加载model worker的配置项。
    优先级:FSCHAT_MODEL_WORKERS[model_name] > ONLINE_LLM_MODEL[model_name] > FSCHAT_MODEL_WORKERS["default"]
    '''
    from configs.model_config import ONLINE_LLM_MODEL, MODEL_PATH
    from configs.server_config import FSCHAT_MODEL_WORKERS
    # 导入自定义的model
    from server import model_workers

    config = FSCHAT_MODEL_WORKERS.get(model_name, {}).copy()
    config.update(ONLINE_LLM_MODEL.get(model_name, {}).copy())
    config.update(FSCHAT_MODEL_WORKERS.get(model_name, {}).copy())

    # 线上模型
    if model_name in ONLINE_LLM_MODEL:
        config["online_api"] = True
        if provider := config.get("provider"):
            try:
                config["worker_class"] = getattr(model_workers, provider)
            except Exception as e:
                msg = f"在线模型 ‘{model_name}’ 的provider没有正确配置"
                logger.error(f'{e.__class__.__name__}: {msg}',
                             exc_info=e if log_verbose else None)
    # 本地模型
    if model_name in MODEL_PATH["llm_model"]:
        # 获取模型路径
        path = get_model_path(model_name)
        config["model_path"] = path
        if path and os.path.isdir(path):
            config["model_path_exists"] = True
        config["device"] = llm_device(config.get("device"))
    """
    config:{
        online_api:"",
        worker_class:"",
        provider:"",
        model_path:"",
        model_path_exists:"",
        device:""
    }
    """
    return config


def fschat_controller_address() -> str:
    from configs.server_config import FSCHAT_CONTROLLER
    host = FSCHAT_CONTROLLER["host"]
    port = FSCHAT_CONTROLLER["port"]
    return f"http://{host}:{port}"


def fschat_model_worker_address(model_name: str = LLM_MODELS[0]) -> str:
    if model := get_model_worker_config(model_name):
        host = model["host"]
        if host == "0.0.0.0":
            host = "127.0.0.1"
        port = model["port"]
        return f"http://{host}:{port}"
    return ""


def fschat_openai_api_address() -> str:
    from configs.server_config import FSCHAT_OPENAI_API
    host = FSCHAT_OPENAI_API["host"]
    port = FSCHAT_OPENAI_API["port"]
    return f"http://{host}:{port}/v1"

def get_httpx_client(
        use_async: bool = False,
        proxies: Union[str, Dict] = None,
        timeout: float = HTTPX_DEFAULT_TIMEOUT,
        **kwargs,
) -> Union[httpx.Client, httpx.AsyncClient]:
    '''
    helper to get httpx client with default proxies that bypass local addesses.
    '''
    default_proxies = {
        # do not use proxy for locahost
        "all://127.0.0.1": None,
        "all://localhost": None,
    }
    # do not use proxy for user deployed fastchat servers
    for x in [
        fschat_controller_address(),
        fschat_model_worker_address(),
        fschat_openai_api_address(),
    ]:
        host = ":".join(x.split(":")[:2])
        default_proxies.update({host: None})

    # get proxies from system envionrent
    # proxy not str empty string, None, False, 0, [] or {}
    default_proxies.update({
        "http://": (os.environ.get("http_proxy")
                    if os.environ.get("http_proxy") and len(os.environ.get("http_proxy").strip())
                    else None),
        "https://": (os.environ.get("https_proxy")
                     if os.environ.get("https_proxy") and len(os.environ.get("https_proxy").strip())
                     else None),
        "all://": (os.environ.get("all_proxy")
                   if os.environ.get("all_proxy") and len(os.environ.get("all_proxy").strip())
                   else None),
    })
    for host in os.environ.get("no_proxy", "").split(","):
        if host := host.strip():
            # default_proxies.update({host: None}) # Origin code
            default_proxies.update({'all://' + host: None})  # PR 1838 fix, if not add 'all://', httpx will raise error

    # merge default proxies with user provided proxies
    if isinstance(proxies, str):
        proxies = {"all://": proxies}

    if isinstance(proxies, dict):
        default_proxies.update(proxies)

    # construct Client
    kwargs.update(timeout=timeout, proxies=default_proxies)

    if log_verbose:
        logger.info(f'{get_httpx_client.__class__.__name__}:kwargs: {kwargs}')

    if use_async:
        return httpx.AsyncClient(**kwargs)
    else:
        return httpx.Client(**kwargs)

def set_httpx_config(
        timeout: float = HTTPX_DEFAULT_TIMEOUT,
        proxy: Union[str, Dict] = None,
):
    '''
    设置httpx默认timeout。httpx默认timeout是5秒，在请求LLM回答时不够用。
    将本项目相关服务加入无代理列表，避免fastchat的服务器请求错误。(windows下无效)
    对于chatgpt等在线API，如要使用代理需要手动配置。搜索引擎的代理如何处置还需考虑。
    '''

    import httpx
    import os

    httpx._config.DEFAULT_TIMEOUT_CONFIG.connect = timeout
    httpx._config.DEFAULT_TIMEOUT_CONFIG.read = timeout
    httpx._config.DEFAULT_TIMEOUT_CONFIG.write = timeout

    # 在进程范围内设置系统级代理
    proxies = {}
    if isinstance(proxy, str):
        for n in ["http", "https", "all"]:
            proxies[n + "_proxy"] = proxy
    elif isinstance(proxy, dict):
        for n in ["http", "https", "all"]:
            if p := proxy.get(n):
                proxies[n + "_proxy"] = p
            elif p := proxy.get(n + "_proxy"):
                proxies[n + "_proxy"] = p

    for k, v in proxies.items():
        os.environ[k] = v

    # set host to bypass proxy
    no_proxy = [x.strip() for x in os.environ.get("no_proxy", "").split(",") if x.strip()]
    no_proxy += [
        # do not use proxy for locahost
        "http://127.0.0.1",
        "http://localhost",
    ]
    # do not use proxy for user deployed fastchat servers
    for x in [
        fschat_controller_address(),
        fschat_model_worker_address(),
        fschat_openai_api_address(),
    ]:
        host = ":".join(x.split(":")[:2])
        if host not in no_proxy:
            no_proxy.append(host)
    os.environ["NO_PROXY"] = ",".join(no_proxy)

    def _get_proxies():
        return proxies

    import urllib.request
    urllib.request.getproxies = _get_proxies

import os
from configs import (KB_ROOT_PATH,MODEL_PATH,EMBEDDING_DEVICE,MODEL_ROOT_PATH,ONLINE_EMBED_MODEL)

def validate_factory_name(factory_name):
    if '../' in factory_name:
        return False
    return True


def get_kb_path(factory_name: str):
    return os.path.join(KB_ROOT_PATH, factory_name)

def get_doc_path(factory_name: str):
    return os.path.join(get_kb_path(factory_name), "content")

def get_file_path(factory_name: str, doc_name: str):
    return os.path.join(get_doc_path(factory_name), doc_name)



def list_online_embed_models() -> List[str]:
    return ONLINE_EMBED_MODEL.keys()




def get_model_path(model_name: str, type: str = None) -> Optional[str]:
    if type in MODEL_PATH:
        paths = MODEL_PATH[type]
    else:
        paths = {}
        for v in MODEL_PATH.values():
            paths.update(v)
    if path_str := paths.get(model_name):  # 以 "OpenBA-V2-Chat": "OpenNLG/OpenBA-V2-Chat" 为例，以下都是支持的路径
        path = Path(path_str)
        if path.is_dir():  # 任意绝对路径
            return str(path)
        root_path = Path(MODEL_ROOT_PATH)
        if root_path.is_dir():
            path = root_path / model_name
            if path.is_dir():  # use key, {MODEL_ROOT_PATH}/OpenBA-V2-Chat
                return str(path)
            path = root_path / path_str
            if path.is_dir():  # use value, {MODEL_ROOT_PATH}/OpenNLG/OpenBA-V2-Chat
                return str(path)
            path = root_path / path_str.split("/")[-1]
            if path.is_dir():  # use value split by "/", {MODEL_ROOT_PATH}/OpenBA-V2-Chat
                return str(path)
        return path_str  # OpenNLG/OpenBA-V2-Chat


def list_local_embed_models() -> List[str]:
    '''
    get names of configured embedding models
    '''
    return list(MODEL_PATH["embed_model"])

def detect_device() -> Literal["cuda", "mps", "cpu","npu"]:
    try:
        import torch
        if torch.cuda.is_available():
            return "cuda"
        if torch.backends.mps.is_available():
            return "mps"
        import torch_npu
        if torch_npu.npu.is_available():
            return "npu"
    except:
        pass
    return "cpu"

def embedding_device(device: str = None) -> Literal["cuda", "mps", "cpu","npu"]:
    device = device or EMBEDDING_DEVICE
    if device not in ["cuda", "mps", "cpu","npu"]:
        device = detect_device()
    return device



def load_local_embeddings(model: str = None, device: str = embedding_device())->Embeddings:
    '''
    从缓存中加载embeddings，可以避免多线程时竞争加载。
    '''
    ## todo 实现embding的加载
    from server.embedding.pool.embeding_pool import embeddings_pool
    from configs import EMBEDDING_MODEL

    model = model or EMBEDDING_MODEL
    return embeddings_pool.load_embeddings(model=model, device=device)


from typing import (
    TYPE_CHECKING,
    Literal,
    Optional,
    Callable,
    Generator,
    Dict,
    List
)


# 用线程池去跑，加快速度
def run_in_thread_pool(
        func: Callable,
        params: List[Dict] = [],
) -> Generator:
    '''
    在线程池中批量运行任务，并将运行结果以生成器的形式返回。
    请确保任务中的所有操作是线程安全的，任务函数请全部使用关键字参数。
    '''
    tasks = []
    with ThreadPoolExecutor() as pool:
        for kwargs in params:
            thread = pool.submit(func, **kwargs)
            tasks.append(thread)

        for obj in as_completed(tasks):
            yield obj.result()