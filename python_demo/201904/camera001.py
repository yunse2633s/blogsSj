# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 13:52:08 2019

@author: admin
打开摄像头，获取时时图像
环境：
    python v3.7.1
    opencv v4.0
    tensorflow v1.13.1
    numpy v1.16.2
"""

import cv2
import sys
from PIL import Image

def CatchUsbVideo(window_name, camera_idx):
    cv2.namedWindow(window_name)
    
    #视频来源，可以来自一段已存好的视频，也可以直接来自USB摄像头
    cap = cv2.VideoCapture(camera_idx)        
        
    while cap.isOpened():
        ok, frame = cap.read() #读取一帧数据
        if not ok:            
            break                    
                        
        #显示图像并等待10毫秒按键输入，输入‘q’退出程序
        cv2.imshow(window_name, frame)
        c = cv2.waitKey(10)
        if c & 0xFF == ord('q'):
            break        
    
    #释放摄像头并销毁所有窗口
    cap.release()
    cv2.destroyAllWindows() 
    
if __name__ == '__main__':
    if len(sys.argv) != 2:
        # print("Usage:%s camera_id\r\n" % (sys.argv[0]))
        CatchUsbVideo("截取视频流", 0) # 第二个参数0 代表摄像头设备的id
    else:
        # CatchUsbVideo("截取视频流", int(sys.argv[1]))
        CatchUsbVideo("截取视频流", 0)