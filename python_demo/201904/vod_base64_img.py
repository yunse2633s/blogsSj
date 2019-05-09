# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 11:52:39 2019

@author: admin
作用：
    将视频每一帧转成base64图像格式
    转换一次需要的时间:28毫秒
"""

import cv2
import base64
from PIL import Image
from io import BytesIO
import time
print('0',time.time()*1000)
def frame2base64(frame):
    print('1',time.time()*1000 )
    img = Image.fromarray(frame) #将每一帧转为Image
    print('2',time.time()*1000 )
    output_buffer = BytesIO() #创建一个BytesIO
    print('3',time.time()*1000 )
    img.save(output_buffer, format='JPEG') #写入output_buffer
    print('4',time.time()*1000)
    byte_data = output_buffer.getvalue() #在内存中读取
    print('5',time.time()*1000 )
    base64_data = base64.b64encode(byte_data) #转为BASE64
    print(base64_data[0:20])
    return base64_data #转码成功 返回base64编码

print('6',time.time()*1000)
vc = cv2.VideoCapture('g:/work/vod/vid_suj.mp4') #读入视频文件
print('7',time.time()*1000)
rval=vc.isOpened()
print('8',time.time()*1000)

rval, frame = vc.read()
print('9',time.time()*1000)

#framebase64=frame2base64(frame)
def get_runtime(xx=False,yy=False):
    t1=time.time()*1000
    if xx:
        xx(yy)
    t2=time.time()*1000-t1
    print(t2)
    
framebase64=get_runtime(frame2base64,frame)
framebase64=get_runtime()