import requests
import streamlit as st

def chat_llm():
    st.title('大语言模型')

    #
    clear_button_placeholder = st.empty()

    # 创建表单
    with st.form(key='my_form'):
        query = st.text_input('输入提问内容')

        # 创建提交按钮
        submit_button = st.form_submit_button(label='发送问题')

    # 初始化 session_state
    if 'history' not in st.session_state:
        st.session_state['history'] = []

    if submit_button:
        url = 'http://127.0.0.1:7861/chat/fastchat'
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        data = {
        "model": "qianfan-api",
        "messages": [
        {
        "role": "user",
        "content": query,
        }
        ],
        "temperature": 1,
        "n": 1,
        "max_tokens": 2048,
        "stop": [],
        "stream": False,
        "presence_penalty": 0,
        "frequency_penalty": 0
        }
        response = requests.post(url, headers=headers, json=data)
        result = response.text

        # 将结果添加到历史记录中
        st.session_state['history'].append((query, result))

    # 显示历史记录
    for i, (q, res) in enumerate(st.session_state['history']):
        # 计算高度
        lines = res.count('\n') + 1
        height = min(lines * 10, 300)  # 设置最大高度为300
        st.text_area(f'输出结果 {i+1} - {q}', value=res, height=height)

    # 添加一个按钮来清除所有内容
    if clear_button_placeholder.button('清除所有内容'):
        st.session_state['history'] = []
        st.rerun()
