# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 14:25:01 2019

@author: admin
环境：
    python v3.7.1
    opencv v4.0
    tensorflow v1.13.1
    numpy v1.16.2
作用：   
图片转视频
"""

import cv2
import glob
 
fps = 20   #保存视频的FPS，可以适当调整
 
#可以用(*'DVIX')或(*'X264'),如果都不行先装ffmepg: sudo apt-get install ffmepg
# python中 '*'的用法是序列化后面的字符串，当作位置参数传进去。 如(*'abc') == ('a','b','c')
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
#saveVideo.avi是要生成的视频名称，（384,288）是图片尺寸
videoWriter = cv2.VideoWriter('saveVideo111.avi',fourcc，（384,288））#括号可能是中文的，改一下，384,288需要改成你的图片尺寸，不然会报错
#imge存放图片
imgs=glob.glob('imge/*.jpg')
for imgname in imgs:
    frame = cv2.imread(imgname)
    videoWriter.write(frame)
videoWriter.release()