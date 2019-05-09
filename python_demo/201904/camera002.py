# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 15:46:44 2019
环境：
    python v3.7.1
    opencv v4.0
    tensorflow v1.13.1
    numpy v1.16.2
参考：
    https://www.jianshu.com/p/182d83926b45
存储视频流
"""

import numpy as np
import cv2

def video_capture(filePath):
    # 打开摄像头
    cap = cv2.VideoCapture(0)
    #
    fps = cap.get(cv2.CAP_PROP_FPS)
    #获取窗口尺寸
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    #fourcc = cv2.cv.FOURCC(*'CVID')  # v2.0版
    fourcc = cv2.VideoWriter_fourcc(*'MPG4') #v4.0版 或 VideoWriter_fourcc('M','P','G','4')
    
    print("fps: %s, size:%s, fourcc: %s "%(fps,size, fourcc) )
    # 存储视频流
    out = cv2.VideoWriter(filePath, fourcc, fps, size)

    while (cap.isOpened()):
        ret, frame = cap.read()

        if ret == True:
            # 旋转视频 flip(旋转的视频 ，旋转的方向)
            frame = cv2.flip(frame, 0)
            # 将捕获的视频流转换为灰色保存
            gray = cv2.cvtColor(frame,  cv2.COLOR_BGR2GRAY)
            # 播放视频
            cv2.imshow('iframe', gray)
            
            out.write(gray)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    # 释放对象销毁窗口
    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    #filePath = 'g:\work\vod\output.avi'  #\v被转义
    filePath = 'g:/work/vod/output.mp4'
    video_capture(filePath)