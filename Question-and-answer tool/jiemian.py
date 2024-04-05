# 渲染中间版
import base64
import streamlit as st
import os
import requests
import json
import re
import tempfile
import fitz

# 设计一个页面布局
st.set_page_config(layout="wide")

# 创建侧边栏
with st.sidebar:
    st.image(os.path.join('img', "baimoyun.png"))
    knowledge_base_list = ['人事知识库', '建发知识库', '佰模伝知识库',"BIM知识库"]
    model_knowledge = st.selectbox('选择知识库', knowledge_base_list)
    knowledge_base_dict = {
        "人事知识库": "personnel",
        "建发知识库": "context_text",
        "佰模伝知识库": "baimoyun",
        "BIM知识库":"context_text"
    }
    selected_knowledge_base = knowledge_base_dict[model_knowledge]

# 自定义函数用于处理文档名称
def get_doc_urls(docs_list):
    # 初始化一个空列表来存储所有找到的URL
    all_urls = []
    # 遍历docs_list中的每个元素
    for doc in docs_list:
        # 确保元素是字符串
        if isinstance(doc, str):
            # 使用正则表达式匹配URL
            urls = re.findall(r'http[s]?://[^\s]+', doc)
            # 将找到的URL添加到列表中
            all_urls.extend(urls)
    return all_urls


# 将图片转换成Base64，以便嵌入到CSS中
def get_image_as_base64(background_image_path):
    with open(background_image_path, 'rb') as image_file:
        data = base64.b64encode(image_file.read()).decode('utf-8')
    return data


# 主要布局分为两列：
col1, col2 = st.columns(2)
# 用于显示历史和对话记录
with col2:
    st.subheader('佰模伝AI知识库')
    user_input = st.text_input('请输入你的问题', key='user_input')
    send_button = st.button('发送')
    # 初始化response为None
    response = None
    if send_button and user_input.strip():
        try:
            # 发送请求到后端模型
            data = {
                "query": user_input,
                "knowledge_base_name": selected_knowledge_base,
                "top_k": 3,
                "score_threshold": 0.6,
                "stream": False,
                "model_name": "chatglm3-6b",
                "temperature": 0.7,
                "max_tokens": 0,
                "prompt_name": "default"
            }
            response = requests.post('http://127.0.0.1:7861/chat/knowledge_base_chat', json=data)
        except requests.RequestException as e:
            st.error('请求发送失败。错误信息：' + str(e))
            response = None  # 将response设置为None，以便后续代码不会尝试访问它的属性

        # 检查响应状态码
        if response is not None and response.status_code == 200:
            try:
                # 尝试去掉前缀并解析JSON
                response_text = response.text
                if response_text.startswith('data: '):
                    response_text = response_text[6:]  # 去掉前缀 "data: "
                answer_dict = json.loads(response_text)
                answer = answer_dict.get('answer')
                docs = answer_dict.get('docs', [])  # 获取参考文档列表
                print("docs", docs)
                # 使用自定义函数处理文档名称
                doc_names = get_doc_urls(docs)
                # 格式化输出结果
                # final_answer = f"{answer}\n以上回答参考自 {selected_knowledge_base} 知识库。\n参考文档：{', '.join(docs)}"
                final_answer = f"{answer}"
                st.write('知识库的回答:', final_answer)
            except json.JSONDecodeError as e:
                st.error('无法解析响应为JSON格式。错误信息：' + str(e))
        else:
            st.error(f'获取答案时出错。状态码：{response.status_code if response else "请求未发送"}')
    elif send_button:
        st.error('请正确输入您的问题。')
with col1:
    st.subheader('文档展示')
    # 创建一个可展开的区域，用户可以点击来展开或折叠内容
    with st.beta_expander("查看PDF文档", expanded=True):
        # 设置一个固定高度的容器，超出部分将显示滚动条
        st.markdown(
            """
            <style>
            .pdf-container {
                height: 700px;  # 可以根据需要调整高度
                overflow-y: auto;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        # 创建一个容器来显示PDF内容
        with st.container():
            if response is not None and response.status_code == 200:
                # ... 省略中间代码 ...
                # 如果PDF文件成功打开，渲染页面并显示
                if 'pdf_document' in st.session_state:
                    pdf_document = st.session_state['pdf_document']
                    pdf_pages = st.session_state['pdf_pages']
                    # 在一个固定高度的容器内显示PDF页面
                    st.markdown('<div class="pdf-container">', unsafe_allow_html=True)
                    for page_number in range(pdf_pages):
                        page = pdf_document[page_number]
                        pix = page.get_pixmap()
                        img_bytes = pix.tobytes("png")
                        st.image(img_bytes, caption=f"Page {page_number + 1}", width=600)
                    st.markdown('</div>', unsafe_allow_html=True)
                    pdf_document.close()
            else:
                st.image(os.path.join('img', "佰模伝AI智能平台(1).png"))


# 清理会话状态
st.session_state.pop('pdf_document', None)
st.session_state.pop('pdf_pages', None)