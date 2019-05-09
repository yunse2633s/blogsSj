# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 13:57:35 2019

@author: admin

作用：
    根据face009_face_train.py所训练的模型，识别视频中的人员
"""


import cv2
import sys
import gc
from face009_face_train import Model


IMG_PATH='G:/work/vod/axis'
OPENCV_PATH = r"d:/Program Files (x86)/python/Lib/site-packages/cv2/data" 
vod='F:\监控摄像头视频\MVI_1423.mp4' 

if __name__ == '__main__':
    if len(sys.argv) != 1:
        print("Usage:%s camera_id\r\n" % (sys.argv[0]))
        sys.exit(0)
        
    #加载模型
    model = Model()
    model.load_model(file_path = IMG_PATH + '/data/face.model.h5')    
              
    #框住人脸的矩形边框颜色       
    color = (0, 255, 0)
    cv2.namedWindow('a_window', 0)
    
    #捕获指定摄像头的实时视频流
    cap = cv2.VideoCapture(vod)
    vod_width=cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    vod_height=cap.get(cv2.CAP_PROP_FRAME_HEIGHT)    
    x = int(vod_width / 2)
    y = int(vod_height / 2) 
    cv2.resizeWindow("a_window", x,y)
    
    #人脸识别分类器本地存储路径
    cascade_path = OPENCV_PATH+"/haarcascade_frontalface_alt2.xml"    
    
    #循环检测识别人脸
    while True:
        ret, frame = cap.read()   #读取一帧视频
        
        if ret is True:
            
            #图像灰化，降低计算复杂度
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            continue
        #使用人脸识别分类器，读入分类器
        cascade = cv2.CascadeClassifier(cascade_path)                
 
        #利用分类器识别出哪个区域为人脸
        faceRects = cascade.detectMultiScale(frame_gray, scaleFactor = 1.3, minNeighbors = 5)        
        if len(faceRects) > 0:                 
            for faceRect in faceRects: 
                x, y, w, h = faceRect
                
                #截取脸部图像提交给模型识别这是谁
                image = frame[y - 10: y + h + 10, x - 10: x + w + 10]
                faceID = model.face_predict(image)   
                '''
                #如果是“我”
                if faceID == 0:                                                        
                    cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), color, thickness = 2)
                    
                    #文字提示是谁
                    cv2.putText(frame,'liziqiang', 
                                (x + 30, y + 30),                      #坐标
                                cv2.FONT_HERSHEY_SIMPLEX,              #字体
                                1,                                     #字号
                                (255,0,255),                           #颜色
                                2)                                     #字的线宽
                else:
                    pass
                '''
                cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), color, thickness = 2)
                #文字提示是谁
                rec_name= 'left' if faceID==1 else 'center' if faceID==2 else 'right' if faceID==3 else 'null'
                print('faceID:',faceID)
                cv2.putText(frame,rec_name,(x + 30, y + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,255), 2)
                            
        cv2.imshow("a_window", frame)
        
        #等待10毫秒看是否有按键输入
        k = cv2.waitKey(1)
        #如果输入q则退出循环
        if k & 0xFF == ord('q'):
            break
 
    #释放摄像头并销毁所有窗口
    cap.release()
    cv2.destroyAllWindows()