import streamlit as st
import requests
import os
from quiz_chat.chat_llm import chat_llm
from quiz_chat.chat_knowledge import chat_knowledge
from quiz_chat.chat_universal import chat_universal


# 加载前端页面
def index():
    with open('index.html', 'r',encoding='utf-8') as f:
        index_html = f.read()
    st.markdown(index_html, unsafe_allow_html=True)



if __name__ == '__main__':

    st.set_page_config(
    page_title = "知识问答工具",
    page_icon = ":smile:",
    layout = 'wide',
    initial_sidebar_state = 'auto',
    menu_items = None
)
    with st.sidebar:
        st.image("static/电科院.png",use_column_width=True)
    app_list = ['']
    selected_app = st.sidebar.selectbox('选择知识库', app_list)
    
    # 增加切换app清空页面历史
    if 'selected_app' in st.session_state:
        if st.session_state['selected_app'] != selected_app:
            st.session_state['history'] = []
    st.session_state['selected_app'] = selected_app

    if selected_app == '首页':
        index()
    elif selected_app == "":
        chat_llm()
    elif selected_app == "":
        chat_universal()
    else:
        chat_knowledge(selected_app)
