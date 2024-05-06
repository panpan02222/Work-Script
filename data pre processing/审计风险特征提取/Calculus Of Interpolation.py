#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   Calculus Of Interpolation.py
@Time    :   2024/04/30 16:16:46
@Author  :   pan binghong 
@Email   :   19909442097@163.com
@description   :   
'''


# 现有期限数据处理
print('处理现有期限数据...')
TreasYield = pd.read_excel(r'data pre processing\BND_TreasYield.xlsx')
TreasYield['日期'] = pd.to_datetime(TreasYield['日期'])
TreasYield['年份'] = TreasYield['日期'].dt.year
# 处理重复债券
TreasYield['max'] = TreasYield.groupby(['Cvtype', '年份'])['日期'].transform('max')
TreasYield = TreasYield[TreasYield['日期'] == TreasYield['max']]
del TreasYield['max']
del TreasYield['日期']
TreasYield = TreasYield.rename(columns={'剩余年限':'收益率(%)'})

# 插值
print('插值中...')
# 每个截面上需要的期限和已有期限数据进行合并
Term = pd.merge(Term, TreasYield, on=['年份','收益率(%)'], how='left', sort=True)
# 分组插值计算
Term['Yield_1'] = Term.groupby('收益率(%)')['Yield'].transform(lambda x: x.interpolate(method='linear'))
Term['Yield_2'] = Term.groupby('年份')['Yield_1'].transform(lambda x: x.interpolate(method='linear'))
# 保留所需的列
Term = Term[['年份', '收益率(%)', 'Yield_2']]
# 将小于等于0的值替换为缺失值
Term.loc[Term['Yield_2'] <= 0, 'Yield_2'] = pd.NA
# 删除重复观测值
Term = Term.drop_duplicates(subset=['年份', '收益率(%)'], keep='first')
# 重命名列
Term = Term.rename(columns={'Yield_2': 'Treasury'})
# 缺失值以组内最小值填充
Term['Treasury'] = Term.groupby('年份')['Treasury'].transform(lambda x: x.fillna(x.min()))
print('差值处理完成！')