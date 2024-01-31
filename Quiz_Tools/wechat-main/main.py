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
    "办公资料": "context_text",
    "国际安全":"samples",
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

# #無法回答的情況直接調用大模型
# def chat_llm(query):
#     url = wenxinyiyan_url
#     data = {"query":query,"pormpt":"llm_chat"}
#     response = requests.post(url, json=data)
#     response.raise_for_status()
#     # 解析返回的数据
#     data = json.loads(response.text)
#     # 提取 "text" 字段的内容
#     text_content = data.get("text", "")
#     print("大模型输出结果为: \n", text_content)
#     # 将结果转换为 JSON 格式
#     response_data = {
#         "usage": {"total_tokens": len(text_content), "completion_tokens": len(text_content)},
#         "choices": [{"message": {"content": text_content}}]
#     }
#     return jsonify(response_data)
def chat_llm(query):
    url = wenxinyiyan_url
    data = {"query":query,"pormpt":"llm_chat"}
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

def chat_knowledge(query, knowledge_name="context_text"):
    url = knowledge_chat_url
    data={"query":query,"knowledge_base_name":knowledge_name}
    print(query)
    print(knowledge_name)
    try:
        # Send a request to the knowledge chat API
        response = requests.post(knowledge_chat_url, json=data)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Process the response
        json_string = response.text.split("data: ", 1)[1]
        result = json.loads(json_string)
        answer = result["answer"]
        answer = answer.encode('utf-8').decode('utf-8')
        #增加判断是否出现引用文档(当前设定为3)
        doc_len = len(result["docs"])
        print("引用文档数量为：",doc_len)
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
        answer = chat_llm(query)
        return answer
        # return answer
    except Exception as e:
        # Handle other unexpected errors
        print(f"Unexpected error: {e}")
        return jsonify({"error": "Unexpected error"}), 500


#问题分类器
def classify(query):
    print(30*"*","启动问题分类器",30*"*")
    content = f"""
    "你是一名人工智能助手，下面是不同的知识库及其描述，你需要根据‘{query}’话，分析它的语义并选择合适的知识库。\
    “办公资料”：该知识库中包含佰模伝公司中各个部门办公室内的管理规章制度以及管理办法等资料，通过该知识库我们可以确保每个人都了解并遵守相应的规定。\
    “国际安全”: 该知识库中包含国家电网公司中，关于输电、配电、变电等方面的安全规程，通过该知识库我们了解并遵守相应的安全规程，从而预防和减少事故的发生。\
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
    query = incoming_data['messages'][-1]['content']
    knowledge_base_name = classify(query)
    answer = chat_knowledge(query, knowledge_base_name)
    return answer

if __name__ == '__main__':
    app.run(debug=True, port=5002)

    


