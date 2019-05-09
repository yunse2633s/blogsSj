# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 17:12:20 2019

@author: admin

作用：
    图片格式
    二进制
    base64
    np序列
    opencv格式
    PIL.Image格式
"""

import base64
import numpy as np
import cv2
import io
from PIL import Image


img_file = open(r'G:\work\vod\img\baidu004.JPG','rb')   # 二进制打开图片文件
print('img_file', img_file)
img_b64encode = base64.b64encode(img_file.read())  # base64编码
print('base64编码', img_b64encode)
img_file.close()  # 文件关闭
img_b64decode = base64.b64decode(img_b64encode)  # base64解码

img_array = np.fromstring(img_b64decode,np.uint8) # 转换np序列
print('np序列', img_array)
img=cv2.imdecode(img_array,cv2.COLOR_BGR2RGB)  # 转换Opencv格式
print('Opencv格式', img)

#cv2.imshow("img",img)
#cv2.waitKey()

image = io.BytesIO(img_b64decode)
print('PIL.Image格式', image)
#img = Image.open(image)
#img.show()