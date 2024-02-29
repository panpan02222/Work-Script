import os
from langchain_community.utilities import SQLDatabase
import mysql.connector
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.agent_toolkits import create_sql_agent


# os.environ["OPENAI_API_KEY"] = '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'
# 创建到MySQL数据库的连接
connection_string = (
    "mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}"
)

# 替换以下占位符为你的MySQL数据库的实际信息
username = "root"
password = "123456"
host = "localhost"  # 或者你的数据库服务器地址
port = "3306"  # MySQL默认端口
database = "company"

# 使用提供的连接信息构建连接字符串
connection_uri = connection_string.format(
    username=username, password=password, host=host, port=port, database=database
)

# 初始化SQLDatabase对象
db = SQLDatabase.from_uri(connection_uri)

# 现在你可以使用db对象来查询MySQL数据库了
print(db.dialect)
print(db.get_usable_table_names())
print(db.run("SELECT * FROM company LIMIT 10;"))

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
chain = create_sql_query_chain(llm, db)
response = chain.invoke({"question": "How many company"})
print(db.run(response))

# chain.get_prompts()[0].pretty_print()

execute_query = QuerySQLDataBaseTool(db=db)
write_query = create_sql_query_chain(llm, db)
chain = write_query | execute_query
print(chain.invoke({"question": "有多少家公司"}))


answer_prompt = PromptTemplate.from_template(
    """鉴于以下用户问题、相应的SQL查询和SQL结果，请回答用户问题。

Question: {question}
SQL Query: {query}
SQL Result: {result}
Answer: """
)

answer = answer_prompt | llm | StrOutputParser()
chain = (
    RunnablePassthrough.assign(query=write_query).assign(
        result=itemgetter("query") | execute_query
    )
    | answer
)

print(chain.invoke({"question": "有多少家公司"}))

agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)
output=agent_executor.invoke(
    {
        "input": "列出注册资本超过100000万人民币的公司"
    }
)
print(output)