from langchain.chains import create_sql_query_chain  
from db import *  
from llms import *  
import gradio as gr  
import mdtex2html  
  
def create_interface():  
    llm = Chat_GLM2_32K()  
    chain = create_sql_query_chain(llm, db)  
  
    interface = gr.Interface(fn=lambda question: chain.invoke({"question": question}),   
                            inputs="text",   
                            outputs="text")  
    return interface  
  
def launch_server():  
    interface = create_interface()  
    interface.launch(share=True,   
                     debug=True,   
                     port=1222,   
                     hostname="192.162.1.103")  
  
if __name__ == "__main__":  
    launch_server()