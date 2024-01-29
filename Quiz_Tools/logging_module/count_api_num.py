import re
import matplotlib.pyplot as plt  
from datetime import datetime  
  
def count_logs_per_day(log_file):  
    daily_logs = {}  
    with open(log_file, 'r') as f:  
        for line in f:  
            match = re.search(r'\d{4}-\d{1,2}-\d{1,2}', line)  
            if match:  
                date = datetime.strptime(match.group(), '%Y-%m-%d')  
                date = date.strftime('%m-%d')  # 仅显示月-日
                if date in daily_logs:  
                    daily_logs[date] += 1  
                else:  
                    daily_logs[date] = 1  
    return daily_logs  

log_file = "./classify_and_chat.log"  # 请替换为你的日志文件路径  
daily_logs = count_logs_per_day(log_file)  
  
# 创建一个新的日期序列，并填充日志数量  
x = sorted(daily_logs.keys())  # 日期排序  
y = [daily_logs[date] for date in x]  # 日志数量排序  
  
# 创建折线图  
plt.figure(figsize=(10, 6))  # 设置图形大小为10x6英寸  
plt.plot(x, y, marker='o')  # 使用圆点标记每个数据点  
plt.title('The number of times the trivia application was called')  # 设置标题  
plt.xlabel('DATE')  # 设置x轴标签  
plt.ylabel('NUMs')  # 设置y轴标签  
plt.grid(True)  # 显示网格线  
plt.show()  # 显示图形