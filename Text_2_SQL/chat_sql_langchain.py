#part.1
import torch
import logging

from langchain import LLMChain
from langchain.llms.base import LLM
from langchain import SQLDatabase, SQLDatabaseChain

from fastchat.model import load_model

from typing import Any, Dict, List, Mapping, Optional, Tuple, Union


#part.2
class Vicuna(LLM):
    max_token: int = 2048
    temperature: float = 0.8
    tokenizer: object = None
    model: object = None
    
    def __init__(self):
        super().__init__()
        
    @property
    def _llm_type(self) -> str:
        return "Vicuna"
            
    def load_model(self, llm_device="gpu",model_name_or_path=None):
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

#part.3
model_path = r"/home/model/vicuna-13b/"
llm = Vicuna()
llm.load_model(model_name_or_path = model_path)


#part.4

local_chain("How many tables are in the database")

