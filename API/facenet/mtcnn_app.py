#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   mtcnn_app.py
@Time    :   2024/02/26 11:08:41
@Author  :   pan binghong 
@Email   :   19909442097@163.com
@description   :   实现基于mtcnn网络进行人脸识别的接口代码
'''

from flask import Flask, jsonify, request
from PIL import Image, ImageDraw
from facenet_pytorch import MTCNN, extract_face
import requests
import io
import base64
import time

app = Flask(__name__)

mtcnn = MTCNN(keep_all=True)

@app.route('/', methods=['POST'])
def detect_faces():
    # Parse JSON request
    json_data = request.get_json()

    image_url = json_data.get('imageURL')

    image_base64 = json_data.get("imageBase64")

    image_name = json_data['imageName']
    model_name = json_data['modelName']

    if image_url:
        # Download image from URL
        response = requests.get(image_url)
        img = Image.open(io.BytesIO(response.content))

        # Detect faces
        t0 = time.time()
        boxes, probs, points = mtcnn.detect(img, landmarks=True)
        t1 = time.time()
        inference_time = round(t1-t0, 4)
        boxes = [[round(num) for num in sublist] for sublist in boxes]
        print(boxes)
        results = []
        results.append(
            {
                'num_faces': len(boxes),
                'face_boxes': boxes
            }
        )
        # Format response
        response = {

            "results" : results,
            # 'imageURL' : image_url,
            'imageName' : image_name,
            'modelNmae': model_name,
            'time' : inference_time
        }
        return jsonify(response)
    elif image_base64:
        # Download image from URL
        response = base64.b64decode(image_base64)
        img = Image.open(io.BytesIO(response))

        # Detect faces
        t0 = time.time()
        boxes, probs, points = mtcnn.detect(img, landmarks=True)
        inference_time = round(time.time()-t0, 4)
        boxes = [[round(num) for num in sublist] for sublist in boxes]
        print(boxes)
        results = []
        results.append(
            {
                'num_faces': len(boxes),
                'face_boxes': boxes
            }
        )
        # Format response
        response = {

            "results" : results,
            # 'imageURL' : image_url,
            'imageName' : image_name,
            'modelNmae': model_name,
            'time' : inference_time
        }
        return jsonify(response)

if __name__ == '__main__':
    app.run(port=8080,debug=True)