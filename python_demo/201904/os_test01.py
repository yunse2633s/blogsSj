# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 11:26:58 2019

@author: admin
环境：
    python v3.7.1
    opencv v4.0
    tensorflow v1.13.1
    numpy v1.16.2
作用：
文件系统的操作
1. 遍历文件夹下文件
2. 获取特定的文件名称
3. 创建文件、文件夹
4. 文件读取、写入、查询、修改

"""

import os
import json


dirpath='g:/work/vod'
dictValue={'name':'china'}
# 类对象的JSON序列化
print('类对象的序列化%s'%(json.dumps(dictValue)) )
# 字符串转 dict

# 1. os.walk() 文件夹遍历
def file_name(file_dir):
    
    pathFiles=os.walk(file_dir) #返回一个元组(dirpath,dirnames,filenames)
    
    file_list=[]
    
    for root,dirs,files in pathFiles:
        print('当前目录路径 %s'%(root))
        print('当前路径下所有子目录$s'%(dirs))
        print('当前路径下所有非目录子文件%s'%(files))
        for file in files:
            if os.path.splitext(file)[1] == '.mp4':
                file_list.append(os.path.join(root,file))
    return file_list

#lists=file_name(dirpath)
#print('目录下有:%s'%(lists))

# os.listdir()
listName=[]

def list_dir(path, list_name):  
    for file in os.listdir(path):  
        file_path = os.path.join(path, file)  
        print('里层%s'%(file_path))
        if os.path.isdir(file_path):
            print(1)
            list_dir(file_path, list_name)  
        elif os.path.splitext(file_path)[1]=='.jpg':  
            list_name.append(file_path)
            
list_dir(dirpath,listName)
print('listName:%s'%(listName))
