# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 11:42:49 2019

@author: admin
环境：
    python v3.7.1
    opencv v4.0
    tensorflow v1.13.1
    numpy v1.16.2
作用：
读取视频文件，并按帧数取图
"""

import cv2
vc = cv2.VideoCapture('g:/work/vod/vid_suj.mp4') #读入视频文件
c=0
rval=vc.isOpened()
timeF = 100  #视频帧计数间隔频率
while rval:   #循环读取视频帧
    c = c + 1
    rval, frame = vc.read()
    #print("c:%d,timef:%d"%(c,timeF))
    if(c%timeF == 0): #每隔timeF帧进行存储操作
        
        #cv2.imwrite('g:/work/vod/img/'+str(c) + '.jpg', frame) #存储为图像
        cv2.waitKey(10)
    #if rval:
	    #img为当前目录下新建的文件夹
        #cv2.imwrite('g:/work/vod/img/'+str(c) + '.jpg', frame) #存储为图像
        #cv2.waitKey(10)
    #else:
        #break
vc.release()