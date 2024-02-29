import os
from langchain_community.utilities import SQLDatabase


os.environ["OPENAI_API_KEY"] = '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'
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

from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)
output=agent_executor.invoke(
    "列出注册资本超过100000万人民币的公司"
)
print(output)

examples = [
    {"input": "List all artists.", "query": "SELECT * FROM Artist;"},
    {
        "input": "Find all albums for the artist 'AC/DC'.",
        "query": "SELECT * FROM Album WHERE ArtistId = (SELECT ArtistId FROM Artist WHERE Name = 'AC/DC');",
    },
    {
        "input": "List all tracks in the 'Rock' genre.",
        "query": "SELECT * FROM Track WHERE GenreId = (SELECT GenreId FROM Genre WHERE Name = 'Rock');",
    },
    {
        "input": "Find the total duration of all tracks.",
        "query": "SELECT SUM(Milliseconds) FROM Track;",
    },
    {
        "input": "List all customers from Canada.",
        "query": "SELECT * FROM Customer WHERE Country = 'Canada';",
    },
    {
        "input": "How many tracks are there in the album with ID 5?",
        "query": "SELECT COUNT(*) FROM Track WHERE AlbumId = 5;",
    },
    {
        "input": "Find the total number of invoices.",
        "query": "SELECT COUNT(*) FROM Invoice;",
    },
    {
        "input": "List all tracks that are longer than 5 minutes.",
        "query": "SELECT * FROM Track WHERE Milliseconds > 300000;",
    },
    {
        "input": "Who are the top 5 customers by total purchase?",
        "query": "SELECT CustomerId, SUM(Total) AS TotalPurchase FROM Invoice GROUP BY CustomerId ORDER BY TotalPurchase DESC LIMIT 5;",
    },
    {
        "input": "Which albums are from the year 2000?",
        "query": "SELECT * FROM Album WHERE strftime('%Y', ReleaseDate) = '2000';",
    },
    {
        "input": "How many employees are there",
        "query": 'SELECT COUNT(*) FROM "Employee"',
    },
]

from langchain_community.vectorstores import FAISS
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings

example_selector = SemanticSimilarityExampleSelector.from_examples(
    examples,
    OpenAIEmbeddings(),
    FAISS,
    k=5,
    input_keys=["input"],
)
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
    SystemMessagePromptTemplate,
)

system_prefix = """您是一个旨在与SQL数据库交互的代理。
给定一个输入问题，创建一个语法正确的{方言}查询来运行，然后查看查询结果并返回答案。
除非用户指定他们希望获得的特定数量的示例，否则请始终将您的查询限制为最多{top_k}结果。
您可以按相关列对结果进行排序，以返回数据库中最有趣的示例。
切勿查询特定表格中的所有列，只需询问给定问题的相关列。
您可以访问与数据库交互的工具。
仅使用给定的工具。仅使用工具返回的信息来构建您的最终答案。
在执行之前，您必须仔细检查您的查询。如果您在执行查询时遇到错误，请重写查询并重试。
不要向数据库进行任何DML语句（INSERT、UPDATE、DELETE、DROP等）。
如果问题似乎与数据库无关，只需返回“我不知道”作为答案。
以下是一些用户输入及其相应的SQL查询的示例："""

few_shot_prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=PromptTemplate.from_template(
        "User input: {input}\nSQL query: {query}"
    ),
    input_variables=["input", "dialect", "top_k"],
    prefix=system_prefix,
    suffix="",
)
full_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate(prompt=few_shot_prompt),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ]
)

# Example formatted prompt
prompt_val = full_prompt.invoke(
    {
        "input": "How many arists are there",
        "top_k": 5,
        "dialect": "SQLite",
        "agent_scratchpad": [],
    }
)
print(prompt_val.to_string())

agent = create_sql_agent(
    llm=llm,
    db=db,
    prompt=full_prompt,
    verbose=True,
    agent_type="openai-tools",
)
agent.invoke({"input": "How many artists are there?"})