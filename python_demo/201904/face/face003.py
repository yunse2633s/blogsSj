# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 15:48:08 2019

@author: admin

作用：
    1. 测试图像清晰度
    2. putText 中文输出乱码
参照:
    https://blog.csdn.net/djstavaV/article/details/86884279

问题：
	图片尺寸不一样，清晰度判断不一致
	
    
"""

import cv2

# 读取原始图片
#img=cv2.imread('g:/work/vod/img/timg.jpg')
#img=cv2.imread('g:/work/vod/img/suoerwei.jpg')
#img=cv2.imread('g:/work/vod/img/IMG_20190322_174021.jpg')

#img=cv2.imread('g:/work/vod/img/thumb.png')
# 将原图色价调整为灰度
igray=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)

# Laplacian()
#ilap=cv2.Laplacian(igray,cv2.CV_16U)
ilap=cv2.Laplacian(igray,cv2.CV_16S)
# convertScaleAbs()函数功能是将CV_16S型的输出图像转变成CV_8U型的图像
dst=cv2.convertScaleAbs(ilap)
# convertScaleAbs()可实现图像增强等相关操作的快速运算
#dst=cv2.convertScaleAbs(img,1.5,3)

# mean()
#meanValue=cv2.mean(ilap)[0]
meanValue=ilap.var()
sharpness="sharpness::"+ str(meanValue)
cv2.putText(img,sharpness,(20,20),cv2.FONT_HERSHEY_PLAIN,1.0,(255,255,0),1,1)

# 显示图片
cv2.imshow('showImg', img)


# 等待键盘输入
cv2.waitKey()
# 销毁所有窗口
cv2.destroyAllWindows()