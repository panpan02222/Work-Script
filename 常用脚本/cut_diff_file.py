import os
import shutil

# 原始文件夹1
src_folder1 = "/home/pbh/yolov5-master/VOCdevkit/labels"
# 原始文件夹2
src_folder2 = "/home/pbh/yolov5-master/VOCdevkit/images"
# 目标文件夹
dst_folder = "/home/pbh/yolov5-master/VOCdevkit/dst"

# 获取原始文件名列表及其路径
src_files1 = {}
src_files2 = {}

# 递归遍历文件夹1和其中的文件
for root, dirs, files in os.walk(src_folder1):
    for file in files:
        file_name = os.path.splitext(file)[0]
        file_path = os.path.join(root, file)
        src_files1[file_name] = file_path

# 递归遍历文件夹2和其中的文件    
for root, dirs, files in os.walk(src_folder2):
    for file in files:
        file_name = os.path.splitext(file)[0]
        file_path = os.path.join(root, file)
        src_files2[file_name] = file_path

# 比较两个文件夹中的文件名，将名称不同的文件剪切到目标文件夹
for file_name in src_files1.keys():
    if file_name not in src_files2.keys():
        src_path = src_files1[file_name]
        dst_path = os.path.join(dst_folder, os.path.basename(src_path))
        shutil.move(src_path, dst_path)
        print(f"移动文件 {src_path} 到目标文件夹")

for file_name in src_files2.keys():
    if file_name not in src_files1.keys():
        src_path = src_files2[file_name]
        dst_path = os.path.join(dst_folder, os.path.basename(src_path))
        shutil.move(src_path, dst_path)
        print(f"移动文件 {src_path} 到目标文件夹")