import os
import xml.etree.ElementTree as ET

# 定义要统计的文件夹路径
# folder_path = "/home/pbh/yolov5-master/VOCdevkit/labels"
# folder_path = r'H:\Pan_BingHong\重新标注样本\统计标签数量任务\保定'
# folder_path = r'H:\Pan_BingHong\重新标注样本\统计标签数量任务\沧州'
# folder_path = r'H:\Pan_BingHong\重新标注样本\统计标签数量任务\石家庄'
# folder_path = r'H:\Pan_BingHong\重新标注样本\统计标签数量任务\衡水'
# folder_path = r'H:\Pan_BingHong\重新标注样本\统计标签数量任务\邢台'
# folder_path = r'H:\Pan_BingHong\重新标注样本\统计标签数量任务\邯郸'
# folder_path = r'H:\Pan_BingHong\重新标注样本\统计标签数量任务\雄安'

city = ["保定","沧州","石家庄","衡水","邢台","邯郸","雄安"]

names = ['xiangtifahuang','xiangtixiushi','xiangtiposun','wumen','wuxiang','youfeng','wufeng','youkaiguangai','wukaiguangai','youtoushichuanggai','wutoushichuanggai']

def cout_labels(city_name):
    path1 = "H:\\潘秉宏\\重新标注样本\\统计标签数量任务"
    folder_path = path1 + '\\' + city_name
    # 定义一个字典来存储object的name出现的次数
    name_counts = {}

    # 遍历文件夹中所有的xml文件
    for filename in os.listdir(folder_path):
        if filename.endswith(".xml"):
            # 解析xml文件
            tree = ET.parse(os.path.join(folder_path, filename))
            root = tree.getroot()
            
            # 遍历xml文件中所有的object标签
            for obj in root.findall('object'):
                name = obj.find('name').text
                # 将name加入字典中，并增加计数
                name_counts[name] = name_counts.get(name, 0) + 1

    #打印需要统计的目录
    print(folder_path)

    # 输出每个name出现的次数
    for name, count in name_counts.items():
        if name in names:
            print(f"{name}: {count}")
    # for name, count in name_counts.items():
    #     print(f"{name}:{count}")


    total_count = sum(name_counts.values())
    print(f"Total count: {total_count}")




if __name__ == '__main__':
    while 1:
        #city = ["保定"，'沧州','石家庄','衡水','邢台','邯郸','雄安']
        city_name = input('请输入要查询的城市名称:')
        if city_name not in city:
            print('检查你输入的城市名称！！！')
        else:
            print('要查询',city_name,'是吧!!!\n稍等一会')

        cout_labels(city_name)
        print('*'*30,'\n统计完毕！！！')



