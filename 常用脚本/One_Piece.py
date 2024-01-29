import os
import xml.etree.ElementTree as ET
import shutil
import pickle
import os.path
import xml.dom.minidom
import random
import tqdm
from os import listdir, getcwd
from os.path import join

img_dir = r"H:\潘秉宏\重新标注样本\营销样本_1\JPEGImages"
xml_dir = r"H:\潘秉宏\重新标注样本\营销样本_1\Annotations"
best_xml_dir = r'C:\Users\Administrator\Desktop\雄安调度\Documents'
best_img_dir = r'C:\Users\Administrator\Desktop\雄安调度\TXT'

txt_path = r"C:\Users\Administrator\Desktop\jueyuanzi\txt"

#/home/bml/storage/mnt/v-ywe1p54l2brsm9cj/org/dianbiao/VOCdevkit4/images

random.seed(7)
images = "images"
Annotations = "Annotations"
txt = "labels"
del_file = "del"
best_images = "best_images"
best_xml = "best_xml"

#每次改这个路径
src_path = r'C:\Users\Administrator\Desktop\雄安调度'

# images_dir = os.path.join(src_path,images)
# print(f'确认一下图片路径：{images_dir}')
# xml_dir = os.path.join(src_path,Annotations)
# print(f'确认一下标签路径：{xml_dir}')

# txt_dir = os.path.join(src_path,txt)
# print(f'确认一下图片路径：{txt_dir}')
dst_dir = os.path.join(src_path,del_file)
# # os.makedirs(txt_dir,exist_ok=True)
# # os.makedirs(dst_dir,exist_ok=True)

# images_dir_best = os.path.join(src_path,best_images)
# if not os.path.exists(images_dir_best):
    # os.mkdir(images_dir_best)
    # print(f"已创建best_images文件夹:{images_dir_best}")
    
# xml_dir_best = os.path.join(src_path,best_xml)
# if not os.path.exists(xml_dir_best):
    # os.mkdir(xml_dir_best)
    # print(f"已创建best_xml文件夹:{xml_dir_best}")



if not os.path.exists(dst_dir):
    os.mkdir(dst_dir)
    print('已创建目标文件夹')
else:
    print('dst文件已存在')

# if not os.path.exists(txt_dir):
    # os.mkdir(txt_dir)
    # print('已创建txt文件夹')
# else:
    # print('txt文件已存在')



# 需要转换的类别，需要和yaml文件一一对应
classes = [
    'xiangtixiushi',
    'xiangtiposun',
    'xiangtifahuang',
    'wumen',
    'wuxiang',
    'youfeng',
    'wufeng',
    'youtoushichuanggai',
    'wutoushichuanggai',
    'youkaiguangai',
    'wukaiguangai'
]

# classes = [
#     "jueyuanzi",
#     "bianyaqi",
#     "daoxianweibangza",
#     "daoxianbangzabuguifan"
# ]

# 获取所有 XML 文件并遍历
def delete_xml_size_is_zero(xml_dir):
    print('------------开始删除尺寸为零的文件！--------------')
    for file in os.listdir(xml_dir):
        if file.endswith('.xml'):
            # 加载 XML 文件
            try:
                print(f'处理的xml文件为：{file}')
                absxmlpath = os.path.join(xml_dir,file)
                tree = ET.parse(absxmlpath)
            except ET.ParseError as e:
                print(f"{file} - 无法解析 XML 文件：{e}")
                continue
            # 查找 width 和 height 为 0 的 size 元素
            root = tree.getroot()
            for size in root.findall('size'):
                width = int(size.find('width').text)
                height = int(size.find('height').text)
                
                if width == 0:
                    # 删除文件
                    os.remove(absxmlpath)
                    print(f"已删除文件：{absxmlpath}（原因：width 长度为 0）")
                    break
                elif height == 0:
                    # 删除文件
                    os.remove(absxmlpath)
                    print(f"已删除文件：{absxmlpath}（原因：height 长度为 0）")
                    break

            # 遍历xml文件中所有的object标签
            for obj in root.findall('object'):
                name = obj.find('name').text
                # 将name加入字典中，并增加计数
                if name not in classes:
                    try:
                        os.remove(absxmlpath)
                        print(f'已删除文件：{absxmlpath}(原因 标签名称不对！！！{name}')
                    except FileNotFoundError as e:
                        print(f'该文件已被删除{absxmlpath}')
                        continue
                    break
    print('------------删除完毕！！！--------------')

