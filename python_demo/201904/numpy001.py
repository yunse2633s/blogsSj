# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 16:26:11 2019

@author: admin

环境：
    python v3.7.1
    opencv v4.0
    tensorflow v1.13.1
    numpy v1.16.2
作用：
numpy 操作
"""


import numpy as np
# arange
a=np.arange(18)

# reshape() 调整矩阵的行数、列数、维数
b=a.reshape(2,3,3)
c=a[::-1] #上下颠倒
d=a[:,::-1] # 左右颠倒
e=a[:,:,::-1] #矩阵翻转

#