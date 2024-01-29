import os

##################################依据图片删xml-----mode= 1 ###############################
model = 1
#################################依据xml删图片-----mode= 2 ###############################
# model = 2

images_dir = 'H:\pbh\重新标注样本\VOCdevkit4含26-27-28-29\images'  #xml文件夹
xml_dir = 'H:\pbh\重新标注样本\VOCdevkit4含26-27-28-29\labels'      #jpg文件夹

if model == 1:
    # 创建列表
    xmls = []
    # 读取xml文件名(即：标注的图片名)
    for xml in os.listdir(xml_dir):
        # xmls.append(os.path.splitext(xml)[0])    #append()参数：在列表末尾添加新的对象，即将所有文件名读入列表
        xmls.append(xml.split('.')[0])  # splitext和split的区别：前者('0001','.jpg'), 后者('0001','jpg') 在此可选用
    print(xmls)
    
    # 读取所有图片
    for image_name in os.listdir(images_dir):
        image_name = image_name.split('.')[0]
        if image_name not in xmls:
            image_name = image_name + '.xml'
            print(image_name + '\n')
            os.remove(os.path.join(images_dir, image_name))
    print('处理完成')

if model == 2:
    # 创建列表
    xmls = []
    # 读取xml文件名(即：标注的图片名)
    for xml in os.listdir(xml_dir):
        # xmls.append(os.path.splitext(xml)[0])    #append()参数：在列表末尾添加新的对象，即将所有文件名读入列表
        xmls.append(xml.split('.')[0])  # splitext和split的区别：前者('0001','.jpg'), 后者('0001','jpg') 在此可选用
    print(xmls)
    
    # 读取所有图片
    for image_name in os.listdir(images_dir):
        image_name = image_name.split('.')[0]
        if image_name not in xmls:
            image_name = image_name + '.jpg'
            print(image_name+'\n')
            os.remove(os.path.join(images_dir, image_name))
    print('处理完成')