def cut_diff_file_best(image_dir,xml_dir,image_dir_best,xml_dir_best):

    xml_list = os.listdir(xml_dir)
    jpg_list = os.listdir(image_dir)
    n = len(xml_list)
    count = 0

    for i in tqdm.trange(n):
        for ajpg in jpg_list:
            if ajpg[:-4] == xml_list[i][:-4]:
                shutil.copy(xml_dir + '/' + xml_list[i], xml_dir_best + '/' + xml_list[i])
                shutil.copy(image_dir + '/' + ajpg, image_dir_best + '/' + ajpg)
                count = count + 1
                break
    print('\ndone. 共移动',count,'对xml和jpg对应的文件.')


def cut_diff_file(images_dir,xml_dir):
    print('------------开始删除名称不对应的文件！--------------')
    # 获取原始文件名列表及其路径
    src_files1 = {}
    src_files2 = {}

    # 递归遍历文件夹1和其中的文件
    for root, dirs, files in os.walk(xml_dir):
        for file in files:
            file_name = os.path.splitext(file)[0]
            file_path = os.path.join(root, file)
            src_files1[file_name] = file_path

    # 递归遍历文件夹2和其中的文件    
    for root, dirs, files in os.walk(images_dir):
        for file in files:
            file_name = os.path.splitext(file)[0]
            file_path = os.path.join(root, file)
            src_files2[file_name] = file_path

    # 比较两个文件夹中的文件名，将名称不同的文件剪切到目标文件夹
    for file_name in src_files1.keys():
        if file_name not in src_files2.keys():
            src_path = src_files1[file_name]
            dst_path = os.path.join(dst_dir, os.path.basename(src_path))
            shutil.move(src_path, dst_path)
            print(f"移动文件 {src_path} 到目标文件夹")

    for file_name in src_files2.keys():
        if file_name not in src_files1.keys():
            src_path = src_files2[file_name]
            dst_path = os.path.join(dst_dir, os.path.basename(src_path))
            shutil.move(src_path, dst_path)
            print(f"移动文件 {src_path} 到目标文件夹")
    print('------------删除完毕！检查文件数目！！！--------------')

def convert(size, box):
    x_center = (box[0] + box[1]) / 2.0
    y_center = (box[2] + box[3]) / 2.0
    x = x_center / size[0]
    y = y_center / size[1]
    w = (box[1] - box[0]) / size[0]
    h = (box[3] - box[2]) / size[1]
    return (x, y, w, h)
 
def convert_annotation(xml_files_path, save_txt_files_path, classes):
    print('------------开始转换标签！！！--------------')
    xml_files = os.listdir(xml_files_path)
    print(xml_files)
    for xml_name in xml_files:
        print(xml_name)
        xml_file = os.path.join(xml_files_path, xml_name)
        out_txt_path = os.path.join(save_txt_files_path, xml_name.split('.')[0] + '.txt')
        out_txt_f = open(out_txt_path, 'w')
        tree = ET.parse(xml_file)
        root = tree.getroot()
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)
 
        for obj in root.iter('object'):
            difficult = obj.find('difficult').text
            cls = obj.find('name').text
            if cls not in classes or int(difficult) == 1:
                continue
            cls_id = classes.index(cls)
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
                 float(xmlbox.find('ymax').text))
            # b=(xmin, xmax, ymin, ymax)
            print(w, h, b)
            bb = convert((w, h), b)
            out_txt_f.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
    print('------------转换完毕！！！--------------')

def count_labels_names(xml_dir):
    print('------------开始统计标签数量！！！--------------')
    # 定义一个字典来存储object的name出现的次数
    name_counts = {}

    # 遍历文件夹中所有的xml文件
    for filename in os.listdir(xml_dir):
        if filename.endswith(".xml"):
            # 解析xml文件
            tree = ET.parse(os.path.join(xml_dir, filename))
            root = tree.getroot()
            
            # 遍历xml文件中所有的object标签
            for obj in root.findall('object'):
                name = obj.find('name').text
                # 将name加入字典中，并增加计数
                name_counts[name] = name_counts.get(name, 0) + 1

    # 输出每个name出现的次数
    for name, count in name_counts.items():
        print(f"{name}: {count}")

    total_count = sum(name_counts.values())
    print(f"Total count: {total_count}")

