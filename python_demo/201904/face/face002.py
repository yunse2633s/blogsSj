# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 14:02:25 2019

@author: admin
环境：
    python v3.7.1
    opencv v4.0
    tensorflow v1.13.1
    numpy v1.16.2
作用：
    人脸、人眼数量
    人头数量不行;

完成度90%    
"""

import cv2
import numpy as np

OPENCV_PATH = r"d:/Program Files (x86)/python/Lib/site-packages/cv2/data" 

#face_cascade=cv2.CascadeClassifier(OPENCV_PATH+"/haarcascade_frontalface_default.xml")
eye_cascade=cv2.CascadeClassifier(OPENCV_PATH+"/haarcascade_eye.xml")
face_cascade=cv2.CascadeClassifier(OPENCV_PATH+"/haarcascade_upperbody.xml")
#i = cv2.imread('g:/work/vod/img/timg.jpg')
#i = cv2.imread('g:/work/vod/img/IMG_20190322_174021.jpg')
i = cv2.imread('g:/work/vod/img/baidu004.jpg')
#print(i.shape)

gray=cv2.cvtColor(i,cv2.COLOR_BGR2GRAY)

faces=face_cascade.detectMultiScale(gray,1.05,3)
print("faces%d"%(len(faces)))
l=len(faces) # 人脸的数量

for (x,y,w,h) in faces:
    print("faces:",x,y,w,h)
    cv2.rectangle(i,(x,y),(x+w,y+h),(255,0,0),2)
    cv2.putText(i,'face',(int(w/2+x),int(y-h/5)),cv2.FONT_HERSHEY_PLAIN,1.0,(255,255,255),1,1)
    roi_gray = gray[y:y+h, x:x+w] # 每个头像高、宽
    roi_color = i[y:y+h, x:x+w]
    # 显示某个头像
    #cv2.imshow("img",roi_gray)
    #break
    
    # 人眼和人脸都都需要调整匹配detectMultiScale()中的参数
    #eyes = eye_cascade.detectMultiScale(roi_gray)
    eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.9,minNeighbors=3)
    
    cv2.putText(i,"face count",(20,20),cv2.FONT_HERSHEY_PLAIN,2.0,(255,255,255),2,1)
    cv2.putText(i,str(l),(230,20),cv2.FONT_HERSHEY_PLAIN,2.0,(255,255,255),2,1)	
    cv2.putText(i,"eyes count",(20,60),cv2.FONT_HERSHEY_PLAIN,2.0,(255,255,255),2,1)
    #print(i.shape)	
    r=len(eyes) #人眼的数量
    # 绘制眼睛
    for (x0,y0,w0,h0) in eyes:
        print("eye:",x0,y0,w0,h0)
        cv2.rectangle(i,(x+x0,y+y0),(x+x0+w0,y+y0+h0),(255,255,0),2)
    
    cv2.putText(i,str(r),(230,60),cv2.FONT_HERSHEY_PLAIN,2.0,(255,255,255),2,1)
    #cv2.imshow("img", roi_gray)
    
cv2.imshow("img",i)
cv2.waitKey(0)