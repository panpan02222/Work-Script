#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   main.py
@Time    :   2024/03/21 22:03:33
@Author  :   pan binghong 
@Email   :   19909442097@163.com
@description   :  
'''

import warnings
from langchain_elasticsearch import ElasticsearchStore
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import UnstructuredFileLoader

warnings.filterwarnings('ignore')

# 指定文件路径
file_path = r"Text_2_SQL\推荐系统\data01.json"
# 创建UnstructuredFileLoader实例
loader = UnstructuredFileLoader(file_path)
# 加载文档
documents = loader.load()
# 打印文档内容的前100个字符
print(documents[0].page_content[:100])

documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

# 准备embedding
import os
from langchain_community.embeddings import QianfanEmbeddingsEndpoint

os.environ["QIANFAN_AK"] = "da5shPmvrUC1r3EbIuGBcNIw"
os.environ["QIANFAN_SK"] = "tQ0EWGsYGDNBt85ydbA8ar6w9GBbF8CS"

embeddings = QianfanEmbeddingsEndpoint(
    qianfan_ak='da5shPmvrUC1r3EbIuGBcNIw',
    qianfan_sk='tQ0EWGsYGDNBt85ydbA8ar6w9GBbF8CS'
)

db = ElasticsearchStore.from_documents(
    docs,
    embeddings,
    es_url="http://localhost:9200",
    index_name="test-basic",
)

db.client.indices.refresh(index="test-basic")

query = "I want to learn python"
results = db.similarity_search(query)
print(results)



print("加载到最后了")