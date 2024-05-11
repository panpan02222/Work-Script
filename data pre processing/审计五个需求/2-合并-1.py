import pandas as pd

# 加载第一个文件
df2 = pd.read_excel('./data_filled.xlsx')
# 证券代码

# 加载第二个文件
df1 = pd.read_excel('结果.xlsx')
# 证券代码 统计截止日期

# 合并数据集
df = df1.merge(df2, on=['证券代码', '统计截止日期'], how='inner')

df.to_excel('merged_data.xlsx')
