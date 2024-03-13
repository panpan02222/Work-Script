#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   Gemma_api.py
@Time    :   2024/02/28 11:59:09
@Author  :   pan binghong 
@Email   :   19909442097@163.com
@description   :   CPU运行gemma-7b调用代码, 没加载出来, 电脑太烫了.
'''

# 模型地址 : https://huggingface.co/google/gemma-7b

from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained(r"E:\llms\gemma-7b")
model = AutoModelForCausalLM.from_pretrained(r"E:\llms\gemma-7b")

input_text = "Write me a poem about Machine Learning."
input_ids = tokenizer(input_text, return_tensors="pt")

outputs = model.generate(**input_ids)
print(tokenizer.decode(outputs[0]))

# pip install accelerate

# from transformers import AutoTokenizer, AutoModelForCausalLM

# tokenizer = AutoTokenizer.from_pretrained("google/gemma-7b")
# model = AutoModelForCausalLM.from_pretrained("google/gemma-7b", device_map="auto")

# input_text = "Write me a poem about Machine Learning."
# input_ids = tokenizer(input_text, return_tensors="pt").to("cuda")

# outputs = model.generate(**input_ids)
# print(tokenizer.decode(outputs[0]))

