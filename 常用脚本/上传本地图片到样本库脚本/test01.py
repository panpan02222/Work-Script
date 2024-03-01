#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test01.py
@Time    :   2024/03/01 22:19:40
@Author  :   pan binghong 
@Email   :   19909442097@163.com
@description   :   
'''

import os 
import shutil

def copy_files(src_folders,dst_folder,duplicate_folder):
    for i ,src_folder in enumerate(src_folders):
        print(f'copying files from folder {i+1} of 25')
        for root,dirs,files in os.walk(src_folder):
            print(src_folder)
            for file in files:
                if file.endswith('.rar'):
                    continue
                src_path = os.path.join(root,file)
                base_name,ext = os.path.splitext(file)
                duplicate_path = os.path.join(duplicate_folder,file)
                if os.path.exists(duplicate_path):
                    print(f'skipping {file} as it already exists in the duplicate folder!!!')
                    continue
                dst_path = os.path.join(dst_folder,file)
                shutil.copy(src_path,dst_path)
                print(f'copy {file} from {src_path} to {dst_path}')
            if not files and not dirs:
                print('{os.path.basename(root)} not has file')

src_folders = []  
dst_folders = r""
duplicate_folder = r''
copy_files(src_folders,dst_folders,duplicate_folder)