# 注册elastic账号, 免费使用15天.
> https://www.elastic.co/cn/cloud/elasticsearch-service/signup?page=docs&placement=docs-body
## 使用账号密码链接
```
import elasticsearch
from langchain_elasticsearch import ElasticsearchStore

es_client= elasticsearch.Elasticsearch(
    hosts=["http://localhost:9200"],
    es_user="elastic",
    es_password="changeme"
    max_retries=10,
)

embedding = OpenAIEmbeddings()
elastic_vector_search = ElasticsearchStore(
    index_name="test_index",
    es_connection=es_client,
    embedding=embedding,
)
```