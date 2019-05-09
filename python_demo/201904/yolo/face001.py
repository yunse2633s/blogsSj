# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 12:04:00 2019

@author: admin
作用：
    基于YOLO框架检测实物
    
环境：
    python v3.7.1
    opencv v4.0
    tensorflow v1.13.1
    numpy v1.16.2
    
    
参照：
https://blog.csdn.net/haoqimao_hard/article/details/82081285

"""
import cv2
import numpy as np



## 初始化参数
confThreshold = 0.5  #Confidence threshold
nmsThreshold = 0.4   #Non-maximum suppression threshold
inpWidth = 416       #Width of network's input image
inpHeight = 416      #Height of network's input image


### Load names of classes
OPENCV_PATH=r"H:/swap/yolo3/"
classesFile = OPENCV_PATH + "coco.names";
classes = None
with open(classesFile, 'rt') as f:
    classes = f.read().rstrip('\n').split('\n')
 
# Give the configuration and weight files for the model and load the network using them.
modelConfiguration = OPENCV_PATH + "yolov3.cfg";
modelWeights = OPENCV_PATH + "yolov3.weights";
 
net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
#print(net)
####
# Get the names of the output layers

def getOutputsNames(net):
    # Get the names of all the layers in the network
    layersNames = net.getLayerNames()
    # Get the names of the output layers, i.e. the layers with unconnected outputs
    return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]

###
def postprocess(frame, outs):
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]
 
    classIds = []
    confidences = []
    boxes = []
    # Scan through all the bounding boxes output from the network and keep only the
    # ones with high confidence scores. Assign the box's class label as the class with the highest score.
    classIds = []
    confidences = []
    boxes = []
    for out in outs:
        
        for detection in out:
            
            scores = detection[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            
            if confidence > confThreshold:                
                center_x = int(detection[0] * frameWidth)
                center_y = int(detection[1] * frameHeight)
                width = int(detection[2] * frameWidth)
                height = int(detection[3] * frameHeight)
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                classIds.append(classId)
                confidences.append(float(confidence))
                boxes.append([left, top, width, height])
 
    # Perform non maximum suppression to eliminate redundant overlapping boxes with
    # lower confidences.
    indices = cv2.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)
    for i in indices:
        i = i[0]
        box = boxes[i]
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]
        drawPred(classIds[i], confidences[i], left, top, left + width, top + height)
        
        
#

####
def drawPred(classId, conf, left, top, right, bottom):
    # Draw a bounding box.
    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255))
    
    label = '%.2f' % conf
        
    # Get the label for the class name and its confidence
    if classes:
        assert(classId < len(classes))
        label = '%s:%s' % (classes[classId], label)
 
    #Display the label at the top of the bounding box
    labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    top = max(top, labelSize[1])
    cv2.putText(frame, label, (left, top), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))



####
#outputFile="G:/work/vod/videoTimg.mp4"
#cap = cv2.VideoCapture(outputFile)
#vodadd = "http://root:123456@192.168.1.103/axis-cgi/mjpg/video.cgi?resolution=1280x1024"
vodadd='F:\监控摄像头视频\MVI_1423.mp4'
cap = cv2.VideoCapture(cv2.CAP_DSHOW) #读取高振
cap.open(vodadd)

#inpWidth=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#inpHeight=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

print('==>', cap.isOpened())
#while cv2.waitKey(1) < 0:
while cap.isOpened(): 
    
    # get frame from the video
    hasFrame, frame = cap.read()
    print('a', hasFrame)
    # Stop the program if reached end of video
    if not hasFrame:
        print("Done processing !!!")
        print("Output file is stored as ", outputFile)
        cv2.waitKey(3000)
        break
 
    # Create a 4D blob from a frame.
    blob = cv2.dnn.blobFromImage(frame, 1/255, (inpWidth, inpHeight), [0,0,0], 1, crop=False)
    #blob = cv2.dnn.blobFromImage(frame, 1.0, ( 224, 224), ( 104, 117, 123), False, crop= False)

 
    # Sets the input to the network
    net.setInput(blob)
    print(getOutputsNames(net))
    # Runs the forward pass to get output of the output layers
    outs = net.forward(getOutputsNames(net))
 
    # Remove the bounding boxes with low confidence
    postprocess(frame, outs)
 
    # Put efficiency information. The function getPerfProfile returns the 
    # overall time for inference(t) and the timings for each of the layers(in layersTimes)
    t, _ = net.getPerfProfile()
    label = 'Inference time: %.2f ms' % (t * 1000.0 / cv2.getTickFrequency())
    cv2.putText(frame, label, (0, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
    print('a')
    # Write the frame with the detection boxes
    '''
        if (args.image):
            cv2.imwrite(outputFile, frame.astype(np.uint8));
        else:
            cap.write(frame.astype(np.uint8))
    '''
    #cap.write(frame.astype(np.uint8))
    
    cv2.imshow('abc', frame.astype(np.uint8))
    # waitKey()方法本身表示等待键盘输入
    c = cv2.waitKey(1)
        
    if c & 0xFF == ord('q'):
        break        
    
    #释放摄像头并销毁所有窗口
cap.release()
cv2.destroyAllWindows()     
