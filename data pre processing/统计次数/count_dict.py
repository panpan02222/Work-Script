#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   count_dict.py
@Time    :   2024/05/06 16:09:48
@Author  :   pan binghong 
@Email   :   19909442097@163.com
@description   :   
'''

import pandas as pd

df = pd.read_excel('data pre processing\统计次数\Events-20240506.xlsx')

result = df.groupby('机器编号')['计数'].sum().reset_index()

# 将结果保存在sheet2表内
with pd.ExcelWriter('data pre processing\统计次数\Events-20240506.xlsx') as writer:
    result.to_excel(writer, sheet_name='Sheet2', index=False)
