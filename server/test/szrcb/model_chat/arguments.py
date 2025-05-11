from dataclasses import dataclass, field
from typing import Optional

@dataclass
class InferenceArguments:
    '''
    模型参数
    '''
    model_name_or_path:str=field(
        metadata={"help": "Path to pretrained model or model identifier from huggingface.co/models"}
    )
    tokenizer_name: Optional[str] = field(
        default=None, metadata={"help": "Pretrained tokenizer name or path if not the same as model_name"}
    )
    temperature: float=field(
        metadata={"help":"模型推理时后的温度"}
    )
    top_p:float=field(
        metadata={"help":"模型推理时的top_p"}
    )
    max_new_tokens:int=field(
        metadata={"help":"模型推理时生成最大token数量"}
    )
    do_sample:bool=field(
        metadata={"help":"模型推理时是否随机采样"}
    )
    gpus:str=field(
        metadata={"help":"需要加载的gpus"}
    )
    