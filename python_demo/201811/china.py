# 默认编码格式为 utf-8 ,python2.7 需要文章开头声明
print('中文')
def print_paras(fpara, *nums, **words):
	print("fpara:" + str(fpara))
	print("nums:" + str(nums))
	print("words:" + str(words))

print_paras('hello', 1,2,0,3,4, word="pyhon")

# userinp = input('请输入：')

# 写出
# f=open('userinp.txt', w) 
# f.write('a')
# f.close()
# 
#  写读
# f=open('userinp.txt')
# while True:
# 	line=f.readline()
# 	if len(line)==0:
# 		break
# 	print('line:'+line)

# f.close

# 语法异常处理
while True:
	try:
		x=int(input('please input:'))
		break
	except ValueError:
		print('not input...')