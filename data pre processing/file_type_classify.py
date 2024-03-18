#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   file_type_classify.py
@Time    :   2024/03/18 16:34:50
@Author  :   pan binghong 
@Email   :   19909442097@163.com
@description   :   
'''

import os  
import shutil  
from tqdm import tqdm  
  
def organize_files_by_extension(folder_path):  
    # 获取指定文件夹下的所有文件（不包括子文件夹中的文件）  
    files_to_process = []  
    for root, dirs, files in os.walk(folder_path):  
        for filename in files:  
            files_to_process.append(os.path.join(root, filename))  
  
    # 使用tqdm创建进度条  
    with tqdm(total=len(files_to_process), desc="正在整理文件", ncols=100) as pbar:  
        for src_file in files_to_process:  
            file_extension = os.path.splitext(os.path.basename(src_file))[1].lower()  # 获取文件后缀名并转换为小写  
            if file_extension:  # 排除没有后缀的文件  
                # 创建对应后缀的文件夹（如果不存在）  
                file_dir = os.path.dirname(src_file)  
                dest_folder = os.path.join(file_dir, file_extension[1:])  
                if not os.path.exists(dest_folder):  
                    os.makedirs(dest_folder)  
                # 获取文件名（不带路径）  
                filename = os.path.basename(src_file)  
                # 移动文件到对应的文件夹下  
                dest_file = os.path.join(dest_folder, filename)  
                shutil.move(src_file, dest_file)  
            # 更新进度条  
            pbar.update()  
  
if __name__ == "__main__":  
    folder_path = r""  
    organize_files_by_extension(folder_path)  
    print("文件整理完成！")