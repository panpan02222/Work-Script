#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test02.py
@Time    :   2024/03/01 22:19:47
@Author  :   pan binghong 
@Email   :   19909442097@163.com
@description   :   
'''

import os
import  shutil
from tqdm import tqdm

def move_mismatched_files(src_folder,dst_img_folder,dst_xml_folder):
    file_list = os.listdir(src_folder)
    progress_bar = tqdm(file_list,desc='Moving Files',unit='file')


    for filename in progress_bar:
        if filename.endswith('.jpg') or filename.endswith('.JPG'):
            xml_file = os.path.join(src_folder,filename[:-4] + '.xml')
            if not os.path.exists(xml_file):
                src_file = os.path.join(src_folder,filename)
                dst_file = os.path.join(dst_img_folder,filename)
                shutil.move(src_file,dst_file)

        elif filename.endswith('.xml'):
            img_file = os.path.join(src_folder,filename[:-4] + '.jpg')
            if not os.path.exists(img_file):
                src_file = os.path.join(src_folder,filename)
                dst_file = os.path.join(dst_xml_folder,filename)
                shutil.move(src_file,dst_file)
                # xml_file = os.path.splitext(filename)[0]+'.xml'
                # xml_file_path = os.path.join(src_folder,xml_file)
                # shutil.move(xml_file_path,dst_folder)
    print('移动完成')



src_folder = r''
aaa = r''
bbb = r''
move_mismatched_files(src_folder,aaa,bbb)