def change_label_names(xml_dir):
    # 将"白色口罩、蓝色口罩、黑色口罩"都替换为："已佩戴口罩"
    # path为需要替换标签的目标文件夹
    files = os.listdir(xml_dir)  # 得到文件夹下所有文件名称
    s = []
    print('------------开始替换标签名称！--------------')
    for xmlFile in files:  # 遍历原标签文件夹

        if not os.path.isdir(xmlFile):  # 判断是否是文件夹，不是文件夹才打开
            dom = xml.dom.minidom.parse(os.path.join(xml_dir, xmlFile))
            root = dom.documentElement
            #替换节点，除了name也可以替换为其他节点
            pathNode = root.getElementsByTagName('name')
            print(pathNode)
            print(len(pathNode))
            j = len(pathNode)
            for i in range(j):
                # if pathNode[i].firstChild.data == "xaingtifahuang" or pathNode[i].firstChild.data == "xiangtifahunag":#or pathNode[i].firstChild.data == "" or pathNode[i].firstChild.data == "":
                #     print("替换前的名称为：", pathNode[i].firstChild.data)
                #     pathNode[i].firstChild.data = "xiangtifahuang"
                #     print("i为:", i)
                #     print("替换后的名称为：", pathNode[i].firstChild.data)
                #     i = i + 1
                #     with open(os.path.join(xml_dir, xmlFile), 'w', encoding ='utf8') as fh:
                #         dom.writexml(fh)

                if pathNode[i].firstChild.data == "transformer" or pathNode[i].firstChild.data == "绝缘子缺失" or pathNode[i].firstChild.data == "绝缘子污秽" or pathNode[i].firstChild.data == "绝缘子破损":
                    print("替换前的名称为：", pathNode[i].firstChild.data)
                    pathNode[i].firstChild.data = "bianyaqi"
                    print("i为:", i)
                    print("替换后的名称为：", pathNode[i].firstChild.data)
                    i = i + 1
                    with open(os.path.join(xml_dir, xmlFile), 'w', encoding ='utf8') as fh:
                        dom.writexml(fh)

                # if pathNode[i].firstChild.data == "yougaiguangai" or pathNode[i].firstChild.data == "youkaigaungai" or pathNode[i].firstChild.data == "youkaiguangan" or pathNode[i].firstChild.data == "youkaiguankai: ":
                #     print("替换前的名称为：", pathNode[i].firstChild.data)
                #     pathNode[i].firstChild.data = "youkaiguangai"
                #     print("i为:", i)
                #     print("替换后的名称为：", pathNode[i].firstChild.data)
                #     i = i + 1
                #     with open(os.path.join(xml_dir, xmlFile), 'w', encoding ='utf8') as fh:
                #         dom.writexml(fh)

    print('------------标签名称替换成功！--------------')

# def moveimg(images_dir, val_dir):
#     pathDir = os.listdir(images_dir)  # 取图片的原始路径
#     filenumber = len(pathDir)
#     rate = 0.1  # 自定义抽取图片的比例，比方说100张抽10张，那就是0.1
#     picknumber = int(filenumber * rate)  # 按照rate比例从文件夹中取一定数量图片
#     sample = random.sample(pathDir, picknumber)  # 随机选取picknumber数量的样本图片
#     print(sample)
#     for name in sample:
#         shutil.move(images_dir + name, val_dir + name)
#     return
 
# def movelabel(file_list, file_label_train, file_label_val):
#     for i in file_list:
#         if i.endswith('.jpg') or i.endswith('.JPG') or i.endswith('.jepg') or i.endswith('.png'):
#             # filename = file_label_train + "\\" + i[:-4] + '.xml'  # 可以改成xml文件将’.txt‘改成'.xml'就可以了
#             filename = file_label_train + i[:-4] + '.txt'  # 可以改成xml文件将’.txt‘改成'.xml'就可以了
#             if os.path.exists(filename):
#                 shutil.move(filename, file_label_val)
#                 print(i + "处理成功！")
 
 
 
# if __name__ == '__main__':
#     fileDir = "/home/pbh/yolov5-master/VOCdevkit2/images/" # 源图片文件夹路径
#     tarDir = '/home/pbh/yolov5-master/VOCdevkit2/images_val'  # 图片移动到新的文件夹路径
#     moveimg(fileDir, tarDir)
#     file_list = os.listdir(tarDir)
#     file_label_train = "/home/pbh/yolov5-master/VOCdevkit2/txt_labels/"  # 源图片标签路径
#     file_label_val = "/home/pbh/yolov5-master/VOCdevkit2/txt_labels_val/"  # 标签txt_labels_val
#       # 移动到新的文件路径
#     movelabel(file_list, file_label_train, file_label_val)

