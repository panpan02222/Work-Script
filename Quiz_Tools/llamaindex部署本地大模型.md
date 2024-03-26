## Llamaindex + 部署本地大模型

### 1.https://github.com/run-llama/llama_index|github链接
### 2.https://docs.llamaindex.ai/en/stable/|文档说明主页
### 3.langchain & llamaindex | 调研
### 4.阅读说明手册
![image-20240326201113259](Quiz_Tools\images\image-20240326201113259.png)

### 5.[BAAI/bge-large-zh-v1.5 · Hugging Face](https://huggingface.co/BAAI/bge-large-zh-v1.5) | Embedding模型下载链接

### 6.![image-20240326201814951](images\image-20240326201814951.png)

### 7. [Ollama平台](https://github.com/ollama/ollama) | 大模型管理平台下载

### 8. [Bilbil安装教程](https://www.bilibili.com/video/BV19m411f7GX?vd_source=4f233a17ccc9dbdb1e5b6f3a66919a6b) | Ollama

### 9. 运行代码
```
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.embeddings import resolve_embed_model
from llama_index.llms.ollama import Ollama

documents = SimpleDirectoryReader("data").load_data()

# bge embedding model
Settings.embed_model = resolve_embed_model("local:BAAI/bge-small-en-v1.5")

# ollama
Settings.llm = Ollama(model="mistral", request_timeout=30.0)

index = VectorStoreIndex.from_documents(
    documents,
)
```

```
query_engine = index.as_query_engine()
response = query_engine.query("What did the author do growing up?")
print(response)
```

### 10. 额外拓展链接

#### 清华大模型库
> https://huggingface.co/THUDM
#### Langchain-chatchat项目地址
> https://github.com/chatchat-space/Langchain-Chatchat
### Langchain官方项目地址
> https://python.langchain.com/docs/use_cases/question_answering/quickstart

