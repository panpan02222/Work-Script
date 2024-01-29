from langchain import SQLDatabase


db = SQLDatabase.from_uri("mysql+pymysql://llm2:dyy*1234@192.162.1.105:3306/beijing_xiaoxue")
#db = SQLDatabase.from_uri("mysql+pymysql://llm2:dyy*1234@192.162.1.105:3306/wuzi")



