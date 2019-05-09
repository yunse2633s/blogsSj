# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 09:39:27 2019

@author: admin
环境：
    python v3.7.1
    opencv v4.0
    tensorflow v1.13.1
    numpy v1.16.2
作用：
    1.读取“网络视频”文件，并按帧数取图
    2.制作训练模型所需的正例子和反例子
    3.行人识别后，画图，并保存

"""

import cv2
import numpy as np
from imutils.object_detection import non_max_suppression


vodadd = "http://root:123456@192.168.1.103/axis-cgi/mjpg/video.cgi?resolution=1280x1024"

vc = cv2.VideoCapture(cv2.CAP_DSHOW) #读取高振
vc.open(vodadd)
c=0
rval=vc.isOpened()

## 调用 行人检测
# 定义HOG对象，采用默认参数，或者按照下面的格式自己设置
defaultHog=cv2.HOGDescriptor()
# 设置SVM分类器，用默认分类器
defaultHog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# 循环读帧

while rval:   #循环读取视频帧
    c = c + 1
    rval, frame = vc.read()
    
    if rval:
        #这里对整张图片进行裁剪
        # # detect people in the image
        (rects, weights) = defaultHog.detectMultiScale(frame, winStride=(4, 4),padding=(8, 8), scale=1.05)
        
        for (x, y, w, h) in rects:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            
        rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
        
        #pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

	    #img为当前目录下新建的文件夹
        #cv2.imwrite('g:/work/vod/img/'+str(c) + '.jpg', frame) #存储为图像
        cv2.imshow('hog', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
    
vc.release()