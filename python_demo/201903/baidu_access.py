#coding:utf-8 
import urllib, urllib2, sys
import ssl


## 获取token
# client_id 为官网获取的AK， client_secret 为官网获取的SK
client_id='Q4Oq6F8laoOrcrG3odS0v65c'
client_secret='cgRl4lFG6BOAyvPEOMFAqLgOV27fBObj'
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='+client_id+'&client_secret='+client_secret
request = urllib2.Request(host)
request.add_header('Content-Type', 'application/json; charset=UTF-8')
response = urllib2.urlopen(request)
content = response.read()
if (content):
	# access_token=content['refresh_token']
	# 
    #print(isinstance(content, str))
    #print(type(content))
    access_token=(eval(content))['refresh_token']  # eval字符串 转字典
    print(access_token)

## 获取图片识别信息
host = 'https://aip.baidubce.com/rest/2.0/face/v3/detect'
image=''
image_type='URL'
face_field=''
max_face_num=10
face_type='LIVE'

'''
20190326

{"refresh_token":"25.67975d562bedd515318a46156f4d9a37.315360000.1868941904.282335-15851949","expires_in":2592000,"session_key":"9mzdDxLOp9Gm14\/FFUGkbC+C5YW7OUQ+HQXfh+n+uYOJMQl7HOK1NbV8KdpA4rkyTxtOyafGK8uK2A+nppm8Xg+pza8jfA==","access_token":"24.4616fbd1635afda90c1b36c4d77f91fb.2592000.1556173904.282335-15851949","scope":"public vis-faceverify_faceverify vis-faceattribute_faceattribute vis-faceverify_faceverify_v2 vis-faceverify_faceverify_match_v2 vis-faceverify_vis-faceverify-detect brain_all_scope vis-faceverify_faceverify_h5-face-liveness vis-faceverify_FACE_V3 wise_adapt lebo_resource_base lightservice_public hetu_basic lightcms_map_poi kaidian_kaidian ApsMisTest_Test\u6743\u9650 vis-classify_flower lpq_\u5f00\u653e cop_helloScope ApsMis_fangdi_permission smartapp_snsapi_base iop_autocar oauth_tp_app smartapp_smart_game_openapi oauth_sessionkey smartapp_swanid_verify smartapp_opensource_openapi","session_secret":"cbff71a1a81ad4f0d41a677a8cf58923"}

'''