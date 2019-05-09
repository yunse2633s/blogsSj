# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 10:54:45 2019

@author: admin
作用：
    将视频流转为base64，提供给百度接口获取返回数据，
参照:
    https://blog.csdn.net/zhangpan929/article/details/85410690
    
"""


'''
人流量统计（动态版）+cv2
'''

#import urllib, urllib2, sys
import urllib, sys
import ssl
import base64
import cv2

baidu_ak='GCwD2qaPLAG8LDBL4MjRXIN1'
baidu_sk='g1o7HipnLfknU1YVmPtGyVYWWoXDwH0O'
token_url='https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=GCwD2qaPLAG8LDBL4MjRXIN1&client_secret=g1o7HipnLfknU1YVmPtGyVYWWoXDwH0O'



def get_baidutoken(ak,sk):
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    token_url = r'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='+ak+'&client_secret='+sk
    
    request = urllib2.Request(host)
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    response = urllib2.urlopen(request)
    content = response.read()
    if (content):
        print(content)
        
def get_baidutoken3(ak,sk):
    
    context = ssl._create_unverified_context()
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    token_url = r'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='+ak+'&client_secret='+sk
    print(token_url)
    headers={'Content-Type': 'application/json; charset=UTF-8'}
    
    req = urllib.request.Request(token_url, headers=headers)
    
    try:
        page = urllib.request.urlopen(req).read()
        page = page.decode('utf-8')
        #print(type(page))
        #print(eval(page)["access_token"])
        return eval(page)["access_token"]
    except OSError as e:
        print("OS error: {0}".format(e))
        #print(e.read().decode('utf-8'))

  
    
def get_baidutrack(frame, token):
    # 把视频帧 转为 base64图片
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/body_tracking"
    
    # 二进制方式打开图片文件
    f = open(frame, 'rb')
    img = base64.b64encode(f.read())
    params = {"area":"1,1,500,1,500,500,1,500","case_id":1,"case_init":"false","dynamic":"false","image":img}
    #params = urllib.urlencode(params)
    data = urllib.parse.urlencode(params).encode('ascii')
    
    access_token = token
    request_url = request_url + "?access_token=" + token
    headers={'Content-Type': 'application/x-www-form-urlencoded'}
    req = urllib.request.Request(url=request_url, data=data, headers=headers)
    
    page = urllib.request.urlopen(req).read()
    page=page.decode('utf-8') #若没有此行，结果时class类型
    if page:
        print(type(page))
        print(page)

# 将视频帧转base64
def get_base64(frame):
    base64img=frame
    return base64img

baidutoken = get_baidutoken3(baidu_ak, baidu_sk)
image=r"g:/work/vod/img/baidu004.jpg"
get_baidutrack(image, baidutoken)

# 使用opencv 获取每一帧，并获取百度返回结果，计算响应时间
# 视频流帧数，尺寸，抽帧次数