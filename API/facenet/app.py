#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   app.py
@Time    :   2024/02/26 10:22:01
@Author  :   pan binghong 
@Email   :   19909442097@163.com
@description   :   实现基于Facenet的人脸检测接口代码
'''

import os
import time
import numpy as np
from flask import Flask, request, jsonify
from PIL import Image
from io import BytesIO
import requests
import torch
from facenet_pytorch import MTCNN, InceptionResnetV1
import json
import pickle

app = Flask(__name__)

# 加载MTCNN和InceptionResnetV1模型
device = 'cuda' if torch.cuda.is_available() else 'cpu'
mtcnn = MTCNN(keep_all=True, device=device)
resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)

# 存储人脸特征的字典
features_dict = {}

# 存储路径和文件夹数量上限
storage_path = './Face data'
max_folders = 50

# 创建存储路径和检查文件夹数量
if not os.path.exists(storage_path):
    os.makedirs(storage_path)
folder_count = len(os.listdir(storage_path))

# 上传图片并保存人脸特征
@app.route('/upload', methods=['POST'])
def upload():
   
    data = request.json
    imageURL = data.get('imageURL')
    person_name = data.get('personName')
    
    response = requests.get(imageURL)
    img = Image.open(BytesIO(response.content))

    x_aligned, prob = mtcnn(img, return_prob=True)
    if x_aligned is None:
        return jsonify({'success': False, 'message': 'No face detected in the image'})

    # 创建存储文件夹
    folder_path = os.path.join(storage_path, str(person_name))
    print(folder_path)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # 保存图片到文件夹
    img_path = os.path.join(folder_path, f'{person_name}.jpg')
    img.save(img_path)
    x_aligned = x_aligned.to(device)
    embedding = resnet(x_aligned).detach().to(device)
    # embedding = resnet(x_aligned.unsqueeze(0).to(device)).detach().cpu().numpy().tolist()[0]

    features_dict[person_name] = embedding

    folder_count = len(os.listdir(storage_path))
    if folder_count > max_folders:
        return jsonify({'success': True, 'message': 'Image uploaded successfully', 
                        'folder_count': folder_count, 'max_folders': max_folders})
    
    return jsonify({'success': True, 'message': 'Image uploaded successfully'})

# 比对图片并输出相似度、姓名和耗时
@app.route('/recognize', methods=['POST'])
def recognize():
    with open('features_dict.pkl', 'rb') as f:
        features_dict = pickle.load(f)
    print(features_dict)
    data = request.json
    imageURL = data.get('imageURL')

    response = requests.get(imageURL)
    img = Image.open(BytesIO(response.content))

    start_time = time.time()

    x_aligned, prob = mtcnn(img, return_prob=True)
    if x_aligned is None:
        return jsonify({'success': False, 'message': 'No face detected in the image'})
    x_aligned = x_aligned.to(device)
    embedding = resnet(x_aligned).detach().to(device)
#    embedding = resnet(x_aligned.unsqueeze(0).to(device)).detach().cpu().numpy().tolist()[0]

    min_dist = float('inf')
    min_name = None
    for name, saved_embedding in features_dict.items():
        print('name')

        dist = np.linalg.norm(np.array(embedding.cpu()) - np.array(saved_embedding.cpu()))
        print(dist)
        if dist < min_dist:
            min_dist = dist
            min_name = name

    end_time = time.time()
    elapsed_time = end_time - start_time

    similarity = 100 - (min_dist * 100)
    if similarity < 90:
        return jsonify({'sucess' : False, 'message' : 'No face information was entered'})
    result = {
        'similarity': f'{similarity:.2f}%',
        'name': min_name,
        'elapsed_time': f'{elapsed_time:.2f}ms'
    }

    return jsonify({'success': True, 'result': result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=18181, debug=True)


