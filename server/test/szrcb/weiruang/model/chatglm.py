# -*- coding:UTF-8 -*-
import os
import torch
from langchain_core.language_models.llms import LLM
from typing import Any, List, Mapping, Optional,Coroutine,Dict,AsyncIterator,Union
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.callbacks import AsyncCallbackManagerForLLMRun
from transformers import (
    AutoTokenizer,
    AutoModel,
)
from transformers import TextIteratorStreamer
from threading import Thread

class ChatGLM3_LLM(LLM):
    model:AutoModel=None
    tokenizer: AutoTokenizer = None
    history:List[Dict]=[]
    max_history_len:int=3
    
    def __init__(self,model_path:str,history_len:int,**kwargs):
        super().__init__()
        self.max_history_len=history_len
        print(f"正在加载*{self._llm_type}*模型")
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        self.model = AutoModel.from_pretrained(model_path,trust_remote_code=True).half().cuda()
        self.model.eval()
        print(f"*{self._llm_type}*模型加载成功")
        

    @property
    def _llm_type(self) -> str:
        return "chatglm3"
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        temperature=0.95,
        top_p=0.7,
        max_new_tokens=1024,
        num_beams=1,
        do_sample=True,
        role="user",
        **kwargs: Any,
    ) -> str:
        if self.max_history_len<=0:
            history=[]
        else:
            history=self.history[-self.max_history_len:]

        gen_kwargs = {"max_length": max_new_tokens, "num_beams": num_beams, "do_sample": do_sample, "top_p": top_p,
                      "temperature": temperature, **kwargs}

        inputs=self.tokenizer.build_chat_input(prompt,self.history)
        inputs = inputs.to(self.model.device)
        eos_token_id = [self.tokenizer.eos_token_id, self.tokenizer.get_command("<|user|>"),
                        self.tokenizer.get_command("<|observation|>")]
        outputs = self.model.generate(**inputs, **gen_kwargs, eos_token_id=eos_token_id)
        outputs = outputs.tolist()[0][len(inputs["input_ids"][0]):-1]
        history.append({"role": role, "content": prompt})
        response, history = self.process_response(response, history)
        self.history=history
        return response
    

    async def _acall(self,
                    prompt: str,
                    messages:List[Dict],
                    stop: Union[List[str] , None] = None, 
                    run_manager: Union[AsyncCallbackManagerForLLMRun , None] = None,
                    temperature=0.95,
                    top_p=0.7,
                    max_new_tokens=1024,
                    num_beams=1,
                    do_sample=True,
                    role="user",
                    **kwargs: Any):
        if self.max_history_len<=0:
            history=[]
        else:
            history=self.history[-self.max_history_len:]
        if messages and len(messages)>0:
            history=messages[:-1]
            prompt=messages[-1]["content"]
        else:
            return None
        # inputs=self.tokenizer.build_chat_input(prompt,history)
        inputs = self.tokenizer.apply_chat_template(messages,
                                       add_generation_prompt=True,
                                       tokenize=True,
                                       return_tensors="pt",
                                       return_dict=True
                                       )
        
        inputs = inputs.to(self.model.device)
        # eos_token_id = [self.tokenizer.eos_token_id, self.tokenizer.get_command("<|user|>"),
        #                 self.tokenizer.get_command("<|observation|>")]
        eos_token_id = [self.tokenizer.eos_token_id]
        streamer = TextIteratorStreamer(self.tokenizer,skip_special_tokens=True,skip_prompt=True)
        gen_kwargs = {"inputs":inputs,"streamer":streamer,"max_length": max_new_tokens, "num_beams": num_beams, "do_sample": do_sample, "top_p": top_p,
                "temperature": temperature, "eos_token_id":eos_token_id,**kwargs}
        gen_kwargs=dict(
            inputs,
            streamer=streamer,
            max_length=max_new_tokens,
            num_beams=num_beams,
            do_sample=do_sample,
            top_p=top_p,
            temperature=temperature,
            eos_token_id=eos_token_id
        )
        thread = Thread(target=self.model.generate, kwargs=gen_kwargs)
        thread.start()
        # 流式输出
        content=""
        for new_text in streamer:
            if run_manager:
                await run_manager.on_llm_new_token(new_text)
            content+=new_text
        history.append({"role": role, "content": prompt})
        response, history = self.model.process_response(content, history)
        self.history=history
        return response
         
    def calculate_num_tokens(self,text:str):
        if text is None or len(text)<=0:
            return 0
        return len(self.tokenizer(text))

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"model": self.model.__class__.__name__,"tokenizer":self.tokenizer.__class__.__name__}