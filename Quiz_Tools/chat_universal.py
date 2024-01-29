import requests
import streamlit as st

def chat_universal():
    st.title('e点智寻-百科类问题')

    # 创建表单
    with st.form(key='my_form'):
        query = st.text_input('输入提问内容')

        # 创建提交按钮
        submit_button = st.form_submit_button(label='发送问题')

    # 初始化 session_state
    if 'history' not in st.session_state:
        st.session_state['history'] = []

    if submit_button:
        url = 'http://127.0.0.1:7861/chat/fastchat' #改这里
        data = {
        "content": query,
        }
        response = requests.post(url, json=data)
        result = response.text

        # 将结果添加到历史记录中
        st.session_state['history'].append(result)

    # 显示历史记录
    for i, res in enumerate(st.session_state['history']):
        # 计算高度
        lines = res.count('\n') + 1
        height = min(lines * 20, 500)  # 设置最大高度为300
        st.text_area(f'输出结果 {i+1}', value=res, height=height)

    # 添加一个按钮来清除所有内容
    if st.button('清除所有内容'):
        st.session_state['history'] = []
        st.rerun()
