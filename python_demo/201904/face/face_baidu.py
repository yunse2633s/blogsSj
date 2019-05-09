# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 09:47:09 2019

@author: admin
"""

'''
人流量统计（动态版）
'''

#import urllib, urllib2, sys
import urllib, sys
import ssl
import base64
import time


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
    #context = ssl._create_unverified_context()
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

  
    
def get_baidutrack(frame, token, dynamic):
    
    t3=time.time()*1000    
    # 把视频帧 转为 base64图片
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/body_tracking"
    
    # 二进制方式打开图片文件
    f = open(frame, 'rb')
    img = base64.b64encode(f.read())
    params = {"area":"1,1,500,1,500,500,1,500","case_id":1,"case_init":"false","dynamic": dynamic,"image":img}
    #params = urllib.urlencode(params)
    data = urllib.parse.urlencode(params).encode('ascii')
    
    request_url = request_url + "?access_token=" + token
    headers={'Content-Type': 'application/x-www-form-urlencoded'}
    req = urllib.request.Request(url=request_url, data=data, headers=headers)
    
    page = urllib.request.urlopen(req).read()
    page=page.decode('utf-8') #若没有此行，结果时class类型
    print('body_tracking响应时间:', time.time()*1000-t3)
    if page:
        print(type(page))
        print(page)

# 将视频帧转base64
def get_base64(frame):
    base64img=frame
    return base64img

baidutoken = get_baidutoken3(baidu_ak, baidu_sk)
image=r"g:/work/vod/img/baidu004.jpg"


t1=time.time()*1000
print('0',time.time()*1000)
get_baidutrack(image, baidutoken, False) # True & False 响应时间>791毫秒
#get_baidutoken3(baidu_ak, baidu_sk) # 响应时间>282毫秒
t2=time.time()*1000-t1
print(t2) #791毫秒



