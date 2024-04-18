#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   Keyword feature extraction_3.py
@Time    :   2024/04/05 14:41:12
@Author  :   pan binghong 
@Email   :   19909442097@163.com
@description   :   第二段需求代码实现
'''

import pandas as pd  

# 原始文件路径 | 按自己的文件位置进行修改
file_path = r'C:\Users\24529\Desktop\审计关键字提取\FIN_AuditDetail1.xlsx'

# 以每行为单位, 针对"拼接后的关键审计事项描述"这一字段进行关键字提取, 统计包含"减值","损失","事故","诉讼","重大会计估计","不足"六个词出现的情况 
# 如果"拼接后的关键审计事项描述"内容中出现,则标记为1,否则标记为0.最终输出一个新的字段"是否有负面关键字".将新增的内容补充在Sheet2中.

import pandas as pd  

# 读取Excel文件   
df = pd.read_excel(file_path, sheet_name='Sheet2')  
  
# 定义要检查的关键词列表  
keywords = ['减值', '损失', '事故', '诉讼', '重大会计估计', '不足']  
  
# 初始化一个空列表来存储是否有负面关键字的标记  
has_negative_keyword_flags = []  
  
# 遍历Sheet2的每一行  
for index, row in df.iterrows():  
    description = row['关键审计事项描述']  
      
    # 检查描述中是否包含关键词列表中的任意一个词  
    if any(keyword in description for keyword in keywords):  
        has_negative_keyword = 1  
    else:  
        has_negative_keyword = 0  
      
    # 将标记添加到列表中  
    has_negative_keyword_flags.append(has_negative_keyword)  

# 将是否有负面关键字的标记添加到DataFrame中  
df['是否有负面关键字'] = has_negative_keyword_flags  
  
# 将更新后的DataFrame写回到Sheet2中  
with pd.ExcelWriter(file_path, mode='a', engine='openpyxl') as writer:  
    df.to_excel(writer, sheet_name='Sheet2', index=False)  
  
print("处理完成，'是否有负面关键字'字段已添加到Sheet2。")