def split_dataset(images_dir,txt_dir):

    # 创建images和labels文件夹
    # os.path.join(src_path,"train",exist_ok=True)
    train = "train"
    val = "val"
    train_images_path = os.path.join(images_dir,train)
    val_images_path = os.path.join(images_dir,val)
    train_labels_path = os.path.join(txt_dir,train)
    val_labels_path = os.path.join(txt_dir,val)
    os.makedirs(train_images_path, exist_ok=True)
    os.makedirs(val_images_path, exist_ok=True)
    os.makedirs(train_labels_path, exist_ok=True)
    os.makedirs(val_labels_path, exist_ok=True)
    
    supported_formats = ('.jpg','.jepg','.png','.JPG')
    # 读取图片文件夹中的文件列表
    images = os.listdir(images_dir)
    images = [image for image in images if image.lower().endswith(supported_formats)]

    # 为了保证图片和对应的txt文件对应，我们可以使用文件名的前缀进行匹配
    image_prefixes = [os.path.splitext(image)[0] for image in images]
    
    # 随机打乱文件列表
    random.shuffle(image_prefixes)
    
    # 计算验证集数量（假设为总数据集的20%）
    val_size = int(len(images) * 0.1)
    
    # 将文件划分为训练集和验证集
    train_images = image_prefixes[val_size:]
    val_images = image_prefixes[:val_size]
    
    # 将训练集图片复制到训练集images文件夹
    print(f'确认训练图片的路径是否正确:{train_images_path}')
    for image in train_images:
        try :
            shutil.copy(os.path.join(images_dir, image + ".jpg"), os.path.join(train_images_path, image + ".jpg"))
        except FileNotFoundError as e:
            print(f'该文件不对劲{os.path.join(images_dir,image + ".jpg")}')
            # os.remove(os.path.join(images_dir,image + ".jpg"))
            # print("我把它删掉了！！！")
            continue
    # 将验证集图片复制到验证集images文件夹，并复制对应的txt文件
    for image in val_images:
        try :
            shutil.copy(os.path.join(images_dir, image + ".jpg"), os.path.join(val_images_path, image + ".jpg"))
        except FileNotFoundError as e:
            print(f'该文件不对劲{image}')
            # os.remove(os.path.join(images_dir,image + ".jpg"))
            # print("我把它删掉了！！！")
            continue
        try:
            shutil.copy(os.path.join(txt_dir, image + ".txt"), os.path.join(val_labels_path, image + ".txt"))
        except FileNotFoundError as e:
            print(f'该文件不对劲{image}')
            # os.remove(os.path.join(txt_dir,image + ".txt"))
            print("我把它删掉了！！！")
            continue
        
    # 将训练集和验证集的txt文件复制到labels文件夹对应的train和val文件夹
    for image in train_images:
        try:
            shutil.copy(os.path.join(txt_dir, image + ".txt"), os.path.join(train_labels_path, image + ".txt"))
        except FileNotFoundError as e:
            print(f'该文件不对劲{image}')
            # os.remove(os.path.join(txt_dir,image + ".txt"))
            print("我把它删掉了！！！")
            continue
    # 打印文件数量
    train_images_count = len(os.listdir(train_images_path))
    val_images_count = len(os.listdir(val_images_path))
    train_labels_count = len(os.listdir(train_labels_path))
    val_labels_count = len(os.listdir(val_labels_path))
    
    print(f"训练集图片数量：{train_images_count}")
    print(f"验证集图片数量：{val_images_count}")
    print(f"训练集标签数量：{train_labels_count}")
    print(f"验证集标签数量：{val_labels_count}")


if __name__ == '__main__':
    
    # 删除xml文件中size为0的文件
    # 111111111111111111111111111111111111111111111111111111111111111111
    # delete_xml_size_is_zero(xml_dir)


    #删除图片和xml标签不对应的文件
    #2222222222222222222222222222222222222222222222222222222222222222222
    # cut_diff_file_best(img_dir,xml_dir,best_img_dir, best_xml_dir)

    
    #删除图片和xml标签不对应的文件
    cut_diff_file(  best_xml_dir,best_img_dir)
    #删除图片和txt标签不对应的文件
    # cut_diff_file(images_dir,txt_dir)
    # cut_diff_file(txt_dir,images_dir)

    #统计标签数量
    #33333333333333333333333333333333333333333333333333333333333333333333
    # count_labels_names(xml_dir_best)

    #修改标签名称并查看标签数量
    # change_label_names(xml_dir)

    # count_labels_names(xml_dir)
    
    #voc格式转txt格式
    #44444444444444444444444444444444444444444444444444444444444444444444
    # convert_annotation(xml_dir_best, txt_dir, classes)
    
    #切分训练和验证集
    # moveimg(images_dir,images_val_dir)
    # images_val_dir_filelist = os.listdir(images_val_dir)
    # movelabel(images_val_dir_filelist,txt_dir,labels_val_dir)

    #5555555555555555555555555555555555555555555555555555555555555555555
    # split_dataset(images_dir_best,txt_dir)
    
    # change_label_names(xml_path)
    # count_labels_names(xml_path)
    # convert_annotation(xml_path,txt_path,classes)
    # split_dataset(image_path,txt_path)
    