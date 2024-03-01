#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   find_and_moveout_the_match_xml_and_jpg.py
@Time    :   2024/03/01 22:33:24
@Author  :   pan binghong 
@Email   :   19909442097@163.com
@description   :   曹振给我的代码
'''

import shutil
import os
import tqdm

Source_xml_path = './source_xml'
Object_xml_path = 'G:\Pan_BingHong\Jiliangbiao_DataSets\VOCdevkit_3-1\after_resize_1280v2\images\new_'
Source_jpg_path = 'G:\Pan_BingHong\Jiliangbiao_DataSets\VOCdevkit_3-1\after_resize_1280v2\images\train'
Object_jpg_path = 'G:\Pan_BingHong\Jiliangbiao_DataSets\VOCdevkit_3-1\after_resize_1280v2\images\new_train'

xml_list = os.listdir(Source_xml_path)
jpg_list = os.listdir(Source_jpg_path)
n = len(xml_list)
count = 0

for i in tqdm.trange(n):
    for ajpg in jpg_list:
        if ajpg[:-4] == xml_list[i][:-4]:
            shutil.copy(Source_xml_path + '/' + xml_list[i], Object_xml_path + '/' + xml_list[i])
            shutil.copy(Source_jpg_path + '/' + ajpg, Object_jpg_path + '/' + ajpg)
            count = count + 1
            break
print('\ndone. 共移动',count,'对xml和jpg对应的文件.')