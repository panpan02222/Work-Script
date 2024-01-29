import requests
import streamlit as st

def chat_knowledge(knowledge_base_name):
    st.title(f'{knowledge_base_name}知识问答')

        # 创建表单
    with st.form(key='my_form'):
        query = st.text_input('输入提问内容')
        # 创建提交按钮
        submit_button = st.form_submit_button(label='发送问题')

    # 初始化 session_state
    if 'history' not in st.session_state:
        st.session_state['history'] = []
    # 根据选择的app来切换不同的知识库
    app_to_kb_name = {
        "财务税政" : "caiwu",
        "安全规程" : "angui",
        "通用规章制度" : "zhidu",
        "雄安调度专业" : "diaodu",
        "保定调度专业" : "baoding_diaodu",
        "电力行业主设备检修" : "shebei",
        "营销2.0系统使用手册" : "营销"
    }


    if submit_button:
        url = 'http://127.0.0.1:7861/chat/knowledge_base_chat'
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        data = {
            "query": query,
            "knowledge_base_name": app_to_kb_name[knowledge_base_name],
            "top_k": 3,
            "score_threshold": 0.5,
            "history": [],
            "stream": False,
            "model_name": "qianfan-api",
            "temperature": 0.9,
            "prompt_name": "knowledge_base_chat",
            "local_doc_url": False
        }
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        print(result)
        st.session_state['history'].append(str(result['answer']))
        # st.text_area('输出结果', value=result['answer'], height=400)
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
