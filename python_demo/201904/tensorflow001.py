# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 14:17:45 2019

@author: admin
环境：
    python v3.7.1
    tensorflow v1.13.1
    numpy v1.16.2
    matplotlib v3.0.2
作用：
1554947497124: 出随机图样
"""

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

# create data
x_data=np.random.rand(100).astype(np.float32)
y_data=x_data*0.1+0.3
# 打印样本
fig=plt.figure()
plt.xlabel('X')
plt.ylabel('Y')
plt.scatter(x_data,y_data,c='r',marker='x')
# 设置图标
plt.legend('X')
plt.show()
# tensorflow structure start
Weights=tf.Variable(tf.random_uniform([1], -1.0, 1.0))
biases=tf.Variable(tf.zeros([1]))
y=Weights*x_data+biases
loss=tf.reduce_mean(tf.square(y-y_data))
optimizer=tf.train.GradientDescentOptimizer(0.5)
train=optimizer.minimize(loss)
init=tf.initialize_all_variables()
# tensorflow structure end
sess=tf.Session()
sess.run(init)

cost=[]
for step in range(201):
    sess.run(train)
    if step % 20 == 0:
        print("cost after iteration {}:{}".format(step, np.squeeze(sess.run(loss))))
        cost.append(sess.run(loss))

# 训练出的模型
fig=plt.figure()
plt.xlabel('Xmodel')
plt.ylabel('Ymodel')
plt.scatter(x_data, sess.run(y), c='y', marker='o')
plt.legend('xmodel')
plt.show()
plt.plot(np.squeeze(cost))
plt.ylabel('cost')
plt.xlabel('Learing rate=' +str(0.5))
plt.show()