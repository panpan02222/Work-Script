import pandas as pd

# 设置文件路径  
file_path = r'C:\Users\24529\Desktop\审计关键字提取\FIN_AuditDetail1.xlsx'   
# 读取Excel文件  
df = pd.read_excel(file_path)  
  
# 检查"财务杠杆"、"经营杠杆"和"综合杠杆"列，如果值为0或空，则删除整行  
df = df.dropna(subset=['财务杠杆', '经营杠杆', '综合杠杆', '证券简称'], how='any')  
df = df[(df['财务杠杆'] != 0) & (df['经营杠杆'] != 0) & (df['综合杠杆'] != 0)]  
  
# 将更新后的DataFrame保存为新的Excel文件  
df.to_excel(file_path, index=False)  

print(f'处理完成，已更新数据并保存到 {file_path}')