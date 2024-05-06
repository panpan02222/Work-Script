#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   zhihu.py
@Time    :   2024/04/26 11:22:57
@Author  :   pan binghong 
@Email   :   19909442097@163.com
@description  : 将债券基本情况表BND_Bndinfo.xlsx中的'票面利率'\
                与中债国债收益率情况表BND_TreasYield.xlsx中'收益率(%)'进行相减, \
                条件为债券基本情况表BND_Bndinfo.xlsx的'发行起始日期'列与 \
                中债国债收益率情况表BND_TreasYield.xlsx的'日期'列一致时进行相减.\
'''
import pandas as pd

# 从Excel文件中读取债券基本情况表数据和中债国债收益率情况表数据
bond_info = pd.read_excel(r'C:\Users\24529\Desktop\不是很专业的万事屋\审计关键字提取\file\债券基本情况表BND_Bndinfo.xlsx')
treas_yield = pd.read_excel(r'C:\Users\24529\Desktop\不是很专业的万事屋\审计关键字提取\file\中债国债收益率情况表BND_TreasYield.xlsx')

# 将'发行起始日期'列转换为日期类型
bond_info['发行起始日期'] = pd.to_datetime(bond_info['发行起始日期'])

# 将'日期'列转换为日期类型
treas_yield['日期'] = pd.to_datetime(treas_yield['日期'])

# 合并两个表格，条件是'发行起始日期'列与'日期'列相等
merged_data = pd.merge(bond_info, treas_yield, how='left', left_on='发行起始日期', right_on='日期')

# 计算'公司债券风险溢价'列，即'票面利率'与'收益率(%)'相减
merged_data['公司债券风险溢价'] = merged_data['票面利率'] - merged_data['收益率(%)']

# 将结果保存到新的Excel文件中
merged_data.to_excel(r'', index=False)
