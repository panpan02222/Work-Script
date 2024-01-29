import os.path
import xml.dom.minidom

# 将"白色口罩、蓝色口罩、黑色口罩"都替换为："已佩戴口罩"
# path为需要替换标签的目标文件夹
path = '/home/pbh/yolov5-master/VOCdevkit/labels'
files = os.listdir(path)  # 得到文件夹下所有文件名称
s = []
print('------------开始替换标签名称！--------------')
for xmlFile in files:  # 遍历原标签文件夹

    if not os.path.isdir(xmlFile):  # 判断是否是文件夹，不是文件夹才打开
        dom = xml.dom.minidom.parse(os.path.join(path, xmlFile))
        root = dom.documentElement
        #替换节点，除了name也可以替换为其他节点
        pathNode = root.getElementsByTagName('name')
        print(pathNode)
        print(len(pathNode))
        j = len(pathNode)
        for i in range(j):
            if pathNode[i].firstChild.data == "xaingtixiushi" or pathNode[i].firstChild.data == "kaiguangaiposun" or pathNode[i].firstChild.data == "jiliangxiangwaibu" or pathNode[i].firstChild.data == "xiang gai fa huang":
                print("替换前的名称为：", pathNode[i].firstChild.data)
                pathNode[i].firstChild.data = "xiangtixiushi"
                print("i为:", i)
                print("替换后的名称为：", pathNode[i].firstChild.data)
                i = i + 1
                with open(os.path.join(path, xmlFile), 'w',encoding='utf8') as fh:
                    dom.writexml(fh)

print('------------标签名称替换成功！--------------')

# import os.path
# import xml.dom.minidom

# # 将"白色口罩、蓝色口罩、黑色口罩"都替换为："已佩戴口罩"
# # path为需要替换标签的目标文件夹
# path = 'D:pythonproject\change_label\Annotation_1'
# files = os.listdir(path)  # 得到文件夹下所有文件名称
# s = []
# print('------------开始替换标签名称！--------------')
# for xmlFile in files:  # 遍历原标签文件夹

#     if not os.path.isdir(xmlFile):  # 判断是否是文件夹，不是文件夹才打开
#         dom = xml.dom.minidom.parse(os.path.join(path, xmlFile))
#         root = dom.documentElement
#         #替换节点，除了name也可以替换为其他节点
#         pathNode = root.getElementsByTagName('name')
#         print(pathNode)
#         print(len(pathNode))
#         j = len(pathNode)
#         for i in range(j):
#             if pathNode[i].firstChild.data == "白色口罩" or pathNode[i].firstChild.data == "蓝色口罩"  :
#                 print("替换前的名称为：", pathNode[i].firstChild.data)
#                 pathNode[i].firstChild.data = "已佩戴合格口罩"
#                 print("i为:", i)
#                 print("替换后的名称为：", pathNode[i].firstChild.data)
#                 i = i + 1
#                 with open(os.path.join(path, xmlFile), 'w',encoding='utf8') as fh:
#                     dom.writexml(fh)
#             elif pathNode[i].firstChild.data == "黑色口罩" :
#                 print("替换前的名称为：", pathNode[i].firstChild.data)
#                 pathNode[i].firstChild.data = "已佩戴不合格口罩"
#                 print("i为:", i)
#                 print("替换后的名称为：", pathNode[i].firstChild.data)
#                 i = i + 1
#                 with open(os.path.join(path, xmlFile), 'w',encoding='utf8') as fh:
#                     dom.writexml(fh)
# print('------------标签名称替换成功！--------------')

