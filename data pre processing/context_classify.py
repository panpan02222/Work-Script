#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   context_classify.py
@Time    :   2024/02/20 15:12:36
@Author  :   pan binghong 
@Email   :   19909442097@163.com
@description   :   
'''

import pandas as pd
import os

# 读取Excel文件
df = pd.read_excel(r"C:\Users\24529\Desktop\wenben-utf8\通话文本数据(1).xlsx")

# 将“通话开始时间”列转换为日期格式
df['通话开始时间'] = pd.to_datetime(df['通话开始时间'])

# 提取日期
df['日期'] = df['通话开始时间'].dt.date

# 获取需要的列
df = df[['日期', '业务类型', '通话内容']]

# 指定输出目录
output_dir = r'C:\Users\24529\Desktop\wenben-utf8'

# 根据日期分组并创建新的txt文件
for date, group in df.groupby('日期'):
    # 更改列名
    group = group.rename(columns={'业务类型': 'label', '通话内容': 'content'})
    output_path = os.path.join(output_dir, f'{date}.txt')
    group[['label','content']].to_csv(output_path, index=False, sep='\t',encoding='utf-8')
