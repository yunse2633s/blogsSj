# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 10:57:16 2019

@author: admin

环境：
    python v3.7.1
    opencv v4.0
    tensorflow v1.13.1
    numpy v1.16.2
    
作用
  热度图
参考
https://www.cnblogs.com/arkenstone/p/6932632.html

需要确定人头位置和人头中心点
代码完成度：0%

"""
import cv2
import numpy as np
import matplotlib.pyplot as plt
from colour import Color


image= cv2.imread('g:/work/vod/img/baidu004.jpg')

box_centers=[]
radias=100

density_range = 100
gradient = np.linspace(0, 1, density_range)
img_width = image.shape[1]
img_height = image.shape[0]
density_map = np.zeros((img_height, img_width))
color_map = np.empty([img_height, img_width, 3], dtype=int)
# get gradient color using rainbow
cmap = plt.get_cmap("rainbow") # 使用matplotlib获取颜色梯度
blue = Color("blue") # 使用Color来生成颜色梯度
hex_colors = list(blue.range_to(Color("red"), density_range))
rgb_colors = [[rgb * 255 for rgb in color.rgb] for color in hex_colors][::-1]
for i in range(img_height):
    for j in range(img_width):
        for box in box_centers:
            dist = distance.euclidean(box, (j, i))
            if dist <= radias * 0.25:
                density_map[i][j] += 10
            elif dist <= radias:
                density_map[i][j] += (radias - dist) / (radias * 0.75) * 10
        ratio = min(density_range-1, int(density_map[i][j]))
        for k in range(3):
            # color_map[i][j][k] = int(cmap(gradient[ratio])[:3][k]*255)
            color_map[i][j][k] = rgb_colors[ratio][k]