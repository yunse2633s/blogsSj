#coding:utf-8
# 基于python2 爬去网页信息
#  参考资料 https://www.cnblogs.com/Axi8/p/5757270.html
import urllib
import re

def get_html(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

reg = r'src="(.+?\.jpg)" width'#正则表达式
reg_img = re.compile(reg)#编译一下，运行更快
imglist = reg_img.findall(get_html('http://tieba.baidu.com/p/1753935195'))#进行匹配

pageFile=open('demo05_push_img.txt', 'a+')
# 循环写入
for img in imglist:

	pageFile.write(img+'\n')

pageFile.close()