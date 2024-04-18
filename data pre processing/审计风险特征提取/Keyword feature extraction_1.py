#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   Keyword feature extraction.py
@Time    :   2024/04/05 13:32:40
@Author  :   pan binghong 
@Email   :   19909442097@163.com
@description   :   "Keyword feature extraction_审计专业关键字特征提取之数据整理"

'''

# 将文件中字段为"证券代码","证券简称"内容一致的行数,以这两个字段为主,将"关键审计事项描述"拼接到一行内.
# 最终实现创建一个新表格sheet2,这个表格中有3个字段,为"证券代码","证券简称","关键审计事项描述".

import pandas as pd    
  
# 原始文件路径，请按照您自己的文件位置进行修改  
file_dir = r'C:\Users\24529\Desktop\审计关键字提取\FIN_AuditDetail1.xlsx'  
  
# 读取Excel文件    
df = pd.read_excel(file_dir, sheet_name='Sheet1')    
  
# 使用groupby对证券代码、证券简称和会计截止日期进行分组，并拼接关键审计事项描述  
grouped = df.groupby(['证券代码', '证券简称', '会计截止日期'])['关键审计事项描述'].apply(lambda x: ' '.join(x.dropna().astype(str))).reset_index()  
  
# 确保列名正确，如果需要的话可以进行重命名  
grouped.rename(columns={'会计截止日期': '新的会计截止日期列名'}, inplace=True)  # 如果需要重命名，取消注释这行  
  
# 将结果写入新的sheet    
with pd.ExcelWriter(file_dir, mode='a', if_sheet_exists='replace', engine='openpyxl') as writer:    
    grouped.to_excel(writer, sheet_name='Sheet2', index=False)    
  
print("处理完成，结果已写入Sheet2。")