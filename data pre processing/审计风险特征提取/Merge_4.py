#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   Merge_4.py
@Time    :   2024/04/26 08:57:11
@Author  :   pan binghong 
@Email   :   19909442097@163.com
@description   :   债券基本情况的票面利率，与前面的数据合并，删除空白的
'''


file_path = r'C:\Users\24529\Desktop\不是很专业的万事屋\审计关键字提取\file\FIN_AuditDetail1.xlsx'  
dst_path = r'C:\Users\24529\Desktop\不是很专业的万事屋\审计关键字提取\file\file\资产负债表.xlsx'
import pandas as pd  

# 读取原Excel文件  
original_df = pd.read_excel(file_path,sheet_name='Sheet1')  

# 读取目标Excel文件  
target_df = pd.read_excel(dst_path, sheet_name='sheet1')  
  
merged_df = pd.merge(original_df, target_df[['证券简称', '统计截止日期', '资产总计', '负债合计', '所有者权益合计', '负债与所有者权益总计']],   
                      on=['证券简称', '统计截止日期'], how='left')  
  
# 替换由于没有匹配项而产生的NaN值为0或适当的默认值  
merged_df.fillna(0, inplace=True)  

# 将更新后的DataFrame保存回原Excel文件（或保存为新的Excel文件）  
merged_df.to_excel(file_path, index=False)