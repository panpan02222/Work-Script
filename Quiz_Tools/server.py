from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import json

class Item(BaseModel):
    content: str

wenxinyiyan_url = 'http://127.0.0.1:7861/chat/chat'
knowledge_chat_url = "http://localhost:7861/chat/knowledge_base_chat"

knowledge_dict = {
    # "安规知识问答": "angui",
    # "科技项目立项查重": "keji",
    # "调度应急处置": "diaodu",
    "通用规章制度": "zhidu",
    # "电网主设备技术标准": "jishu",
    # "营销2.0系统使用手册": "yingxiao"
}

knowledge_name_list = [
    # "安规知识问答",
    # "科技项目立项查重",
    # "调度应急处置",
    # "信息通信专业通用制度",
    # "电网主设备技术标准",
    # "营销2.0系统使用手册"
]

app = FastAPI()
#直接与大模型对话
def chat_wenxin(query):
    url = wenxinyiyan_url
    headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
    }
    data = {
    "model": "qianfan-api",
    "messages": [
    {
    "role": "user",
    "content": query
    }
    ],
    "temperature": 0.9,
    "n": 1,
    "max_tokens": 2048,
    "stop": [],
    "stream": False,
    "presence_penalty": 0,
    "frequency_penalty": 0
    }
    response = requests.post(url, headers=headers, json=data)
    result = response.text
    return result

#问题分类器
def classify(query):
    # content = f'你是一个文本分类器,目前共有“安规知识问答”、“科技项目立项查重”、“调度应急处置”，“信息通信专业通用制度”、“电网主设备技术标准”5类本地知识库。你的作用是将“{query}”这句话进行分类,最终告诉我这句话应属于哪个知识库,仅告诉我知识库的名称即可。最终回答的结果只能有“安规知识问答”、“科技项目立项查重”、“调度应急处置”，“信息通信专业通用制度”、“电网主设备技术标准”这5项中的一项。不允许出现多余的描述信息。'
    #问题分类提示词构建——方案一:
    content_0 = f"你是一个文本分类器，可以将输入的句子进行分类，\
                目前有6个类别，分别为“安规知识问答”、“科技项目立项查重”、“调度应急处置”、“信息通信专业通用制度”、“电网主设备技术标准”和“营销2.0系统使用手册”。\
                请分析“{query}”这句话，并告诉我它属于哪个分类。回答格式为“{query}”属于“某某”类。不要有多余的描述信息。"
    content_1 = f"我想要你帮我对用户输入的{query}进行判断。如果这个{query}的语义属于“规章制度”中的内容，请直接输出“规章制度”这4个文字。\
                否则请你用自己的能力来回答{query}这句话。并告诉用户“以上回答没有借助知识库中的内容，仅供参考”。"

    url = wenxinyiyan_url
    headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
    }
    wenxinyiyan_data = {"query": query, "prompt": "llm_chat"}
    response = requests.post(url, headers=headers, json=wenxinyiyan_data)
    knowledge_name = response.text
    #正则匹配方案
    # knowledge_name_re = re.findall(r'“(.+?)”', knowledge_name)[1]



    #文字相同匹配方案
    for key in knowledge_dict.keys():
        if key in knowledge_name:
            knowledge_name_str = key
            return knowledge_name_str
        
        else:
            return response.text

    # return knowledge_name_str



@app.post("/classify_and_chat")
async def classify_and_chat(item: Item):

    
    Knowledge_base_name_or_Anwser = classify(item.content)
    print("======================")
    print(knowledge_dict.keys())
    if Knowledge_base_name_or_Anwser not in knowledge_dict.keys():
        return Knowledge_base_name_or_Anwser

    url = knowledge_chat_url

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    data = {
        "query": item.content,
        "knowledge_base_name": Knowledge_base_name_or_Anwser,
        "top_k": 3,
        "score_threshold": 0.85,
        "history": [],
        "stream": False,
        "model_name": "qianfan-api",
        "temperature": 0.7,
        "prompt_name": "knowledge_base_chat",
        "local_doc_url": False
    }

    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    return result['answer']

