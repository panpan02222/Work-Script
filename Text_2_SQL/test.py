#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
 * @Author: BingHong Pan 
 * @Date: 2024-03-20 17:46:38 
 * @Last Modified by:   BingHong Pan 
 * @Last Modified time: 2024-03-20 17:46:38 
 */
'''

# pip install --upgrade --quiet  langchain langchain-community langchain-openai
# pip install qianfan

from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
import os
from langchain_community.llms import QianfanLLMEndpoint


# 调用文心一言
os.environ["QIANFAN_AK"] = ""
os.environ["QIANFAN_SK"] = ""

llm = QianfanLLMEndpoint(streaming=True)
res = llm("你好, 你是谁?")
print(res)


# 连接数据库
db = SQLDatabase.from_uri("mysql+pymysql://username:password@127.0.0.1:3306/databases")
print(db.dialect)
print(db.get_usable_table_names())

# # 利用大模型和数据库进行chain
chain = create_sql_query_chain(llm, db)


question = input("请输入你要查询的问题 : ")
response = chain.invoke({"question": question})
response
# 使用SQL进行查询
db.run(response)