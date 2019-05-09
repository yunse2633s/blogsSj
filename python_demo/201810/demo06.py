# coding:utf-8
# python2 用户输入url，抓取图片
# 
import urllib
import re
import time

# 定义获取图片的函数
def get_image(html_code):
	reg=r'src="(.+?\.jpg" width'
	reg_img=re.compile(reg)
	img_list=reg_img.findall(html_code)
	x=0
	for img in img_list:
		print img
		x=x+1

# 获取html源码
def get_html(url):
	#如果url 没有http 或https 则增加
	page=urllib.urlopen(url)
	html=page.read()
	return html

time_stap=int(round(time.time()*1000))

#print time_stap
#pageFile = open(time_stap+'.txt', 'a+') #打开，追加写
#pageFile.close() #关闭

def user_input():
	print u'请输入url:'
	url=raw_input()
	return url

# main	
url=user_input()
if url:
	pass
else:
	print u'请输入url:'

html_code=get_html(url)
get_image(html_code)