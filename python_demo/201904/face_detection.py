# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 15:02:12 2019

@author: admin
环境：
    python v3.7.1
    opencv v4.0
    tensorflow v1.13.1
    numpy v1.16.2

作用：人脸识别
参考：
https://blog.csdn.net/qq_42633819/article/details/81191308
https://www.cnblogs.com/21207-iHome/articles/6253796.html
"""


import cv2
import sys
from PIL import Image
 
def CatchCamera(window_name, camera_idx):
    cv2.namedWindow(window_name)
    
    #视频来源，可以来自一段已存好的视频，也可以直接来自USB摄像头
    cap = cv2.VideoCapture(camera_idx)                
    
    #告诉OpenCV使用人脸识别分类器
    OPENCV_PATH = r"d:/Program Files (x86)/python/Lib/site-packages/cv2/data" 
    # haarcascade_frontalface_alt2 haarcascade_frontalface_alt haarcascade_frontalface_default
    classfier = cv2.CascadeClassifier(OPENCV_PATH + "/haarcascade_frontalface_default.xml")
    #classfier = cv2.CascadeClassifier("H:\\OpenCV\\opencv\\build\\etc\\haarcascades\\haarcascade_frontalface_alt2.xml")
    
    #识别出人脸后要画的边框的颜色，RGB格式
    color = (0, 255, 0)
    frame_num=1    
    while cap.isOpened():
        ok, frame = cap.read() #读取一帧数据
        if not ok:            
            break  
 
        #将当前帧转换成灰度图像
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)                 
        
        #人脸检测，1.2和2分别为图片缩放比例和需要检测的有效点数
        faceRects = classfier.detectMultiScale(grey, scaleFactor = 1.5, minNeighbors = 3)
        if len(faceRects) > 0:            #大于0则检测到人脸  
            # 打印第一帧原图
            if frame_num < 1:
                #保存图片
                cv2.imwrite('g:/work/vod/axis/right/oneframe0.jpg', frame) 
            for faceRect in faceRects:  #单独框出每一张人脸
                x, y, w, h = faceRect        
                cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), color, 2)
            # 保存识别到人脸的第一帧
            if frame_num < 1:
                print(frame_num)
                #保存图片
                cv2.imwrite('g:/work/vod/axis/right/oneframe1.jpg', frame)                                 
                frame_num +=1
                        
        #显示图像
        cv2.imshow(window_name, frame)    
        
        c = cv2.waitKey(1)
        if c & 0xFF == ord('q'):
            break        
    
    #释放摄像头并销毁所有窗口
    cap.release()
    cv2.destroyAllWindows() 
    
if __name__ == '__main__':
    if len(sys.argv) != 1:
        print("Usage:%s camera_id\r\n" % (sys.argv[0]))
    else:
        #CatchCamera("识别人脸区域", 0)
        vod='F:\监控摄像头视频\MVI_1423.mp4'
        CatchCamera("face", vod)