from skimage import io
from PIL import Image
import numpy as np
# from elementsWebTest.yolo import OBJ_DETECTION
# import OBJ_DETECTION
import cherrypy
import time,json
import os

import torch
import cv2
from models.experimental import attempt_load
from utils.general import non_max_suppression

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
os.environ['CUDA_VISIBLE_DEVICES']='1'


class OBJ_DETECTION():
    def __init__(self, model_path, classes):
        self.classes = classes
        self.yolo_model = attempt_load(weights=model_path, map_location=device)
        self.input_width = 320

    def detect(self,main_img):
        # np 格式数组切片 --> 转到前两位
        height, width = main_img.shape[:2]
        # print('当前输入图片的高度: ', height)
        # print('当前输入图片的宽度: ', width)
        new_height = int((((self.input_width/width)*height)//32)*32)
        # new_height = 640
        img = cv2.resize(main_img, (self.input_width,new_height))
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        img = np.moveaxis(img,-1,0)
        img = torch.from_numpy(img).to(device)
        img = img.float()/255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        pred = self.yolo_model(img, augment=False)[0]
        pred = non_max_suppression(pred, conf_thres=0.25, iou_thres=0.25, classes=None)
        items = []
        
        if pred[0] is not None and len(pred):
            for p in pred[0]:
                score = np.round(p[4].cpu().detach().numpy(),2)
                label = self.classes[int(p[5])]
                xmin = int(p[0] * main_img.shape[1] /self.input_width)
                ymin = int(p[1] * main_img.shape[0] /new_height)
                xmax = int(p[2] * main_img.shape[1] /self.input_width)
                ymax = int(p[3] * main_img.shape[0] /new_height)

                item = {'label': label,
                        'bbox' : [(xmin,ymin),(xmax,ymax)],
                        'score': score
                        }

                items.append(item)

        return items

# # yaml 文件
# modelname={'jueyuanzi_posun_classes':['jueyuanzi', 'jueyuanzi_posun'],
#            'anquanmao_classes':['wu_anquanmao', 'dai_anquanmao'],
#            'diguagaoyong_classes':['diguagaoyong'],
#            'gongzhuang_classes':['wu_gongzhuang'],
#            'weilan_classes':['weilan'],
#            'biaoshipai_classes':['biaoshipai'],
#            'denggao_classes':['denggao_yrft', 'denggao_wrft']
# } 
# # jueyuanzi-yolov7 对应的是样本库的 模型名称
# model={'jueyuanzi_posun':OBJ_DETECTION('weights/jueyuanzi_posun.pt',modelname['jueyuanzi_posun_classes']),
#        'anquanmao_test0413':OBJ_DETECTION('weights/anquanmao.pt', modelname['anquanmao_classes']),
#        'diguagaoyong_test0413':OBJ_DETECTION('weights/diguagaoyong_3.pt', modelname['diguagaoyong_classes']),
#        'gongzhuang_test0413':OBJ_DETECTION('weights/gongzhuang.pt', modelname['gongzhuang_classes']),
#        'weilan_test0413':OBJ_DETECTION('weights/weilan_p815.pt', modelname['weilan_classes']),
#        'biaoshipai_test0413':OBJ_DETECTION('weights/biaoshipai_p893.pt', modelname['biaoshipai_classes']),
#        'denggao_test0413':OBJ_DETECTION('weights/denggao_p841.pt', modelname['denggao_classes'])
# }

classes = {
    "jiliangbiao_waibu":
        [
        "xiangtifahuang",
        "xiangtixiushi",
        "xiangtiposun",
        "wumen",
        "wuxiang",
        "youfeng",
        "wufeng",
        "youkaiguangai",
        "wukaiguangai",
        "youtoushichuanggai",
        "wutoushichuanggai"
        ]
}

model = {
    "jiliangbiao_waibu":OBJ_DETECTION('weights/jiliangbiao_waibu.pt',classes["jiliangbiao_waibu"])
}


class YoloServer():
    def __init__(self):
        return

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def index(self):
        input_json = cherrypy.request.json
        print(input_json)
        queryData = {
            'imageName': input_json['imageName'],
            'imageURL': input_json['imageURL'],
            'modelName': input_json['modelName']
        }
        img = io.imread(queryData['imageURL'])
        time_start = int(time.time()*1000)
        results = []
        rv = {'imageName':queryData['imageName'], 'imageURL':queryData['imageURL'], 'modelName':queryData['modelName']}
        for modelName in rv['modelName']:
            print(modelName)
            dets = model[modelName].detect(img)
            time_end = int(time.time() * 1000)
            duration = time_end - time_start
            for od in dets:
                bbox = od['bbox']
                mp = {
                    'type': od['label'],
                    'modelname': modelName,
                    'score': str(od['score']),
                    'time': duration,
                    'xmin': bbox[0][0],
                    'ymin': bbox[0][1],
                    'xmax': bbox[1][0],
                    'ymax': bbox[1][1],
                }
                results.append(mp)
                print(mp)
        rv['results'] = results
        return rv

if __name__ == '__main__':
    cherrypy.server.socket_host = '0.0.0.0'
    cherrypy.config.update({'server.socket_port': 10010})
    cherrypy.response.headers['Content-Type'] = 'application/json'
    cherrypy.quickstart(YoloServer())
