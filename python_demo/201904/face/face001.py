# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 11:45:42 2019

@author: admin
环境：
    python v3.7.1
    opencv v4.0
    tensorflow v1.13.1
    numpy v1.16.2
作用：
    1，测试各种构造器在视频流的人脸识别
    2，测试横屏旋转为竖屏


"""


import cv2
import sys
from PIL import Image
import numpy as np


def CatchUsbVideo(window_name, camera_idx):
    
    #视频来源，可以来自一段已存好的视频，也可以直接来自USB摄像头
    #cap = cv2.VideoCapture("g:/work/vod/vid_suj.mp4")                
    #cap = cv2.VideoCapture("F:/蚂蚁儿童乐园/came3_2019-03-24__13-00-00_13-59-59__CAM3.avi") 
    cap = cv2.VideoCapture("F:\监控摄像头视频\MVI_1423.mp4")               
    
    OPENCV_PATH = r"d:/Program Files (x86)/python/Lib/site-packages/cv2/data" 
    #告诉OpenCV使用人脸识别分类器
    #classfier = cv2.CascadeClassifier(OPENCV_PATH + "/haarcascade_frontalface_default.xml")
    #classfier = cv2.CascadeClassifier(OPENCV_PATH + "/haarcascade_frontalface_alt.xml")
    classfier = cv2.CascadeClassifier(OPENCV_PATH + "/haarcascade_frontalface_alt2.xml")
    #
    #classfier = cv2.CascadeClassifier(OPENCV_PATH + "/haarcascade_upperbody.xml")
    #classfier = cv2.CascadeClassifier(OPENCV_PATH + "/haarcascade_profileface.xml")
    #classfier = cv2.CascadeClassifier(OPENCV_PATH + "/haarcascade_frontalcatface.xml")
    #classfier = cv2.CascadeClassifier(OPENCV_PATH + "/haarcascade_licence_plate_rus_16stages.xml")
    
    
    #识别出人脸后要画的边框的颜色，RGB格式
    color = (0, 255, 0)
    
    ### 横屏转竖屏 start
    '''
    因手机录制的视频，读取后由竖屏转横屏，所以需要做一些处理
     1,将窗口设置为用户自定义
     2,获取视频的尺寸
     3,设置窗口尺寸
     4,旋转图片
    '''     
    #cv2.namedWindow(window_name, 0)
    #vod_width=cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    #vod_height=cap.get(cv2.CAP_PROP_FRAME_HEIGHT)    
    #x = int(vod_width / 2)
    #y = int(vod_height / 2) 
    #cv2.resizeWindow(window_name, y,x)
    ### 横屏转竖屏 end
        
    while cap.isOpened():
        ok, frame = cap.read() #读取一帧数据
        if not ok:            
            break  
        
        ### 横屏转竖屏 start
        # 将每一帧左旋转90度
        #frame=cv2.transpose(frame)
        #frame=cv2.flip(frame,-1)
        ### 横屏转竖屏 end
        
        #将当前帧转换成灰度图像
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)                 
        
        #人脸检测，1.2和2分别为图片缩放比例和需要检测的有效点数
        faceRects = classfier.detectMultiScale(grey, scaleFactor = 1.2, minNeighbors = 3, minSize = (32, 32))
        if len(faceRects) > 0:            #大于0则检测到人脸                                   
            for faceRect in faceRects:  #单独框出每一张人脸
                x, y, w, h = faceRect        
                cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), color, 2)
                        
        #显示图像
        cv2.imshow(window_name, frame)
        # waitKey()方法本身表示等待键盘输入
        c = cv2.waitKey(1)
            
        if c & 0xFF == ord('q'):
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
CatchUsbVideo("frame", 0)