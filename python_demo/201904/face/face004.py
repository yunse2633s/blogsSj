# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 10:29:07 2019

@author: admin
环境：
    python v3.7.1
    opencv v4.0
    tensorflow v1.13.1
    numpy v1.16.2
作用：
    1. 链接AXIS 213 PTZ Network Camera
    2. 链接网络摄像机
    3. 人流量
    3. 视频图卡顿，可以配置高频摄像参数
参照:
    
完成度90%  
    
"""

import cv2
#import sys
from PIL import Image
import numpy as np
import time


def CatchUsbVideo(window_name, camera_idx):
    
    #视频来源，可以来自一段已存好的视频，也可以直接来自USB摄像头
    #cap = cv2.VideoCapture("g:/work/vod/vid_suj.mp4")                
    #cap = cv2.VideoCapture(camera_idx)                
    cap = cv2.VideoCapture(cv2.CAP_DSHOW) #读取高振
    cap.open(camera_idx)
    OPENCV_PATH = r"d:/Program Files (x86)/python/Lib/site-packages/cv2/data" 
    #告诉OpenCV使用人脸识别分类器
    #classfier = cv2.CascadeClassifier(OPENCV_PATH + "/haarcascade_frontalface_default.xml")
    #classfier = cv2.CascadeClassifier(OPENCV_PATH + "/haarcascade_frontalface_alt.xml")
    #classfier = cv2.CascadeClassifier(OPENCV_PATH + "/haarcascade_frontalface_alt2.xml")
    #
    classfier = cv2.CascadeClassifier(OPENCV_PATH + "/haarcascade_upperbody.xml")
    #classfier = cv2.CascadeClassifier(OPENCV_PATH + "/haarcascade_profileface.xml")
    #classfier = cv2.CascadeClassifier(OPENCV_PATH + "/haarcascade_frontalcatface.xml")
    #classfier = cv2.CascadeClassifier(OPENCV_PATH + "/haarcascade_licence_plate_rus_16stages.xml")
    # 检测行人 “H:\swap\opencv\data\hogcascades\hogcascade_pedestrians.xml”
    #classfier=cv2.CascadeClassifier("H:/swap/opencv/data/hogcascades/hogcascade_pedestrians.xml")
    
    #识别出人脸后要画的边框的颜色，RGB格式
    color = (0, 255, 0)
    

    i=0
    sum=0
    while cap.isOpened():
        ok, frame = cap.read() #读取一帧数据
        
        if not ok:            
            break  
        
        ### 横屏转竖屏 start
        # 将每一帧左旋转90度
        #frame=cv2.transpose(frame)
        #frame=cv2.flip(frame,-1)
        ### 横屏转竖屏 end
        
        t1=time.time()*1000
        #''' 如果不进行计算，直接显示视频帧，
        #如果执行计算，那么响应时间多长 :100毫秒
        #将当前帧转换成灰度图像
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)                 
        
        #人脸检测，1.2和2分别为图片缩放比例和需要检测的有效点数
        #faceRects = classfier.detectMultiScale(grey, scaleFactor = 1.2, minNeighbors = 3, minSize = (32, 32))
        faceRects = classfier.detectMultiScale(grey, scaleFactor = 1.2, minNeighbors = 3)
        if len(faceRects) > 0:            #大于0则检测到人脸                                   
            for faceRect in faceRects:  #单独框出每一张人脸
                x, y, w, h = faceRect        
                cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), color, 2)
                        
        #显示图像
        #'''
        t2=time.time()*1000
        t3=t2-t1
        i=i+1
        sum=sum+t3
        print("sn:%i,t1:%d,t2:%d, run: %d"%(i,t1,t2,t3))
        cv2.imshow(window_name, frame)
        # waitKey()方法本身表示等待键盘输入
        c = cv2.waitKey(1)
            
        if c & 0xFF == ord('q'):
            avg=sum/i
            print('sum:%d,i:%d,avg:%d'%(sum,i,avg))
            break        
    
    #释放摄像头并销毁所有窗口
    cap.release()
    cv2.destroyAllWindows() 

'''  
if __name__ == '__main__':
    if len(sys.argv) != 1:
        print("Usage:%s camera_id\r\n" % (sys.argv[0]))
    else:
        CatchUsbVideo("识别人脸区域", 0)
'''

#vodadd = "http://192.168.1.103/axis-cgi/mjpg/video.cgi?user=root&pwd=123456"
#vodadd = "http://192.168.1.103/axis-cgi/mjpg/video.cgi"
vodadd = "http://root:123456@192.168.1.103/axis-cgi/mjpg/video.cgi?resolution=1280x1024"

CatchUsbVideo("ipCamer", vodadd)

