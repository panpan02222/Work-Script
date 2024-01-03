
from PIL import Image
from io import BytesIO
import numpy as np
from flask import Flask, request, jsonify
import cv2,os,torch,requests
from models.experimental import attempt_load
from utils.general import non_max_suppression
import base64
from datetime import datetime
import time
import pandas as pd
import json

import warnings
warnings.filterwarnings("ignore")

classes =         [
        "050111",
        "051512",
        "050113",
        "051501",
        "050101",
        "youfeng",
        "050301",
        "youkaiguangai",
        "051503",
        "youtoushichuanggai",
        "051601"
        ]

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class YoloServer():
    def __init__(self,model_path):
        self.model = attempt_load(weights=model_path,map_location=None)
        self.input_width = 640
        self.classes = classes
        self.model.to(dtype=torch.float32)
        self.model.to(device).eval()

    def process_detection(self, image_input):
        img_BGR = np.array(Image.open(image_input))
        # 检查是否为RGB格式，如果不是则转换为RGB格式
        if img_BGR.shape[-1] == 1:  # 灰度图像
            img = cv2.cvtColor(img_BGR, cv2.COLOR_GRAY2RGB)
        elif img_BGR.shape[-1] == 3:  # RGB图像
            img = cv2.cvtColor(img_BGR, cv2.COLOR_BGR2RGB)
        else:  # 其他格式
            raise ValueError("Image format not supported! Only grayscale and RGB images are supported.")

        h,w = img.shape[:2]
        img = cv2.resize(img, (self.input_width,self.input_width))
        print(f'after_resize:{img.shape}') 
        print('*'*30)

        img = np.array(img).transpose(2,0,1)
        print(f'after_transpose:{img.shape}')
        print('*'*30)
        img = torch.from_numpy(img).to(device)
        img = img.float() / 255.0
        img = img.unsqueeze(0)
        print(f'after_unsqueeze:{img.shape}')

        start_time = time.time()
        results = self.model(img)[0]

        results = non_max_suppression(results)
        print('*'*30)
        end_time = time.time()
        inference_time = round(end_time - start_time, 4)
        
        for i ,det in enumerate(results):
            cc = []
            if det is not None and len(det):
                for *xyxy, conf, cls in reversed(det):
                    label = "%s" % (self.classes[int(cls)])
                    score = "%.2f"%conf
                    # x1,y1,x2,y2 = int(xyxy[0]*w/self.input_width),int(xyxy[1]*h/nh),int(xyxy[2]*w/self.input_width),int(xyxy[3]*h/nh)
                    x1,y1,x2,y2 =int(xyxy[0]*w/self.input_width),int(xyxy[1]*h/self.input_width),int(xyxy[2]*w/self.input_width),int(xyxy[3]*h/self.input_width)
                    cc.append({"type":label,"score":score,"xmin":x1,"ymin":y1,"xmax":x2,"ymax":y2,"time":inference_time})
                return cc



app=Flask(__name__)

@app.route('/',methods=['POST'])
def pred():
    t0 = time.time()                 #1.记录当前时间功能
    current_time = datetime.now()    #2.调用本次接口耗时功能
    print("当前时间为：",current_time)

    with torch.no_grad():
    # if request.headers['Content-Type'] == 'application/json':
        input_json = request.json
        print('=========================start detect===========================')

        #传递入参
        imageName = input_json['imageName']
        print(f'input imageName : {imageName}')

        imageURL = input_json.get('imageURL')
        print(f'input imageURL :{imageURL}')
        imageBase64 = input_json.get('imageBase64')

        modelName = input_json['modelName']
        print(f'input modelName : {modelName}')

        model_path = os.path.join('./weights/',f'{str(modelName[0])}.pt')
        # print(f'model path : {model_path}')

        yolo_server = YoloServer(model_path)

        if imageURL:
            print("本次传入图片类型为:imageURL")
            img_data = BytesIO(requests.get(imageURL).content)
        elif imageBase64:
            print("本次传入图片类型为:imageBase64")
            img_data = BytesIO(base64.b64decode(imageBase64))
        else:
            print("请输入正确的图片格式！！！")


        out = yolo_server.process_detection(img_data)
        if out:
            out = {"imageURL":imageURL,"imageName":imageName,"results":out}
        else:
            out = {"imageURL":imageURL,"imageName":imageName,"results":[]}

        t1 = time.time()
        print("调用本次接口总耗时:",t1-t0)
        print('=========================complete!!!===========================')
        # 打印每日调用次数
        return jsonify(out)

        # else:
        #     print("本次传入图片类型为：imageBinary")
        #     img_data = request.get_data()
        #     out = yolo_server.process_detection(img_data)
        #     if out:
        #         out = {"results":out}
        #     else:
        #         out = {"results":[]}
        #     return jsonify(out)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=10021,debug=True)
