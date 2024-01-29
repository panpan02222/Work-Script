#接通本地数据库
import pymysql
# import mysql.connector
from langchain.utilities import SQLDatabase

# mydb = mysql.connector.connector(
#     host = "192.162.1.105",
#     port = "3306",
#     user = "llm2",
#     password = "dyy*1234",
#     database = "student"
# )
# db = SQLDatabase(mydb)

db = SQLDatabase.from_uri("mysql+pymysql://llm2:dyy*1234@192.162.1.105:3306/student")
# db = SQLDatabase.from_uri("jdbc+pymysql://llm2:dyy*1234@192.162.1.105:3306/student")

#调用本地大模型
from transformers import AutoTokenizer, AutoModel
from typing import Any, List

class chatGLM():
    def __init__(self, model_name, quantization_bit=4) -> None:
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        model = AutoModel.from_pretrained(model_name, trust_remote_code=True).half().cuda().eval()
        self.model = model.quantize(quantization_bit)

    def __call__(self, prompt) -> Any:
        response, _ = self.model.chat(self.tokenizer , prompt) # 这里演示未使用流式接口. stream_chat()
        return response
llm =  chatGLM(model_name=r"/home/Pan_BingHong/glm/input/ChatGLM2-6B/")




#server
#from langchain_experimental.sql import SQLDatabaseChain
from sql.base import SQLDatabaseChain
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

#chat
db_chain.run("who is zhangsan's dad?")

