import pandas as pd  
  
# 读取两个Excel文件  
df1 = pd.read_excel('merged_data.xlsx')  
df2 = pd.read_excel('data-1.xlsx')  
  
# 确保用于合并的列名在两个DataFrame中完全一致  
# 如果不一致，你可能需要重命名这些列  
# 例如：df2.rename(columns={'some_old_name': '证券代码'}, inplace=True)  
  
# 使用merge函数合并两个DataFrame  
# how='left'表示左连接，即保留df1中的所有行，即使df2中没有匹配的行  
merged_df = pd.merge(df1, df2[['证券代码', '统计截止日期', '经营现金流比例_y', '销售收入增长率_y']],  
                     on=['证券代码', '统计截止日期'], how='left')  
  
# 保存合并后的DataFrame到新的Excel文件  
merged_df.to_excel('merged_data_with_additional_info.xlsx', index=False)