import pandas as pd  
  
# 指定文件路径  
file_path = r'E:\Work-Script\data pre processing\审计五个需求\结果表.xlsx'  
  
# 加载Excel文件  
df = pd.read_excel(file_path)  
  
# 填充'证券代码'列，使用前向填充（ffill）  
df['证券代码'] = df['证券代码'].ffill()  
df['公司全称'] = df['公司全称'].ffill()  
df['所在行业'] = df['所在行业'].ffill()  
df['是否纳入'] = df['是否纳入'].ffill()  
# 保存更改而不修改原始DataFrame  
df_filled = df.copy()  # 创建一个副本  
df_filled.to_excel('data_filled.xlsx', index=False)  # 保存填充后的副本