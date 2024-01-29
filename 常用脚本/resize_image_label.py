import os
import cv2
import xml.etree.ElementTree as ET

def resize_images_and_labels(image_dir, label_dir, output_dir, target_size):
    os.makedirs(output_dir, exist_ok=True)
    
    image_files = os.listdir(image_dir)
    label_files = os.listdir(label_dir)
    
    for image_file, label_file in zip(image_files, label_files):
        # 读取图片
        image_path = os.path.join(image_dir, image_file)
        image = cv2.imread(image_path)
        
        # 读取标签文件
        label_path = os.path.join(label_dir, label_file)
        try:
            print(f'处理的xml文件为：{label_path}')
            tree = ET.parse(label_path)
        except ET.ParseError as e:
            print(f"{label_path} - 无法解析 XML 文件：{e}")
            continue
        root = tree.getroot()
        
        # 获取原始图片的尺寸
        original_width = int(root.find('size/width').text)
        original_height = int(root.find('size/height').text)
        
        # 计算调整后的尺寸
        width_ratio = target_size[0] / original_width
        height_ratio = target_size[1] / original_height
        
        # 调整图片尺寸
        resized_image = cv2.resize(image, target_size)
        
        # 调整标签文件中的坐标信息
        for obj in root.findall('object'):
            bbox = obj.find('bndbox')
            xmin = int(bbox.find('xmin').text)
            ymin = int(bbox.find('ymin').text)
            xmax = int(bbox.find('xmax').text)
            ymax = int(bbox.find('ymax').text)
            
            xmin = int(xmin * width_ratio)
            ymin = int(ymin * height_ratio)
            xmax = int(xmax * width_ratio)
            ymax = int(ymax * height_ratio)
            
            bbox.find('xmin').text = str(xmin)
            bbox.find('ymin').text = str(ymin)
            bbox.find('xmax').text = str(xmax)
            bbox.find('ymax').text = str(ymax)
        
        # 保存调整后的图片和标签文件
        image_filename , label_filename = 'image' , 'label'
        newpath1 = os.path.join(output_dir,image_filename)
        os.makedirs(newpath1,exist_ok=True)
        newpath2 = os.path.join(output_dir,label_filename)
        os.makedirs(newpath2,exist_ok=True)
        resized_image_path = os.path.join(newpath1, image_file)
        resized_label_path = os.path.join(newpath2, label_file)

        cv2.imwrite(resized_image_path, resized_image)
        tree.write(resized_label_path)
        
        print(f"Resized image and label: {image_file}, {label_file}")



# 示例用法
image_dir = r'C:\Users\Administrator\Desktop\detect_jueyuanzi\JPEGlmages'
# image_dir = r'G:\Pan_BingHong\Jiliangbiao_DataSets\VOCdevkit_3-1\test02'
label_dir = r'C:\Users\Administrator\Desktop\detect_jueyuanzi\Annotations'
# label_dir = r'G:\Pan_BingHong\Jiliangbiao_DataSets\VOCdevkit_3-1\test'
output_dir = r'C:\Users\Administrator\Desktop'
target_size = (1280, 1280)

resize_images_and_labels(image_dir, label_dir, output_dir, target_size)