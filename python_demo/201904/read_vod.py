# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 16:01:22 2019

@author: admin
环境：
    python v3.7.1
    opencv v4.0
    tensorflow v1.13.1
    numpy v1.16.2
    
参照:  
https://www.cnblogs.com/21207-iHome/articles/6253796.html
https://blog.csdn.net/fengbingchun/article/details/52554711
"""

import cv2
import numpy as np
 

##  执行后，窗口卡死
def err001():
    ## 打开后卡死
    cap = cv2.VideoCapture("g:/work/vod/vid_suj.mp4")
    # 获取视频帧数
    rate=cap.get(cv2.CAP_PROP_FPS)
    # 每一帧之前的延迟与视频的帧率相对应
    delay = int(1000 / rate)
    ok, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow("vod", gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows() 
        
## 执行后，视频倒置
def err002():
    cap = cv2.VideoCapture("g:/work/vod/vid_suj.mp4")
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow('frame', gray)
            # & 0xFF is required for a 64-bit system
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()
'''
使用 
resizeWindow():调整窗口大小,
transpose():可实现图片方向和镜像图片的同时变换,
flip():翻转,
将视频竖屏
实际是将图片由横屏转为竖屏，然后显示


'''

def right001():
    cap = cv2.VideoCapture("g:/work/vod/vid_suj.mp4")
    #获取视频的宽、高、帧数、时长
    vod_width=cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    vod_height=cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    vod_rate=cap.get(cv2.CAP_PROP_FPS)
    # 获取总帧数
    vod_rate_count=cap.get(cv2.CAP_PROP_FRAME_COUNT)
    vod_time=int(vod_rate_count/vod_rate) # 获取秒数
    # 调整窗口尺寸
    cv2.namedWindow('frame', 0)
    x = int(vod_width / 2)
    y = int(vod_height / 2) 
    cv2.resizeWindow("frame", y,x)
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            frame=cv2.transpose(frame)
            frame=cv2.flip(frame,-1)
            #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #cv2.resizeWindow(frame,int(2,5))
            cv2.imshow('frame', frame)
            # & 0xFF is required for a 64-bit system
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()
    
right001()