#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   提取文件.py
@Time    :   2024/03/01 22:32:15
@Author  :   pan binghong 
@Email   :   19909442097@163.com
@description   :   
'''

import os
import shutil

def move_files(source_folder,destination_folder):
    # for filename in os.listdir(source_folder):
    for root,dirs,files in os.walk(source_folder):
        for filename in files:
            source_file = os.path.join(root,filename)
        # if os.path.isfile(source_file):
            destination_file = os.path.join(destination_folder,filename)
            shutil.move(source_file,destination_file)
    print("finished")

# 这里放置你的docx文件夹
source_folder = r""
from docx import Document
def convert_docx_to_doc(source_folder):
    files = os.listdir(source_folder)
    for filename in files:
        if filename.endswith('.docx'):
            source_file=os.path.join(source_folder,filename)
            doc=Document(source_file)
            destination_file = os.path.splitext(source_file)[0]+".doc"
            doc.save(destination_file)
    print("convert finished!!!")
# convert_docx_to_doc(source_folder)

import os
from docx import Document
import win32com.client as win32

def convert_doc_to_docx(source_folder):
    files = os.listdir(source_folder)
    word = win32.gencache.EnsureDispatch("Word.Application")
    for filename in files:
        if filename.endswith('.doc'):
            source_file = os.path.join(source_folder,filename)
        # try:
        # word = win32.gencache.EnsureDispatch("Word.Application")
        doc = word.Document.Open(source_file)
        destination_file = os.path.splitext(source_file)[0]+"docx"
        doc.SaveAs(destination_file,16)
        doc.Close()
        # doc.Quit()
        print(f'已转{source_file}-->{destination_file}')
        # except Exception as e:
        #     print("转不了一点:",{source_file})
    print("convert finished!!!")
    word.Quit()

convert_doc_to_docx(source_folder)
