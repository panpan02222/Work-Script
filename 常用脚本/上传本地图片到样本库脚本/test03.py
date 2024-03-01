#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test03.py
@Time    :   2024/03/01 22:20:04
@Author  :   pan binghong 
@Email   :   19909442097@163.com
@description   :   
'''

import os
import shutil
import xml.etree.ElementTree as ET

def del_inxml_noobj_file(src_folder,dst_folder):
    for filename in os.listdir(src_folder):
        if filename.endswith('.xml'):
            xml_path = os.path.join(src_folder,filename)

            tree = ET.parse(xml_path)
            root = tree.getroot()

            obj_nodes = root.findall('.//object')
            if len(obj_nodes) == 0:
                dst_path = os.path.join(dst_folder,filename)
                shutil.move(xml_path,dst_path)
                print(f'Moved {filename} to {dst_folder}')

src_folder = r''
dst_folder = r''

del_inxml_noobj_file(src_folder,dst_folder)