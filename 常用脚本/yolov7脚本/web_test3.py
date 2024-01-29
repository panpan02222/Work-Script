from skimage import io
from PIL import Image
import numpy as np
from elementsWebTest.yolo import OBJ_DETECTION
# import OBJ_DETECTION
import cherrypy
import time,json
import os
os.environ['CUDA_VISIBLE_DEVICES']='1'
# yaml 文件
modelname={'jueyuanzi_posun_classes':['jueyuanzi', 'jueyuanzi_posun'],
           'anquanmao_classes':['wu_anquanmao', 'dai_anquanmao'],
           'diguagaoyong_classes':['diguagaoyong'],
           'gongzhuang_classes':['wu_gongzhuang'],
           'weilan_classes':['weilan'],
           'biaoshipai_classes':['biaoshipai'],
           'denggao_classes':['denggao_yrft', 'denggao_wrft']
} 
# jueyuanzi-yolov7 对应的是样本库的 模型名称
model={'jueyuanzi_posun':OBJ_DETECTION('weights/jueyuanzi_posun.pt',modelname['jueyuanzi_posun_classes']),
       'anquanmao_test0413':OBJ_DETECTION('weights/anquanmao.pt', modelname['anquanmao_classes']),
       'diguagaoyong_test0413':OBJ_DETECTION('weights/diguagaoyong_3.pt', modelname['diguagaoyong_classes']),
       'gongzhuang_test0413':OBJ_DETECTION('weights/gongzhuang.pt', modelname['gongzhuang_classes']),
       'weilan_test0413':OBJ_DETECTION('weights/weilan_p815.pt', modelname['weilan_classes']),
       'biaoshipai_test0413':OBJ_DETECTION('weights/biaoshipai_p893.pt', modelname['biaoshipai_classes']),
       'denggao_test0413':OBJ_DETECTION('weights/denggao_p841.pt', modelname['denggao_classes'])
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
    cherrypy.config.update({'server.socket_port': 10054})
    cherrypy.response.headers['Content-Type'] = 'application/json'
    cherrypy.quickstart(YoloServer())
