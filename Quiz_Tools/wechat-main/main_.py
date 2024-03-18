from pydantic import BaseModel
import requests
import json
from datetime import datetime
from flask import Flask, request, jsonify
import re

app = Flask(__name__)
  

wenxinyiyan_url = 'http://127.0.0.1:7861/chat/chat'
knowledge_chat_url = "http://127.0.0.1:7861/chat/knowledge_base_chat"

knowledge_dict = {
    "建发（客户设计标准）知识库": "Jianfa ",
    "人事知识库":"personnel",
    "BIM知识库": "bim",
    "佰模伝知识库":"BaiMoYun Infor"
}

#通过正则取出引用文档名称
def get_doc_name(docs):
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

def chat_llm(query, history=None,**kwargs):
    url = wenxinyiyan_url
    data = {"query":query,"pormpt":"llm_chat", "history":history, "history_len":-1}
    print("chat llm api", data)
    response = requests.post(url, json=data)
    response.raise_for_status()
    # 提取 "text" 字段的内容
    json_string = response.text.split("data: ", 1)[1]
    result = json.loads(json_string)
    answer = result["text"]
    print("大模型输出结果为: \n", answer)
    # 将结果转换为 JSON 格式
    response_data = {
        "usage": {"total_tokens": len(answer), "completion_tokens": len(answer)},
        "choices": [{"message": {"content": answer}}]
    }
    return jsonify(response_data)


def chat_knowledge(query, knowledge_name="context_text", history=None,**kwargs):
    print("chat knowlage api history",history)
    url = knowledge_chat_url
    data = {
        "query": query,
        "knowledge_base_name": knowledge_name,
        "history": history,
        "history_len":-1,
        "model_name": "chatglm3-6b",
        "prompt_name": "default"
    }
    print(data)
    print(query)
    print(knowledge_name)
    try:
        # Send a request to the knowledge chat API
        response = requests.post(url, json=data)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Process the response
        json_string = response.text.split("data: ", 1)[1]
        result = json.loads(json_string)
        answer = result["answer"]
        answer = answer.encode('utf-8').decode('utf-8')

        # Check if there are any referenced documents
        doc_len = len(result["docs"])
        print("引用文档数量为：", doc_len)
        if doc_len > 0:
            docs_names = get_doc_name(result["docs"])
        answer = answer + f"\n以上回答参考自 {get_keys_from_value(knowledge_dict,knowledge_name)} 知识库\n以上回答参考自 {docs_names}."
        print("知识库输出结果为: \n", answer)

        response_data = {
            "usage": {"total_tokens": len(answer), "completion_tokens": len(answer)},
            "choices": [{"message": {"content": answer}}]
        }
        return jsonify(response_data)
    except requests.exceptions.RequestException as e:
        answer = chat_llm(query, history)
        return answer
    except Exception as e:
        # Handle other unexpected errors
        print(f"Unexpected error: {e}")
        return jsonify({"error": "Unexpected error"}), 500

#问题分类器
def classify(query):
    print(30*"*","启动问题分类器",30*"*")
    content = f"""
    "你是一名人工智能助手，下面是不同的知识库及其描述，你需要根据‘{query}’话，分析它的语义并选择合适的知识库。\
    “人事知识库”：该知识库中包含佰模伝公司简介以及中各个部门办公室内的管理规章制度以及管理办法等资料，通过人事知识库我们可以清楚的了解到公司的发展历程以及确保每个人都了解并遵守相应的规定。\
    “建发知识库”: 该知识库中包含建发房产中，关于净高、梁高、设计要求、，通过该知识库我们了解并遵守相应的设计规程，从而很好的找到对应的一些数值。\
    “佰模伝知识库”：该知识库中包含佰模伝公司统一社会信用代码，类型，法定代表人，经营范围，注册资本，成立的时间，营业期限。住所，登记机关，登记时间，通过该知识库我们可以了解到佰模伝公司的基本信息。\
    "BIM知识库" : 该知识库中包含全国各省市BIM计费标准，关于发布日期，来自于哪个省市，各个省市的计费标准内容，以及来源地区，以及标准名称，通过该知识库我们可以很好的了解到各个省市对于BIM计费标准。\
     输出结果中必须输出对应的知识库名称，例如“规章制度知识库”，“安全规程知识库”,不需要有额外的信息。请注意如果没有合适的知识库，请用你自己的能力来回答'{query}'这句话。\
    【用户问题】{query}
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
      
@app.route('/v1/chat/completions', methods=['POST'])
def api_adapter():
    incoming_data = request.json
    messages = incoming_data['messages']
    print("aaaaaaaaaaaaaaaaaaaa")
    print(messages)
    query = messages[-1]['content']
    print("query",query)
    history = messages[-6:]  # Keep the last 5 turns of conversation
    print("history",history)
    knowledge_base_name = classify(query)
    answer = chat_knowledge(query, knowledge_base_name, history)
    return answer

if __name__ == '__main__':
    app.run(debug=True, port=5004)

    


