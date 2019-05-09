#!/usr/bin/python3

#获取json文件并保存到本地
from urllib import request
import json
# with request.urlopen('https://api.douban.com/v2/book/2129650') as f:
#     data = f.read()
#     print('Status:', f.status, f.reason)
#     for k, v in f.getheaders():
#         print('%s: %s' % (k, v))
#     print('Data:', data.decode('utf-8'))
#     
    
# 获取网络数据
with request.urlopen('https://static-data.geekbang.org/aicon2018/data.json') as f:
    data = f.read()

# 打印网络请求结果
    # print('Data:',  json.dumps(json.loads(data),ensure_ascii=False)) # 1
    # print('Data:',  data.decode('raw_unicode_escape')) # 2 存在问题
    # print(json.dumps(json.loads(data), indent=4, sort_keys=False, ensure_ascii=False))) # 3 格式化输出json数据
# 创建一个文件，修改内容
# a+ 打开一个文件用于读写。如存在，指针在结尾。如果不存在，创建。
# w+ 打开一个文件用于读写。如存在，原内容删除指针在开始。如果不存在，创建。
fo=open('./aicon.json', 'w+')
# fo.write(json.dumps(json.loads(data),ensure_ascii=False))
fo.write(json.dumps(json.loads(data), indent=4, sort_keys=False, ensure_ascii=False))
fo.close()
print('存储格式化后的文件')