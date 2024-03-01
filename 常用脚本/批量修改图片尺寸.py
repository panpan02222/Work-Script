#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   批量修改图片尺寸.py
@Time    :   2024/03/01 22:31:27
@Author  :   pan binghong 
@Email   :   19909442097@163.com
@description   :   
'''


from PIL import image
import os.path
import glob

def convertjpg(jpgfile,outdir,width=640,height=640):
	img = Image.open(file)
	try :
		new_img = img.resize((width,height),Image.BILINEAR)
		if not os.path.exists(outdir):
			os.mkdir(outdir)
		new_img.save(os.path.join(outdir,os.path.basename(jpgfile)))
	except Exception as e:
		print(e)

path = "G:\Pan_BingHong\原图\*.jpg"
dst_path = "G:\Pan_BingHong\修改后\\"


for jpgfile in glob.glob(path):
	convertjpg(jpgfile,dst_path)