#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   Data Cleansing.py
@Time    :   2024/04/30 15:07:54
@Author  :   pan binghong 
@Email   :   19909442097@163.com
@description   :   上市公司债券信用利差计算
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from tqdm import tqdm

plt.rcParams['font.sans-serif'] = ['SimHei'] #正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False #解决负号显示为方块的问题

# 数据清洗

print('债券基本情况数据清洗-债券基本情况数据清洗-债券基本情况数据清洗-债券基本情况数据清洗-债券基本情况数据清洗-债券基本情况数据清洗')
Bndinfo = pd.read_excel('data pre processing\审计风险特征提取\BND_Bndinfo.xlsx')
# 增加进度条
for i in tqdm(range(int(9e6))):
    pass

# 筛选出A股上市公司债券
Bndinfo  = Bndinfo.dropna(subset=['发行人股票代码'])
# 添加上市公司证券代码
Bndinfo['发行人股票代码'] = Bndinfo['发行人股票代码'].astype(int) # 去掉小数点
Bndinfo['市场代码'] = Bndinfo['发行人股票代码'].astype(str)
Bndinfo['市场代码'] = Bndinfo['市场代码'].str.zfill(6)
# 提取year
Bndinfo['年份'] = pd.to_datetime(Bndinfo['上市日期']).dt.year
Bndinfo = Bndinfo[['年份','债券代码','债券简称','市场代码','期限']]
Bndinfo.groupby(['年份','市场代码'])['债券代码'].count().mean()

# 重复样本的处理
print('重复样本的处理')
# 增加进度条
for i in tqdm(range(int(5e6))):
    pass
# 为数据集中的每个观测值生成一个介于0和1之间的随机数
Bndinfo['rand'] = np.random.rand(len(Bndinfo))
# 计算每个组中的最大随机数
Bndinfo['max'] = Bndinfo.groupby(['市场代码', '年份'])['rand'].transform('max')
# 保留只有最大随机数的观测值
Bndinfo = Bndinfo[Bndinfo['max'] == Bndinfo['rand']]
# 删除不再需要的列
Bndinfo = Bndinfo.drop(['max', 'rand'], axis=1)
Bndinfo['债券代码'] = Bndinfo['债券代码'].astype(str)

print(Bndinfo)

# 提取 "Term" 列
Term = Bndinfo[['年份','期限']]
# 删除重复观测值
Term = Term.drop_duplicates()
# 按照 "Term" 列进行排序
Term = Term.sort_values('期限')
Term = Term.dropna()

# 现有期限数据处理
print('国债收益率插值计算-国债收益率插值计算-国债收益率插值计算-国债收益率插值计算-国债收益率插值计算-国债收益率插值计算-国债收益率插值计算')
TreasYield = pd.read_excel(r'data pre processing\审计风险特征提取\BND_TreasYield.xlsx')
TreasYield['日期'] = pd.to_datetime(TreasYield['日期'])
TreasYield['年份'] = TreasYield['日期'].dt.year


# 处理重复债券
TreasYield['max'] = TreasYield.groupby(['收益率曲线类型', '年份'])['日期'].transform('max')
TreasYield = TreasYield[TreasYield['日期'] == TreasYield['max']]
del TreasYield['max']
del TreasYield['日期']
TreasYield = TreasYield.rename(columns={'剩余年限':'期限'})

# 插值
print('插值中...')
# 每个截面上需要的期限和已有期限数据进行合并
Term = pd.merge(Term, TreasYield, on=['年份','期限'], how='left', sort=True)
# 分组插值计算
Term['Yield_1'] = Term.groupby('期限')['收益率(%)'].transform(lambda x: x.interpolate(method='linear'))
Term['Yield_2'] = Term.groupby('年份')['Yield_1'].transform(lambda x: x.interpolate(method='linear'))
# 保留所需的列
Term = Term[['年份', '期限', 'Yield_2']]
# 将小于等于0的值替换为缺失值
Term.loc[Term['Yield_2'] <= 0, 'Yield_2'] = pd.NA
# 删除重复观测值
Term = Term.drop_duplicates(subset=['年份', '期限'], keep='first')
# 重命名列
Term = Term.rename(columns={'Yield_2': 'Treasury'})
# 缺失值以组内最小值填充
Term['Treasury'] = Term.groupby('年份')['Treasury'].transform(lambda x: x.fillna(x.min()))
print('差值处理完成！')


print('债券信用利差计算-债券信用利差计算-债券信用利差计算-债券信用利差计算-债券信用利差计算-债券信用利差计算-债券信用利差计算')

Tradeinfo = pd.read_excel(r'data pre processing\审计风险特征提取\BND_Bndyt.xlsx')
Tradeinfo = Tradeinfo.rename(columns={'交易年份':'年份'})
# 删除重复观测值
Tradeinfo = Tradeinfo.drop_duplicates(subset=["债券代码", "年份"], keep="first")
Tradeinfo = Tradeinfo[['债券代码','年份','年收盘日到期收益率(%)']] # Clsyield：收盘日到期收益率
# 数据类型转换，以便合并
Tradeinfo['债券代码'] = Tradeinfo['债券代码'].astype(str)
# 与债券基本情况数据合并
df = pd.merge(Bndinfo, Tradeinfo, on=['债券代码','年份'], how='left', sort=True)
df = df[df['年份']>=2010]

### <b>债券信用利差计算</b>
#  截尾操作
## 年收盘日到期收益率(%),交易市场代码
df['YTM_1'] = df['年收盘日到期收益率(%)'].clip(lower=np.percentile(df['年收盘日到期收益率(%)'], 1))
# 替换小于等于0的值为缺失值
df.loc[df['YTM_1'] <= 0, 'YTM_1'] = np.nan
# 计算每个组的均值
# 为数据框中的YTM_2列添加每个债券代码对应的YTM_1列的平均值
df['YTM_2'] = df.groupby('债券代码')['YTM_1'].transform('mean')

# 为数据框中的YTM_3列添加每个市场代码对应的YTM_2列的平均值
df['YTM_3'] = df.groupby('市场代码')['YTM_2'].transform('mean')

# 为数据框中的YTM_4列添加每个年份对应的YTM_3列的平均值
df['YTM_4'] = df.groupby('年份')['YTM_3'].transform('mean')
# 创建新变量并填充缺失值
df['YTM'] = np.nan
for x in range(1, 5):
    df.loc[df['YTM'].isnull(), 'YTM'] = df[f'YTM_{x}']
print(df['YTM'])
df = df[['债券代码','年份','债券简称','市场代码','期限','YTM']]
# 合并国债收益率插值结果
df = pd.merge(df, Term, on=['期限','年份'], how='left', sort=True)
# 作差计算CS
df['CS'] = df['YTM'] - df['Treasury']
# 负值和零值处理（组内最小值填充）
df.loc[df['CS'] <= 0, 'CS'] = np.nan
df['CS'] = df.groupby('年份')['CS'].transform(lambda x: x.fillna(x.min()))
print(df['CS'])
print('债券信用利差计算完成！')