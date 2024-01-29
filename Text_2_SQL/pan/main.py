#from langchain.chains import create_sql_query_chain
#from .sql_database.query import create_sql_query_chain
from db import *
from llms import *

from langchain_experimental.sql import SQLDatabaseChain

glm2 = Chat_GLM2()
glm2_32k = Chat_GLM2_32K()
#chain = create_sql_query_chain(llm,db)

#defult
db_chain = SQLDatabaseChain.from_llm(glm2,db,verbose=True)
while 1:
    q = input("input : ")
    result = db_chain.run(q)




# while True:  
#     try:
#         question = input("请输入问题：")  
#         chain = create_sql_query_chain(llm, db)  
#         response = chain.invoke({"question": question})  
#         print("sql:",response)
#         print("查询结果:",db.run(response))

#     except Exception as e:
#         print("报错",str(e))
#         continue


#while True:  
    #question = input("请输入问题：")  
    #chain = create_sql_query_chain(llm, db)  
    #response = chain.invoke({"question": question})  
    #print("sql:",response)
    #print("查询结果:",db.run(response))


