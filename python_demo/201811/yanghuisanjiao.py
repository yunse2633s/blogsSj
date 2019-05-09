#!/usr/bin/env python
#杨辉三角
# def YangHui (num = 10):
#     LL = [[1]]
#     for i in range(1,num):
#         LL.append([(0 if j== 0 else LL[i-1][j-1])+ (0 if j ==len(LL[i-1]) else LL[i-1][j]) for j in range(i+1)])
#     return LL



def triangles():
	ret = [1]
	while True:
		yield ret
		for i in range(1, len(ret)):
			ret[i] = pre[i] + pre[i - 1]
			ret.append(1)
			pre = ret[:]

		print(pre)

triangles()