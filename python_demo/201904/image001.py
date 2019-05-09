# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 13:52:57 2019

@author: admin

环境：
    python v3.7.1
    opencv v4.0
    tensorflow v1.13.1
    numpy v1.16.2

作用：
图片 读、写、显操作
参考：https://blog.csdn.net/jqw11/article/details/73826014
1. 图片读取
2. 图片显示
3. 在图片中写文字
4. 缩放图片
5. 图片平移
6. 图片旋转
7. 仿射变换
8. 图像颜色变换
9. 通道拆分/合并
10. 图片添加边距
11. 图片90度旋转
"""

    # 0:摄像头ID, 打开摄像头


import cv2
import numpy as np

image=cv2.imread('g:/work/vod/img/400.jpg', cv2.CAP_PROP_FPS) # LoadImage--imread

## 获取图片属性
print(image.shape)
print(image.size)
#print(image.dtype)
#print(image.shape[0])  高度
#print(image.shape[1]) 宽度

# 设置窗体大小, cv2.WINDOW_AUTOSIZE| cv2.WINDOW_KEEPRATIO| cv2.GUI_EXPANDED
cv2.namedWindow('a_window', 0) # Facultative NamedWindow--namedWindow

## 将一段文字显示在图片中
#font=cv2.circle(cv2.FONT_HERSHEY_SIMPLEX, 1, 1, 0, 3, 8)

#y = image.height / 2 # y position of the text
y = int(image.shape[0] / 2) 
#x = image.width / 4 # x position of the text
x = int(image.shape[1] / 2)
# 调整窗体尺寸
cv2.resizeWindow("a_window", y,x)
# 图片中写文字
# putText(img, text, org, fontFace, fontScale, color)
# param: org中的坐标值必须是整数
def writeTextImg():    
    cv2.putText(image,"Hello World !", (x,y), cv2.FONT_HERSHEY_PLAIN,5, (255, 255, 0))
    cv2.imshow('a_window', image) #Show the image  ShowImage--imshow
    # 写图片
    cv2.imwrite("g:/work/vod/img/thumb.png", image)   # SaveImage-->imwrite



# 改变图片大小, 缩放
def zoomImg():    
    res=cv2.resize(image, (x,y), interpolation=cv2.INTER_CUBIC)
    cv2.imwrite("g:/work/vod/img/resize.png", res)


# 图像平移
def levelMoveImg():
    M=np.float32([[1,0,100],[0,1,50]])
    translational=cv2.warpAffine(image, M, (x,y))
    cv2.imwrite('g:/work/vod/img/translational.png', translational)

# 图像旋转
## getRotationMatrix2D() 获取旋转矩阵
## warpAffine() 实现坐标系仿射变换
def revolveImg():
    #M=cv2.getRotationMatrix2D((x,y), 90, 1)
    #dst=cv2.warpAffine(image, M, (image.shape[1],image.shape[0]))
    
    M=cv2.getRotationMatrix2D((x,y), 180, 1)
    dst=cv2.warpAffine(image, M, (x,y))
    cv2.imshow('a_window', dst)


# 仿射变换
def affineImg():
    pts1=np.float32([ [50,50], [200,50], [50,200] ])
    pts2=np.float32([ [10,100],[200,50], [100,250] ])
    M=cv2.getAffineTransform(pts1, pts2)
    dst=cv2.warpAffine(image, M, (x, y))
    cv2.imshow('a_window', dst)

# 颜色变换
def colorChangeImg():
    #res2=cv2.CreateImage(cv2.getSize(image), cv2.CV_8UC2,3) #v4.0版已经没有CreateImage()
    # 颜色通道 拆分与合并
    b,g,r=cv2.split(image) # 颜色通道分离,
    img2=cv2.merge([r,g,b]) #
    
    cv2.imshow('a_window', img2)
    # 颜色空间转换
    #cv2.imshow('a_window2', image[:,:,::-1]) # BGR转换为RGB的操作
    cv2.imshow('a_window3', cv2.cvtColor(image, cv2.COLOR_RGB2YUV))    
    
# 图片添加边距
def frameImg():
    #replicate=cv2.copyMakeBorder(image, 10,10,10,10, cv2.BORDER_REPLICATE)
    #reflect = cv2.copyMakeBorder(image,10,10,10,10,cv2.BORDER_REFLECT)
    #reflect101 = cv2.copyMakeBorder(image,10,10,10,10,cv2.BORDER_REFLECT_101)
    #wrap = cv2.copyMakeBorder(image,10,10,10,10,cv2.BORDER_WRAP)
    constant= cv2.copyMakeBorder(image,10,10,10,10,cv2.BORDER_CONSTANT,value=(255,255,0))
    cv2.imshow('a_window', constant)
    
# transpose() 可实现图片方向和镜像图片的同时变换
def transposeImg():
    # 将横屏的图像转为竖屏 必须放在全局
    #cv2.namedWindow('a_window2', 0) # 为0时，用户可以调整窗口尺寸
    # resizeWindow() 调整窗口尺寸  必须放在全局
    #cv2.resizeWindow("a_window2", image.shape[0],image.shape[1])
    #image=cv2.transpose(image)   # 必须放在全局 
    #image=cv2.flip(image,-1) # 必须放在全局
    cv2.imshow('a_window', image)
    

cv2.imshow('a_window', image)
cv2.waitKey() #Wait for user input and quit WaitKey-->waitKey

#cv2.destroyAllWindows()
