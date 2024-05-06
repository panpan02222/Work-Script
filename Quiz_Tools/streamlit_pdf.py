import streamlit as st
import pandas as pd
import base64
import os
import requests
import json
import re
import tempfile
import fitz
import datetime
from openpyxl import load_workbook

# 设计一个页面布局
st.set_page_config(layout="wide")

# 创建侧边栏
with st.sidebar:
    st.image(os.path.join('img', "baimoyun.png"))
    knowledge_base_list = ['人事知识库', '建发知识库', '佰模伝知识库',"BIM知识库","建发知识库2"]
    model_knowledge = st.selectbox('选择知识库', knowledge_base_list)
    knowledge_base_dict = {
        "人事知识库": "personnel",
        "建发知识库": "Jianfa",
        "佰模伝知识库": "BaiMoYun Infor",
        "BIM知识库":"BIM",
        "建发知识库2":"ssd"
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

#保存Excel的函数，包括用户访问时间，用户访问IP,用户的问题，大模型的回答
def save_to_excel(question,answer,sava_file_path='quetion_answer.xlsx'):
    #获取当前时间戳
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #从Flask的request对象中获取用户的IP
    user_ip ='Unknow'
    #创建一个新的DataFrame来存储数据
    data = {
        "Timestamp":[timestamp],       #获取用户访问时间
        "User_IP":[user_ip],           #获取用户IP
        "user_Question":[question],    #获取用户的问题
        "AI_Answer":[answer],}         #获取大模型的回答
    df = pd.DataFrame(data)
    try:
        # 如果文件存在，追加到现有文件；如果不存在，创建新文件
        if os.path.exists(sava_file_path):
            exciting_data = pd.read_excel(sava_file_path)
            combined_data = pd.concat([exciting_data,df])
        else:
            #文件已存在，使用ExcelWriteer以追加模式写入
            combined_data = df
            #保存DataFrame到excel文件，不包含索引
        combined_data.to_excel(sava_file_path,index=True)
    except Exception as e:
        print(f"保存excel时发生错误:{str(e)}")


# 存储对话历史
conversation_history = []
# 主要布局分为两列
col1, col2 = st.columns(2)
# 用于显示历史和对话记录
with col2:
    st.subheader('佰模伝AI知识库')
    # chat_input_placeholder = "请输入对话内容，换行请使用Shift+Enter。输入/help查看自定义命令 "
    user_input = st.text_input('请输入你的问题', key='user_input')
    send_button = st.button('发送')
    response = None
    if send_button and user_input.strip():
        try:
            # 发送请求到后端模型
            data = {
                "query": user_input,
                "knowledge_base_name":selected_knowledge_base,
                "top_k": 3,
                "score_threshold": 0.6,
                "history":conversation_history,
                "stream": False,
                "model_name": "Qwen-72B-Chat-Int4",
                "temperature": 0.7,
                "max_tokens": None,
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
                response_text = answer
                # 使用自定义函数处理文档名称
                doc_names = get_doc_urls(docs)
                # final_answer = f"{answer}\n以上回答参考自 {selected_knowledge_base} 知识库。\n参考文档：{', '.join(docs)}"
                #streamlit页面上显示AI回答格式化输出结果
                final_answer = f"{answer}"
                st.write('佰模伝AI知识库回答:', final_answer)
                if response_text:
                    #调用保存到Excel的函数
                    save_to_excel(user_input,response_text)
                else:
                    st.error("相应文本为空，无法保存到Excel中去")
            except json.JSONDecodeError as e:
                st.error('无法解析响应为JSON格式。错误信息：' + str(e))
        else:
            st.error(f'获取答案时出错。状态码：{response.status_code if response else "请求未发送"}')
    elif send_button:
        st.error('请正确输入您的问题。')


with col1:
    st.subheader('文档展示区')
    if response is not None and response.status_code == 200:
        try:
            # 尝试去掉前缀并解析JSON
            response_text = response.text
            if response_text.startswith('data: '):
                response_text = response_text[6:]  # 去掉前缀 "data: "
            answer_dict = json.loads(response_text)
            answer = answer_dict.get('answer')
            docs = answer_dict.get('docs', [])  # 获取参考文档列表
            print("尝试获取的URL:", docs)
            # 使用自定义函数处理文档中的URL
            doc_urls = get_doc_urls(docs)
            if doc_urls:
                url_string = doc_urls[0]
                url_string = url_string[:-1]
                doc_urls = url_string
            else:
                print("列表为空，没有URL可以提取。")

            # 检查是否有URL，并且是有效的PDF链接
            if doc_urls.endswith('.pdf'):
                # 从URL下载PDF文件
                response = requests.get(doc_urls)
                if response.status_code == 200:
                    # 创建一个临时文件来保存PDF数据
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmpfile:
                        tmpfile.write(response.content)
                        tmpfile_path = tmpfile.name

                    try:
                        # 使用PyMuPDF读取PDF文件
                        pdf_document = fitz.open(tmpfile_path)
                    except Exception as e:
                        st.error("无法打开PDF文件: " + str(e))
                    else:
                        # 如果PDF文件成功打开，渲染页面并显示
                        st.session_state['pdf_document'] = pdf_document
                        st.session_state['pdf_pages'] = len(pdf_document)

                        # 创建一个数组
                        list = []
                        imgListStr = ''
                        # 遍历所有页面并显示
                        for page_number in range(st.session_state['pdf_pages']):
                            # 从PDF文档中获取指定页面
                            page = pdf_document[page_number - 1]
                            # 渲染页面为图片
                            pix = page.get_pixmap()
                            # 将图片转换为PNG格式的字节
                            img_bytes = pix.tobytes("png")
                            img_base64 = 'data:image/png;base64,' + base64.b64encode(img_bytes).decode('utf-8')
                            list_a = list.append(img_base64)

                        for i in list:
                            imgListStr += f"<img src='{i}' width='560'>"
                        st.markdown(
                            f'<div style="text-align: center;height:1000px;overflow-y: scroll">{imgListStr}</div>',
                            unsafe_allow_html=True)
                        # 关闭PDF文档
                        pdf_document.close()
                        # 删除临时文件
                        os.remove(tmpfile_path)
                else:
                    st.error("未找到有效的PDF链接。")

        except json.JSONDecodeError as e:
            st.error('无法解析响应为JSON格式。错误信息：' + str(e))
        except Exception as e:
            st.error(f'处理PDF时发生错误：{str(e)}')
    else:
        st.image(os.path.join('img', "baimoun_.png"))

# 清理会话状态
st.session_state.pop('pdf_document', None)
st.session_state.pop('pdf_pages', None)



