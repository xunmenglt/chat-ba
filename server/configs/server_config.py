# -*- coding:UTF-8 -*-
# @Time : 2024/3/6 14:12
# @Author : 寻梦
# @File : server_config
# @Project : langchain-ChatBA
import sys
from configs.model_config import LLM_DEVICE

# httpx 请求默认超时时间（秒）。如果加载模型或对话较慢，出现超时错误，可以适当加大该值。
HTTPX_DEFAULT_TIMEOUT = 300.0

# API 是否开启跨域，默认为False，如果需要开启，请设置为True
# is open cross domain
OPEN_CROSS_DOMAIN = False

# 各服务器默认绑定host。如改为"0.0.0.0"需要修改下方所有XX_SERVER的host
DEFAULT_BIND_HOST = "0.0.0.0"

# 服务运行端口
SERVER_PORT=9889


# webui.py server
WEBUI_SERVER = {
    "host": DEFAULT_BIND_HOST,
    "port": 8501,
}

# api.py server
API_SERVER = {
    "host": DEFAULT_BIND_HOST,
    "port": 9889,
}

# fastchat openai_api server
FSCHAT_OPENAI_API = {
    "host": DEFAULT_BIND_HOST,
    "port": 29001,
}

# fastchat model_worker server
# 这些模型必须是在model_config.MODEL_PATH或ONLINE_MODEL中正确配置的。
# 在启动startup.py时，可用通过`--model-name xxxx yyyy`指定模型，不指定则为LLM_MODELS
FSCHAT_MODEL_WORKERS = {
    "qwen-plus":{
        "host": DEFAULT_BIND_HOST,
        "port": 31610,
    },
    "ge-bert":{
        "host": DEFAULT_BIND_HOST,
        "port": 31010,
    },
    "ge-bert-mask":{
        "host": DEFAULT_BIND_HOST,
        "port": 31019,
    },
    "moonshot-v1-8k":{
        "host": DEFAULT_BIND_HOST,
        "port": 31011,
    },
    "deepseek-chat":{
        "host": DEFAULT_BIND_HOST,
        "port": 31111,
    },
    "CodeLlama-7b-hf":{
        "host": DEFAULT_BIND_HOST,
        "port": 31010,
        "load_8bit": False,
        "gpus":"1",
    },
    "OpenBA-V2-Chat":{
        "host": DEFAULT_BIND_HOST,
        "port": 31110,
        "load_8bit": False,
        "gpus":"0",
        "num_gpus":1,
        "conv_template":"openba-chat"
    },
    "openba2-3b-RCB-QA":{
        "host": DEFAULT_BIND_HOST,
        "port": 31010,
        "load_8bit": False,
        "gpus":"1",
        "conv_template":"openba-chat"
    },
    "openba2-3b-RCB-Chat":{
        "host": DEFAULT_BIND_HOST,
        "port": 31020,
        "load_8bit": False,
        "gpus":"2",
        "conv_template":"openba-chat"
    },
    "openba2-3b-RCB-Chat-v2":{
        "host": DEFAULT_BIND_HOST,
        "port": 31025,
        "load_8bit": False,
        "gpus":"3",
        "conv_template":"openba-chat"
    },
    "chatglm3-6b-RCB-QA":{
        "host": DEFAULT_BIND_HOST,
        "port": 31030,
        "load_8bit": False,
        "gpus":"4",
        "conv_template":"chatglm3"
    },
    "chatglm3-6b-RCB-Chat":{
        "host": DEFAULT_BIND_HOST,
        "port": 31040,
        "load_8bit": False,
        "gpus":"5",
        "conv_template":"chatglm3"
    },
    "chatglm3-6b":{
        "host": DEFAULT_BIND_HOST,
        "port": 23070,
        "load_8bit": False,
        "num_gpus": 1,
        "gpus":"3",
        "conv_template":"chatglm3"
    },
    "Qwen1.5-7B-Chat":{
        "host": DEFAULT_BIND_HOST,
        "port": 31150,
        "load_8bit": False,
        "num_gpus": 1,
        "gpus":"1",
        "conv_template":"qwen-7b-chat"
    },
    "Qwen2-7B-Instruct@1":{
        "host": DEFAULT_BIND_HOST,
        "port": 31050,
        "load_8bit": False,
        "num_gpus": 1,
        "gpus":"6",
        "conv_template":"qwen-7b-chat"
    },
    "Qwen2-7B-Instruct@2":{
        "host": DEFAULT_BIND_HOST,
        "port": 31060,
        "load_8bit": False,
        "num_gpus": 1,
        "gpus":"5",
        "conv_template":"qwen-7b-chat"
    },
    "Qwen2-7B-Instruct@3":{
        "host": DEFAULT_BIND_HOST,
        "port": 31070,
        "load_8bit": False,
        "num_gpus": 1,
        "gpus":"6",
        "conv_template":"qwen-7b-chat"
    },
    "Qwen2-7B-Instruct":{
        "host": DEFAULT_BIND_HOST,
        "port": 31080,
        "load_8bit": False,
        "num_gpus": 2,
        "gpus":"3,4",
        "conv_template":"qwen-7b-chat"
    },
    "Qwen2-0.5B-Instruct":{
        "host": DEFAULT_BIND_HOST,
        "port": 31880,
        "load_8bit": False,
        "num_gpus": 1,
        "gpus":"3",
        "conv_template":"qwen-7b-chat"
    },
    "CodeQwen1.5-7B":{
        "host": DEFAULT_BIND_HOST,
        "port": 31082,
        "load_8bit": False,
        "num_gpus": 1,
        "gpus":"4",
        "conv_template":"qwen-7b-chat"
    },
    "CodeQwen1.5-7B-Chat":{
        "host": DEFAULT_BIND_HOST,
        "port": 31083,
        "load_8bit": False,
        "num_gpus": 1,
        "gpus":"5",
        "conv_template":"qwen-7b-chat"
    }

    # 所有模型共用的默认配置，可在模型专项配置中进行覆盖。
    # "default": {
    #     "host": DEFAULT_BIND_HOST,
    #     "port": 20002,
    #     "device": LLM_DEVICE,
    #     # False,'vllm',使用的推理加速框架,使用vllm如果出现HuggingFace通信问题，参见doc/FAQ
    #     # vllm对一些模型支持还不成熟，暂时默认关闭
    #     "infer_turbo": False,
    #
    #     # model_worker多卡加载需要配置的参数
    #     # "gpus": None, # 使用的GPU，以str的格式指定，如"0,1"，如失效请使用CUDA_VISIBLE_DEVICES="0,1"等形式指定
    #     # "num_gpus": 1, # 使用GPU的数量
    #     # "max_gpu_memory": "20GiB", # 每个GPU占用的最大显存
    #
    #     # 以下为model_worker非常用参数，可根据需要配置
    #     # "load_8bit": False, # 开启8bit量化
    #     # "cpu_offloading": None,
    #     # "gptq_ckpt": None,
    #     # "gptq_wbits": 16,
    #     # "gptq_groupsize": -1,
    #     # "gptq_act_order": False,
    #     # "awq_ckpt": None,
    #     # "awq_wbits": 16,
    #     # "awq_groupsize": -1,
    #     # "model_names": LLM_MODELS,
    #     # "conv_template": None,
    #     # "limit_worker_concurrency": 5,
    #     # "stream_interval": 2,
    #     # "no_register": False,
    #     # "embed_in_truncate": False,
    #
    #     # 以下为vllm_worker配置参数,注意使用vllm必须有gpu，仅在Linux测试通过
    #
    #     # tokenizer = model_path # 如果tokenizer与model_path不一致在此处添加
    #     # 'tokenizer_mode':'auto',
    #     # 'trust_remote_code':True,
    #     # 'download_dir':None,
    #     # 'load_format':'auto',
    #     # 'dtype':'auto',
    #     # 'seed':0,
    #     # 'worker_use_ray':False,
    #     # 'pipeline_parallel_size':1,
    #     # 'tensor_parallel_size':1,
    #     # 'block_size':16,
    #     # 'swap_space':4 , # GiB
    #     # 'gpu_memory_utilization':0.90,
    #     # 'max_num_batched_tokens':2560,
    #     # 'max_num_seqs':256,
    #     # 'disable_log_stats':False,
    #     # 'conv_template':None,
    #     # 'limit_worker_concurrency':5,
    #     # 'no_register':False,
    #     # 'num_gpus': 1
    #     # 'engine_use_ray': False,
    #     # 'disable_log_requests': False
    #
    # },
}

FSCHAT_CONTROLLER = {
    "host": DEFAULT_BIND_HOST,
    "port": 28001,
    "dispatch_method": "shortest_queue",
}
