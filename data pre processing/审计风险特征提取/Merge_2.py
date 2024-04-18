#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   Merge_2.py
@Time    :   2024/04/06 20:15:34
@Author  :   pan binghong 
@Email   :   19909442097@163.com
@description   :   
'''

file_path = r'C:\Users\24529\Desktop\审计关键字提取\FIN_AuditDetail1.xlsx'  
dst_path = r'C:\Users\24529\Desktop\审计关键字提取\file\利润表.xlsx'
import pandas as pd  
  
# 读取原Excel文件  
original_df = pd.read_excel(file_path,sheet_name='Sheet1')  

# 读取目标Excel文件  
target_df = pd.read_excel(dst_path, sheet_name='Sheet2')  
  
merged_df = pd.merge(original_df, target_df[['证券简称', '统计截止日期', '营业利润', '利润总额', '净利润']],   
                      on=['证券简称', '统计截止日期'], how='left')  
  
# 替换由于没有匹配项而产生的NaN值为0或适当的默认值  
merged_df.fillna(0, inplace=True)  

# 如果你想要只保留那些实际上有目标文件中数据的行，你可以使用dropna函数来删除全为NaN的行  
# 注意：这将删除那些在原文件中存在但在目标文件中没有匹配项的行  
# merged_df.dropna(subset=['财务杠杆', '经营杠杆', '综合杠杆'], inplace=True)  

# 将更新后的DataFrame保存回原Excel文件（或保存为新的Excel文件）  
merged_df.to_excel(file_path, index=False)