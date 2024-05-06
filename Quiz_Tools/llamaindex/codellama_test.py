#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   codellama_test.py
@Time    :   2024/04/22 10:12:39
@Author  :   pan binghong 
@Email   :   19909442097@163.com
@description   :   
'''


from transformers import AutoTokenizer, LlamaForCausalLM

# Initialize the model
model_path = "Phind/Phind-CodeLlama-34B-v2"
model = LlamaForCausalLM.from_pretrained(model_path, device_map="auto")
tokenizer = AutoTokenizer.from_pretrained(model_path)

# Test question
question = "帮我用c写一段冒泡排序的代码"
# question = "Help me write a bubble sort code in c"

# Tokenize the question
inputs = tokenizer(question, return_tensors="pt")

# Generate answer
outputs = model.generate(input_ids=inputs["input_ids"], max_length=50, num_return_sequences=1)

# Decode and print the answer
answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
print("Answer:", answer)

from vllm import LLM, SamplingParams
llm = LLM(model="模型路径")

prompts = [
    "Hello,who are you?",
    "你好, 你是谁?"
]

# prompts = [
#     "Hello,who are you?",
#     "你好, 你是谁?",
#     "Help me write a bubble sort code in c"
#     "帮我用c写一段冒泡排序的代码",
#     "The capital of France is",
#     "The future of AI is",
# ]
sampling_params = SamplingParams(temperature=0.8, top_p=0.95)

outputs = llm.generate(prompts, sampling_params)

# Print the outputs.
for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs[0].text
    print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")


# 安装 pip install llama-index-llms-vllm


llm = Vllm(
    model="模型路径",
    dtype="float16",
    tensor_parallel_size=1,
    temperature=0,
    max_new_tokens=100,
    vllm_kwargs={
        "swap_space": 1,
        "gpu_memory_utilization": 0.5,
        "max_model_len": 4096,
    },
)

llm.complete([" What is python ?"])



# 接入本地知识库
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.embeddings import resolve_embed_model
from llama_index.llms.vllm import Vllm

# 把你的文档放在data文件夹下
documents = SimpleDirectoryReader("data").load_data()

# embedding model
Settings.embed_model = resolve_embed_model("自己下一个embedding,放路径")
# 参考 | https://docs.llamaindex.ai/en/stable/examples/embeddings/fastembed/ 
# 或者 | 去huggingface搜索BAAI/bge

Settings.llm = Vllm(
    model="模型路径",
    dtype="float16",
    tensor_parallel_size=1,
    temperature=0,
    max_new_tokens=100,
    vllm_kwargs={
        "swap_space": 1,
        "gpu_memory_utilization": 0.5,
        "max_model_len": 4096,
    },
)

index = VectorStoreIndex.from_documents(
    documents,
)

query_engine = index.as_query_engine()
response = query_engine.query("问一个跟你文档相关的问题")
print(response)
