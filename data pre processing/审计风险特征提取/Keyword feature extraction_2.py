#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
@File    :   Keyword feature extraction_2.py
@Time    :   2024/04/05 14:25:42
@Author  :   pan binghong 
@Email   :   19909442097@163.com
@description   :   "第一段需求代码实现"
'''
import pandas as pd  
import re

# 原始文件路径 | 按自己的文件位置进行修改
file_path = r'C:\Users\24529\Desktop\审计关键字提取\FIN_AuditDetail1.xlsx'

# 以每行为单位, 针对"拼接后的关键审计事项描述"这一字段进行关键字提取, 统计"风险","重大"两个词出现的次数, 
# 除以所有的"拼接后的关键审计事项描述"总字数, 再乘100%, 最终输出一个新的字段"风险信息披露程度".要求每行都会输出一个百分比.
# 需要注意的是"风险","重大"两个词前面如果有"非","不","没有".则不能加入统计次数.

# 读取Excel文件，并定位到Sheet2  
df = pd.read_excel(file_path, sheet_name='Sheet2')  
  
# 初始化一个空列表来存储风险信息披露程度  
risk_disclosure_levels = []  
  
# 遍历Sheet2的每一行  
for index, row in df.iterrows():  
    description = row['拼接后的关键审计事项描述']  
      
    # 找出所有的"风险"和"重大"关键字  
    keywords = re.findall(r'风险|重大', description)  
      
    # 过滤掉前面有否定词的关键字  
    filtered_keywords = []  
    for keyword in keywords:  
        # 使用正则表达式查找关键字前面的内容  
        if not re.search(r'(非|不|没有)\s*{}'.format(re.escape(keyword)), description):  
            filtered_keywords.append(keyword)  
      
    # 计算过滤后的关键字数量  
    keyword_count = len(filtered_keywords)  
      
    # 计算描述的总字数  
    total_words = len(re.findall(r'\b\w+\b', description))  
      
    # 避免除以零的情况  
    if total_words == 0:  
        risk_disclosure_level = 0  
    else:  
        # 计算风险信息披露程度  
        risk_disclosure_level = (keyword_count / total_words) * 100  
      
    # 将计算结果添加到列表中  
    risk_disclosure_levels.append(risk_disclosure_level)  
  
# 将风险信息披露程度添加到DataFrame中  
df['风险信息披露程度'] = risk_disclosure_levels  

# 将更新后的DataFrame写回到Sheet2中  
with pd.ExcelWriter(file_path, mode='a', engine='openpyxl') as writer:  
    df.to_excel(writer, sheet_name='Sheet2', index=False)  
  
print("处理完成，风险信息披露程度已添加到Sheet2。")