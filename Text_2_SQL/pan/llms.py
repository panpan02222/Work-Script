import torch

from fastchat.model import load_model
from langchain.llms.base import LLM
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union

LLMs = {
    "vicuna" : "/home/Pan_BingHong/LLM/lmsysvicuna-13b-v1.5-16k/",
    "chat-glm" : "/home/Pan_BingHong/glm/input/ChatGLM6B6449/",
    "chat-glm2" : "/home/Pan_BingHong/glm/input/ChatGLM2-6B/",
    "chat-glm2-32k" : "/home/Pan_BingHong/LLM/THUDMchatglm2-6b-32k/",
    "llama2" : "/home/Pan_BingHong/llama2/Llama2-7b/",
    "wizardcoder" : "/home/Pan_BingHong/LLM/WizardCoder-Python-34B-V1.0/"
}


class Vicuna(LLM):
    max_token: int = 16000
    temperature: float = 0.8
    tokenizer: object = None
    model: object = None
    
    def __init__(self):
        super().__init__()
        
    @property
    def _llm_type(self) -> str:
        return "Vicuna"
            
    def load_model(self, llm_device="gpu",model_name_or_path=LLMs['vicuna']):
    # def load_model(self, llm_device="gpu",model_name_or_path=r"/home/Pan"):
        self.model, self.tokenizer = load_model(model_name_or_path, 'cuda', 1)
        print('load finished')

    def _call(self,prompt:str, stop: Optional[List[str]] = None):
        input_ids = self.tokenizer([prompt]).input_ids
        
        output_ids = self.model.generate(
                    torch.as_tensor(input_ids).to('cuda'), temperature=self.temperature,max_new_tokens=self.max_token
                    ) 
        output_ids = output_ids[0][len(input_ids[0]) :]
        response = self.tokenizer.decode(
            output_ids, skip_special_tokens=True, spaces_between_special_tokens=False
        )
        
        return response.replace('\\', '').split('\n')[0]

class Chat_GLM2(LLM):
    max_token: int = 2048
    temperature: float = 0.8
    tokenizer: object = None
    model: object = None
    
    def __init__(self):
        super().__init__()
        
    @property
    def _llm_type(self) -> str:
        return "Chat-GLM2"
            
    # def load_model(self, llm_device="gpu",model_name_or_path=None):
    def load_model(self, llm_device="gpu",model_name_or_path=LLMs['chat-glm2']):
        self.model, self.tokenizer = load_model(model_name_or_path, 'cuda', 1)
        print('load finished')

    def _call(self,prompt:str, stop: Optional[List[str]] = None):
        input_ids = self.tokenizer([prompt]).input_ids
        
        output_ids = self.model.generate(
                    torch.as_tensor(input_ids).to('cuda'), temperature=self.temperature,max_new_tokens=self.max_token
                    ) 
        output_ids = output_ids[0][len(input_ids[0]) :]
        response = self.tokenizer.decode(
            output_ids, skip_special_tokens=True, spaces_between_special_tokens=False
        )
        
        return response.replace('\\', '').split('\n')[0]
    
class Chat_GLM2_32K(LLM):
    max_token: int = 4096
    temperature: float = 0.8
    tokenizer: object = None
    model: object = None
    
    def __init__(self):
        super().__init__()
        
    @property
    def _llm_type(self) -> str:
        return "Chat_GLM2_32K"
            
    def load_model(self, llm_device="gpu",model_name_or_path=LLMs['chat-glm2-32k']):
        self.model, self.tokenizer = load_model(model_name_or_path, 'cuda', 1)
        print('load finished')

    def _call(self,prompt:str, stop: Optional[List[str]] = None):
        input_ids = self.tokenizer([prompt]).input_ids
        
        output_ids = self.model.generate(
                    torch.as_tensor(input_ids).to('cuda'), temperature=self.temperature,max_new_tokens=self.max_token
                    ) 
        output_ids = output_ids[0][len(input_ids[0]) :]
        response = self.tokenizer.decode(
            output_ids, skip_special_tokens=True, spaces_between_special_tokens=False
        )
        
        return response.replace('\\', '').split('\n')[0]