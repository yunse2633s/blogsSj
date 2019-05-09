# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 15:08:04 2019

@author: admin
作用：
    yolo训练模型 中的步骤
    
"""

import os
from os import listdir, getcwd
from os.path import join
if __name__ == '__main__':
    source_folder='H:/swap/darknet/scripts/VOCdevkit/VOC2019/JPEGImages/'
    dest='H:/swap/darknet/scripts/VOCdevkit/VOC2019/ImageSets/Main/train.txt' 
    dest2='H:/swap/darknet/scripts/VOCdevkit/VOC2019/ImageSets/Main/val.txt'  
    file_list=os.listdir(source_folder)       
    train_file=open(dest,'a')                 
    val_file=open(dest2,'a')                  
    for file_obj in file_list:                
        file_path=os.path.join(source_folder,file_obj) 
       
        file_name,file_extend=os.path.splitext(file_obj)
       
        file_num=int(file_name) 
        
        if(file_num<776):                     
            
            train_file.write(file_name+'\n')  
        else :
            val_file.write(file_name+'\n')    
    train_file.close()