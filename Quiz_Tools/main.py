import streamlit as st
import requests
import os
from quiz_chat.chat_llm import chat_llm
from quiz_chat.chat_knowledge import chat_knowledge
from quiz_chat.chat_universal import chat_universal



def local_css(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def app():
    local_css("static/background.css")
    st.title("My Streamlit App with a Background Image")

# 加载前端页面
def index():
    with open('index.html', 'r',encoding='utf-8') as f:
        index_html = f.read()
    st.markdown(index_html, unsafe_allow_html=True)



if __name__ == '__main__':
    with st.sidebar:
        st.image("static/电科院.png",use_column_width=True)
    app_list = ['首页', "大语言模型","e点智寻",'财务税政','安全规程','通用规章制度','雄安调度专业', '保定调度专业', '电力行业主设备检修', '营销2.0系统使用手册']
    selected_app = st.sidebar.selectbox('选择知识库', app_list)
    
    # 检查是否已经选择了一个应用
    if 'selected_app' in st.session_state:
        # 如果选择的应用改变了，清空历史记录
        if st.session_state['selected_app'] != selected_app:
            st.session_state['history'] = []
    # 更新当前选择的应用
    st.session_state['selected_app'] = selected_app

    if selected_app == '首页':
        index()
    elif selected_app == "大语言模型":
        chat_llm()
    elif selected_app == "e点智寻":
        chat_universal()
    else:
        chat_knowledge(selected_app)
