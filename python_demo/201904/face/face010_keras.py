# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 12:18:17 2019

@author: admin

作用：
    keras搭建网络模型
    keras 有Sequential 和Model两种搭建网络的方式，Sequential只能顺序搭建无分支结构，Model则可以搭建多分支结构
参照：
    https://blog.csdn.net/xingkongyidian/article/details/88018576
"""

from tensorflow.keras.layers import (Input,ConvLSTM2D,)

from tensorflow.keras.models import Model
from tensorflow.keras.models import Sequential


def Seq():
    '''
     input_shape 为(time_steps, map_height, map_width, channels)
     time_steps 就是将一个样例分为多少个时间点读入，x1,x2...,xt，的t
     return_sequences为True时每一个时间点都有输出
     return_sequences为False时，只有最后一个时间点有输出
    '''
    seq = Sequential()
    seq.add(ConvLSTM2D(filters=30, kernel_size=(3, 3),
                       input_shape=(15, 40, 40, 3),
                       padding='same', return_sequences=True, data_format='channels_last'))

    seq.add(ConvLSTM2D(filters=50, kernel_size=(3, 3),
                       padding='same', return_sequences=True, data_format='channels_last'))

    seq.add(ConvLSTM2D(filters=60, kernel_size=(3, 3),
                       padding='same', return_sequences=True, data_format='channels_last'))

    seq.add(ConvLSTM2D(filters=70, kernel_size=(3, 3),
                       padding='same', return_sequences=False, data_format='channels_last'))

    seq.summary()

def main():
    Inputs=[]
    Outputs=[]
    input = Input(shape=(15, 40, 40, 3))
    Inputs.append(input)
    convlstm1= ConvLSTM2D(filters=30, kernel_size=(3,3),
                          padding='same', return_sequences=True, data_format='channels_last')(input)
    convlstm2 = ConvLSTM2D(filters=50, kernel_size=(3, 3),
                           padding='same', return_sequences=True, data_format='channels_last')(convlstm1)
    convlstm3 = ConvLSTM2D(filters=60, kernel_size=(3, 3),
                           padding='same', return_sequences=True, data_format='channels_last')(convlstm2)
    convlstm4 = ConvLSTM2D(filters=70, kernel_size=(3, 3),
                           padding='same', return_sequences=False, data_format='channels_last')(convlstm3)
    Outputs.append(convlstm4)
    model =Model(inputs=input, outputs=convlstm4)
    model.summary()

if __name__ == '__main__':
    Seq()
    main()