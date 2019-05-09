# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 11:32:45 2019

@author: admin
环境：
    python v3.7.1
    tensorflow v1.13.1
    numpy v1.16.2
    matplotlib v3.0.2
摘自: https://www.cnblogs.com/tensorflownews/p/8671397.html
作用是：
"""
#引入tensorflow模块
# tensorflow程序一般分2个过程：图的构建、图的执行
# 节点(operation):每次运算的的结果以及原始的输入数据都可称为一个节点（operation ，缩写为op）
import tensorflow as tf

# 构建过程
## 定义2个 1*2的矩阵， m1, m2
m1=tf.constant([3,5])
m2=tf.constant([2,4])

## 创建m1, m2矩阵相加的节点(operation,op)
result=tf.add(m1,m2)

## 输出一个包含三个属性(Name、Shape和Type)的Tensor，但不输出矩阵相加的结果
print(result)

# 执行过程，在会话(session)中执行模型中定义好的运算。
## 启动默认图模型
sess=tf.Session()
## 调用run()方法，启动并运行图模型，执行矩阵加法
result2=sess.run(result)
## 打印矩阵相加的结果
print(result2)



# 执行过程中的多种选择
## 第一种：使用with...device语句来指定GPU或CPU资源执行操作
def withDevice():
    with tf.Session() as sess:
        #指定第二个GPU资源来运行下面的节点op
        with tf.device("/gpu:2"):
            m1=tf.constant([3,5])
            m2=tf.constant([2,4])
            result=tf.add(m1,m2)

## 第二种：调用函数as_default()生成默认会话
def asDefault(op):
    #
    def funOne():
        sess=tf.Session()
        with sess.as_default():
            print(op.eval())

    # 交互式环境常使用InteractiveSession()
    def funTwo():
        sess=tf.InteractiveSession()
        print(result.eval())


#tensor(张量)是tensorflow种重要的数据结构。
## 常量、变量、占位符
## tf.constant()
## 常量的初始化:tf.zeros、tf.ones、tf.fill、tf.linspace、tf.range等
## 生成一些随机的张量：tf.random_normal()、tf.truncated_normal()、tf.random_uniform()、tf.random_shuffle()等
## 变量的定义 Variable()
b=tf.Variable([1,3], name="vector")
c=tf.Variable([[0,1],[2,3]], name="matrix")
## 函数variable()为构造函数，构造函数的使用需要初始值,并且使用前必须初始化
## 未初始化的变量提示err"Attempting to use uninitialized value d"
## 变量的初始化
def initValue():
    # 初始化全部变量
    init=tf.global_variables_initializer()
    with tf.Session() as sess:
        sess.run(init)
    b=tf.Variable([1,3], name='vector')
    # 初始化变量的子集
    # init_subset=tf.variables_initializer([m1,m2],name="init_subset")
    # m1, m2是常量， 会提示err"'int' object has no attribute 'initializer'"
    init_subset=tf.variables_initializer([b,c],name="init_subset")
    with tf.Session() as sess:
        sess.run(init_subset)
    
    # 初始化单个变量
    init_var=tf.Variable(tf.zeros([2,5]))
    with tf.Session() as sess:
        sess.run(init_var.initializer)
        
## tensorflow变量的保存Save()
def saveValue():
    var1=tf.Variable([1,3], name="v1")
    var2=tf.Variable([2,4], name="v2")
    # 对全部变量进行初始化
    #init=tf.initialize_all_variables()
    init=tf.global_variables_initializer()
    # 调用 Savar()存储器
    saver=tf.train.Saver()
    # 执行图模型
    with tf.Session() as sess:
        sess.run(init)
        # 设置存储路径,它会在当前路径下创建test文件夹及文件
        save_path=saver.save(sess, "test/save.ckpt")

## 变量的获取 restore()
def restoreValue():
    var1=tf.Variable([0,0],name="v1")
    var2=tf.Variable([0,0],name="v2")
    saver=tf.train.Saver()
    # latest_checkpoint()获取到该目录下最近一次保存的模型。
    module_file=tf.train.latest_checkpoint('test/')
    with tf.Session() as sess:
        # 交互环境下可以运行，单独执行时提示错误
        saver.restore(sess,module_file)
        print('model restored')
        #print(var1)
        #print(sess.run(var1))
        
## placeholder() 数据初始化的容器，它与变量的区别是定义模板，用做占位，即占位符
def placeholderValue():
    # e,f的张量类型必须一致
    e=tf.placeholder(tf.float32, shape=[2],name=None)
    f=tf.constant([6,4], tf.float32)
    g=tf.add(e,f)
    with tf.Session() as sess:
        print(sess.run(g,feed_dict={e: [10,10]} ))

## fetch概念，在一个会话中同时运行多个op，取回多个tensor
print(sess.run([m1,m2]))
## 关闭会话
sess.close()