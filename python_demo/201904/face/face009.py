# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 11:10:37 2019

@author: admin


环境：
    python v3.7.1
    opencv v4.0
    tensorflow v1.13.1
    numpy v1.16.2

作用：人脸识别、并存储人脸
参考：
https://blog.csdn.net/qq_42633819/article/details/81191308
https://www.cnblogs.com/21207-iHome/articles/6253796.html
"""


import cv2
import sys
from PIL import Image


 
def CatchCamera(window_name, camera_idx, catch_pic_num, path_name):
    cv2.namedWindow(window_name)
    
    #视频来源，可以来自一段已存好的视频，也可以直接来自USB摄像头
    cap = cv2.VideoCapture(camera_idx)                
    
    # 获取视频总帧数
    frameCount=cap.get(cv2.CAP_PROP_FRAME_COUNT)  # 1987
    #告诉OpenCV使用人脸识别分类器
    OPENCV_PATH = r"d:/Program Files (x86)/python/Lib/site-packages/cv2/data" 
    classfier = cv2.CascadeClassifier(OPENCV_PATH + "/haarcascade_frontalface_default.xml")
    
    eye_cascade=cv2.CascadeClassifier(OPENCV_PATH+"/haarcascade_eye.xml")
    #识别出人脸后要画的边框的颜色，RGB格式
    color = (0, 255, 0)
    
    num=0
    frame_count=0
    while cap.isOpened():
        ok, frame = cap.read() #读取一帧数据
        # 帧数计算
        frame_count += 1
        
        if not ok:            
            break  
        if(frame_count > 700):
            #将当前帧转换成灰度图像
            grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)                 
            
            #人脸检测，1.2和2分别为图片缩放比例和需要检测的有效点数
            faceRects = classfier.detectMultiScale(grey, scaleFactor = 1.3, minNeighbors = 5, minSize = (5, 5))
            if len(faceRects) > 0:            #大于0则检测到人脸                                   
                print('num:',num)
                for faceRect in faceRects:  #单独框出每一张人脸
                    # 人脸左上角位置的xy坐标，w,h为人脸的宽高
                    x, y, w, h = faceRect
                    # 判断是否有2个人眼
                    #roi_gray = grey[y:y+h, x:x+w] # 每个头像高、宽
                    #eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.2,minNeighbors=3)
                    #r=len(eyes) #人眼的数量
                    # 绘制眼睛
                    #if r>=1:
                        ## 保存当前帧的人脸图片
                    img_name='%s/%d.jpg'%(path_name,num)
                    # y减少10像素，就是y轴坐标向上移动10像素，用于扩大面积
                    image=frame[y-10:y+h+10, x-10: x+w+10]
                    #for (x0,y0,w0,h0) in eyes:
                        #print("eye:",x0,y0,w0,h0)
                        #cv2.rectangle(image,(x0,y0),(x0+w0,y0+h0),(255,255,0),2)
                    #保存图片
                    cv2.imwrite(img_name, image)
                    num +=1
                    # 设置图片存储量限制
                    if num > (catch_pic_num):
                        break
                    # 绘制人脸矩形框 ，左上角和右小角的坐标
                    cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), color, 2)
                    # 显示捕捉到多少张人脸
                    font=cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(frame,'num:%d' % (num),(x + 30, y + 30), font, 1, (255,0,255),4)
         
        # 若图片提取超限值，则退出
        if num > (catch_pic_num): break
                        
        #显示图像
        cv2.imshow(window_name, frame)        
        c = cv2.waitKey(10)
        if c & 0xFF == ord('q'):
            break        
    
    #释放摄像头并销毁所有窗口
    cap.release()
    cv2.destroyAllWindows() 

def faceRecogniction(frame, classfier, eye_cascade, path_name,catch_pic_num,color,num):
    # 参数不能保留吗
    return False     

if __name__ == '__main__':
    if len(sys.argv) != 1:
        print("Usage:%s camera_id\r\n" % (sys.argv[0]))
    else:
        vod='F:\监控摄像头视频\MVI_1423.mp4'
        savePaht='G:/work/vod/axis/right'
        CatchCamera("face", vod, 1000,savePaht)