#part.1
import torch
import logging
from ..langchain import LLMChain
from ..langchain.llms.base import LLM
# from langchain import SQLDatabase, SQLDatabaseChain
from ..langchain import SQLDatabase
from ..langchain_experimental.sql import SQLDatabaseChain
from ..fastchat.model import load_model
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
            
    def load_model(self, llm_device="gpu",model_name_or_path="/home/Pan_BingHong/LLM/lmsysvicuna-13b-v1.5-16k/"):
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
            
    def load_model(self, llm_device="gpu",model_name_or_path="/home/Pan_BingHong/glm/input/ChatGLM2-6B/"):
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
class Chat_GLM2_32k(LLM):
    max_token: int = 20480
    temperature: float = 0.8
    tokenizer: object = None
    model: object = None
    
    def __init__(self):
        super().__init__()
        
    @property
    def _llm_type(self) -> str:
        return "Chat-GLM2-32k"
            
    def load_model(self, llm_device="gpu",model_name_or_path="/home/Pan_BingHong/LLM/THUDMchatglm2-6b-32k/"):
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
# model_path = r"/home/Pan_BingHong/glm/input/ChatGLM2-6B/"
# llm = Chat_GLM2()
# llm.load_model(model_name_or_path = model_path)

llm = Chat_GLM2_32k()

#part.4
db = SQLDatabase.from_uri("mysql+pymysql://llm2:dyy*1234@192.162.1.105:3306/wuzi")
local_chain = SQLDatabaseChain.from_llm(
    llm,
    db,
    #retrun_intermediate_steps = True,
    #use_query_checker = False
)

#part.5
# local_chain("what is zhangsan's total grades in the exam?")
# local_chain("")
# local_chain("How many tables are in the database")
# a=local_chain("who is zhangsan's dad? ")
# a=local_chain("who is zhangsan's mother? ")
# a=local_chain("whose son got a 100?please tell me this student's name.")
# a=local_chain("whose son got a 100?please tell me this student's name.")
# a=local_chain("what's the phone number of the parent of the student who got a 100?")
# print(a)

#part.6
local_chain 

def process_input():
    while 1:
        try:
            print("-"*30)
            user_input = input("请输入您的问题:")
            result = local_chain(user_input)
            print("-"*30)
            print(result)
        except Exception as e:
            print("发生错误",str(e))
            continue

process_input()





