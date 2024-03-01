from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import json
import uvicorn
from datetime import datetime
import pandas as pd

from logging_module import LoggingManager  
  


class InputMessage(BaseModel):
    content: str

anquan_words = ["安全","安规","登高","危险","断电"]

wenxinyiyan_url = 'http://192.162.1.117:7861/chat/chat'
knowledge_chat_url = "http://192.162.1.117:7861/chat/knowledge_base_chat"
knowledge_dict = {

}

#通过正则取出引用文档名称
def get_doc_name(docs):
    import re
    results = []
    for doc in docs:
        matches = re.findall(r'\[(.*?)\]',doc)
        if len(matches) >= 2:
            results.append(matches[1])
    return results

#获取知识库的中文名称
def get_keys_from_value(d,value):
    keys=[]
    for k,v in d.items():
        if v ==value:
            keys.append(k)
    return keys

app = FastAPI()
#無法回答的情況直接調用大模型
def chat_llm(query):
    url = wenxinyiyan_url
    data = {"query":query,"pormpt":"llm_chat"}
    response = requests.post(url, json=data)
    result = response.text
    return result

#调用知识库问答
def chat_knowledge(query,knowledge_name):
    url = knowledge_chat_url
    data={"query":query,"knowledge_base_name":knowledge_name}
    response = requests.post(url, json=data)
    result = response.json()
    try:
        answer = result["answer"]
    except Exception as e:
        print("没有找到问题对应的知识库")
        result = chat_llm(query)
        return result
    if "无法" in answer:
        result = chat_llm(query)
        # result = result + "以上回答没有借助知识库中的内容，仅供参考。"
        return result
    #增加判断是否出现引用文档(当前设定为3)
    doc_len = len(result["docs"])
    print("引用文档数量为：",doc_len)
    if doc_len > 0:
        docs_names = get_doc_name(result["docs"])
        print("引用文档为：",docs_names)
    if doc_len == 0:
        return answer
    Answer = answer +f"\n以上内容来自{get_keys_from_value(knowledge_dict,knowledge_name)}"
    return Answer

#问题分类器
def classify(query):
    print(30*"*","启动问题分类器",30*"*")
    content = f"""

    """
    url = wenxinyiyan_url
    headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
    }
    data = {"query": content}
    response = requests.post(url, headers=headers, json=data)

    classify_results = response.text

    for key in knowledge_dict.keys():
        if key in classify_results:
            knowledge_name = key
            knowledge_name_str = knowledge_name.replace(key,knowledge_dict[key])
            print("知识库的名称经过问题分类判断后,得出用户的问题属于:",knowledge_name_str)
            return knowledge_name_str

@app.post("/classify_and_chat")
def classify_and_chat(item:InputMessage):

    knowledge_base_name = classify(item.content)     
    answer = chat_knowledge(item.content,knowledge_base_name)
    print("本次执行【输入内容】为:",item.content)
    print("本次执行调用【知识库】为:",knowledge_base_name)
    print("本次执行的【回答结果】为："'\n',answer)
    print(30*"*","本次知识问答完毕",30*"*")

    # 创建日志管理器实例  
 
    logging_manager = LoggingManager('classify_and_chat.log') 
    logging_manager.setup_handler()  # 仅在第一次使用时调用此方法来设置日志处理器   
    logging_manager.log_input(item.content)  
    logging_manager.log_answer(answer.encode('utf-8').decode('utf-8'))
    return answer

if __name__ == '__main__':
   uvicorn.run("server:app",host='192.162.1.117',port=2222,debug=True,log_level=ERROE)