#! /usr/bin/python3
#
import sqlite3
import json
import requests

# 抓包地址
url = 'http://m.maoyan.com/mmdb/comments/movie/1208282.json?v=yes&offset=15'
url_n = 'http://m.maoyan.com/mmdb/comments/movie/1208282.json?v=yes&offset='


#
# 获取数据
#
def getMoveinfo(url):
	session = requests.Session()
	headers = {
		"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X)"
	}
	response = session.get(url, headers=headers)
	if response.status_code == 200:		
		return response.text
	return None

#
#数据处理
#

def parseInfo(data):
	data = json.loads(html)['cmts']
	for item in data:
		yield{
			'date':item['startTime']
			,'nickname':itme['nickName']
			,'city':item['cityName']
			,'rate':item['score']
			,'conment':item['content']
		}


#
# 存储数据
# 

def saveCommentInfo(moveId, nickname, comment, rate, city, start_time):
	print('cc', moveId, nickname, comment, rate, city, start_time)
	conn = sqlite3.connect('movieComment.db')
	conn.text_factory=str
	cursor=conn.cursor()
	ins="insert into comment values(?,?,?,?,?,?)"
	v=(moveId, nickname, comment, rate, city, start_time)
	cursor.execute(ins, v)
	cursor.close()
	conn.commit()
	conn.close()

#
# 如何批量存储数据呢
# 
 
# 
# 将http返回值存储未 json文件
# 
def saveRequestJson(url):
	# 获取http请求结果
	model=getMoveinfo(url)
	# 存储数据
	with open('./dmm.json', 'w', encoding='utf-8') as json_file:
		json.dump(model, json_file, ensure_ascii=False)

	print('ok')

#
# 将数据保存json格式的文件
# 


# 
# 读取json数据
# 
def readJson():
	model={}
	with open('./dmm.json', 'r', encoding='utf-8') as json_file:
		model=json.load(json_file)

	return json.loads(model)['cmts']

# cc = readJson()

def generatorDemo():
	# 读取json数据
	cc = readJson()
	
	# 提取需要的数据, yield的作用是将一个函数变成一个generator
	# 
	for item in cc:
		# 程序执行到yield时就会return
		# print(item['startTime'], item['nickName'], item['cityName'], item['score'], item['content'])
		yield{
			'date':item['startTime']
			,'nickname':item['nickName']
			,'city':item['cityName']
			,'rate':item['score']
			,'comment':item['content']
		}

# demandData = generatorDemo() # 数据只存

#
# 时间戳，获取运行时间
#
import time

class Elapse_time(object):
    '''耗时统计工具'''
    def __init__(self, prompt=''):
        self.prompt = prompt
        self.start = time.time()
        
    def __del__(self):
        print('%s耗时: %.3f' % (self.prompt, time.time() - self.start))

def jsonLoopSqlite():
	wuyi = generatorDemo()
	for item in wuyi:
		# moveId, nickname, comment, rate, city, start_time
		saveCommentInfo('1208282', item['nickname'], item['comment'], item['rate'], item['city'], item['date'])

# Elapse_times = Elapse_time()

def loopushsqlite(urlT):
	#
	html=getMoveinfo(urlT);

	cy = json.loads(html)['cmts']

	for item in cy:
		saveCommentInfo('1208282', item['nickName'], item['content'], item['score'], item['cityName'], item['startTime'])
#
# 向数据库中逐条添加评论
#
def stepTostepAdd():
	#初始起始页
	num=697 # (1 - 696 磁盘读写占90% 每页15条数据， db文件1.38M)
	while num < 1000:
		cw="%s%s"%(url_n,num)
		loopushsqlite(cw)
		num=num+1
		pass

# Elapse_time()