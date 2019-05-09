# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 15:23:20 2019

@author: admin
环境：
    python v3.7.1
    opencv v4.0
    tensorflow v1.13.1
    numpy v1.16.2
参考：
https://www.cnblogs.com/21207-iHome/articles/6253796.html
作用：
使用 Haar 分类器进行面部检查
"""

import cv2

OPENCV_PATH = r"d:/Program Files (x86)/python/Lib/site-packages/cv2/data" 
# haarcascade_frontalface_alt2, haarcascade_frontalface_default
#face_cascade = cv2.CascadeClassifier(OPENCV_PATH + '/haarcascade_frontalface_default.xml')
face_cascade = cv2.CascadeClassifier(OPENCV_PATH + '/haarcascade_frontalface_alt.xml')
#face_cascade = cv2.CascadeClassifier(OPENCV_PATH + '/haarcascade_eye.xml')

#img = cv2.imread('g:/work/vod/img/suoerwei.jpg')
img = cv2.imread('g:/work/vod/img/MVI_1423.mp4_20190426_121206.378.jpg')
#img = cv2.imread('g:/work/vod/img/timg.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#
"""
 fun.detectMultiScale(image,scaleFactor,minNeighbors,flags,minSize,maxSize)
 param={
    image表示的是要检测的输入图像
    scaleFactor:表示每次图像尺寸减小的比例
    minNeighbors:表示每一个目标至少要被检测到3次才算是真的目标
    minSize为目标的最小尺寸
    minSize为目标的最大尺寸
 }
 return={
         objects:表示检测到的人脸目标序列
 }
 A: fun.detectMultiScale(gray,1.1,3) 高于 (gray, 1.5, 3)
 haarcascade_frontalface_alt2.xml 高于 haarcascade_frontalface_default
"""
faces = face_cascade.detectMultiScale(gray,1.01, 4,maxSize = (40, 40),minSize = (38,38))
# timg.jpg, alt2, (gray,1.01, 5) 多一人
# timg.jpg,alt2, (gray,1.01, [2,5],maxSize = (50, 50)) 符合
# suoerwei.jpg alt, (gray,1.19,3) || (gray,1.01, 4,maxSize = (40, 40),minSize = (38,38)) 符合
for (x,y,w,h) in faces:
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
