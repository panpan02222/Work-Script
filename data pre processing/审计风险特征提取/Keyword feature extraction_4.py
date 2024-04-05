#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   Keyword feature extraction_4.py
@Time    :   2024/04/05 14:51:11
@Author  :   pan binghong 
@Email   :   19909442097@163.com
@description   :   第三段需求代码实现
'''

import pandas as pd  

# 原始文件路径 | 按自己的文件位置进行修改
file_path = r'C:\Users\24529\Desktop\审计关键字提取\FIN_AuditDetail1.xlsx'
jianliti_zhongwen_dict = r'C:\Users\24529\Desktop\审计关键字提取\NTUSD_negative_simplified.txt'
hagongda_dict = r'C:\Users\24529\Desktop\审计关键字提取\stopwords_hit.txt'

# 文件下载链接: 
# https://github.com/ppzhenghua/SentimentAnalysisDictionary/tree/main
# https://github.com/CharyHong/Stopwords/blob/main/stopwords_hit.txt
 
# 以每行为单位, 需要导入<简体中文情感词典>及<哈工大停用词表>, 利用中文分词模块,
# 对"拼接后的关键审计事项描述"中的内容进行分词, 最终统计消极词汇的出现的次数.
# 除以所有的"拼接后的关键审计事项描述"总字数, 再乘100%, 最终输出一个新的字段"消极语调".要求每行都会输出一个百分比.

import pandas as pd  
import jieba  
  
# 读取情感词典和停用词表  
def load_dictionary(file_path):  
    with open(file_path, 'r', encoding='utf-8') as f:  
        words = f.read().splitlines()  
    return set(words)  
  
negative_words = load_dictionary(jianliti_zhongwen_dict)  # 替换为您的消极词汇词典路径  
stop_words = load_dictionary(hagongda_dict)  # 替换为您的停用词表路径  

# 初始化一个空列表来存储消极语调百分比  
negative_tone_percentages = []  

# 读取Excel文件  
df = pd.read_excel(file_path, sheet_name='Sheet2')  
  
# 分词并统计消极词汇出现次数  
for index, row in df.iterrows():  
    description = row['拼接后的关键审计事项描述']  
      
    # 分词  
    seg_list = jieba.cut(description, cut_all=False)  
    words = [word for word in seg_list if word not in stop_words]  
      
    # 统计消极词汇出现次数  
    negative_word_count = sum(1 for word in words if word in negative_words)  
      
    # 计算总字数  
    total_words = len(words)  
      
    # 避免除以零的情况  
    if total_words == 0:  
        negative_tone_percentage = 0  
    else:  
        negative_tone_percentage = (negative_word_count / total_words) * 100  
      
    # 将消极语调百分比添加到列表中  
    negative_tone_percentages.append(negative_tone_percentage)  
  
# 将消极语调百分比添加到DataFrame中  
df['消极语调'] = negative_tone_percentages  
  
# 将更新后的DataFrame写回到Sheet2中  
with pd.ExcelWriter(file_path, mode='a', engine='openpyxl') as writer:  
    df.to_excel(writer, sheet_name='Sheet2', index=False)  

print("处理完成，'消极语调'字段已添加到Sheet2。")