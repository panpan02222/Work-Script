#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   count_folder.py
@Time    :   2024/02/29 10:28:00
@Author  :   pan binghong 
@Email   :   19909442097@163.com
@description   :   统计文件夹下所有的文件个数, 同时如果文件夹下是图片类型的文件, 则将该文件夹下的所有图片文件的个数, 统计为1个文件。最终输出文件个数。空的文件名称。
'''

import os

def count_files(folder_path):
    total_files = 0
    image_files = 0
    empty_files = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            
            # 统计文件个数
            total_files += 1

            # 如果是图片文件，增加图片文件计数
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')):
                image_files += 1

            # 如果文件为空，记录空文件名
            if os.path.getsize(file_path) == 0:
                empty_files.append(file_path)

    # 如果存在图片文件，将图片文件的数量统计为1
    if image_files > 0:
        total_files -= (image_files - 1)

    return total_files, empty_files

def process_folders(root_folder):
    for folder in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder)
        if os.path.isdir(folder_path):
            total_files, empty_files = count_files(folder_path)
            print(f"文件夹: {folder}, 总文件个数: {total_files}")
            if empty_files:
                print("空文件名列表:")
                for empty_file in empty_files:
                    print(empty_file)
            print("\n")

# 指定根文件夹路径
root_folder_path = "/path/to/your/root/folder"

# 调用函数进行处理
process_folders(root_folder_path)

