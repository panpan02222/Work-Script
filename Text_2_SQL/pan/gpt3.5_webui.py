import gradio as gr
from langchain.chains import create_sql_query_chain
from db import *
from llms import *
from mdtex2html import md_to_html


llm = Chat_GLM2_32K()

def chatbot(question):
    try:
        chain = create_sql_query_chain(llm, db)  
        response = chain.invoke({"question": question})  
        return md_to_html(response)
    except:
        return "抱歉，我无法回答这个问题。"

iface = gr.Interface(fn=chatbot, inputs="text", outputs=gr.outputs.HTML(), title="GPT-3.5 机器人聊天室", 
                     description="请输入您的问题，机器人将会给出回答。注意：请勿询问与中国法律法规不符的问题。")

iface.launch(host='192.162.1.103', port=1222)
