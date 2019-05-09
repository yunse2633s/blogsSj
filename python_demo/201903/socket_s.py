#!/usr/bin/ptyhon
import socket
import subprocess  #导入执行命令模块
ip_port=('127.0.0.1', 9999)  #定义元组
#买手机
s=socket.socket()  #绑定协议，生产套接字
s.bind(ip_port)  #绑定ip+协议+端口：用来唯一标识一个进程，ip_port必须是元组格式
s.listen(5) # 定义最大可以挂起链接数。若是缺少这个，程序会报错。


# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.bind((ip_port))
#     s.listen(1)
#     conn, addr = s.accept()


# '''
#等待电话
while True:  #用来重复接收新的链接
	conn,addr=s.accept()  #接收客户端ping链接请求，返回conn（相当于一个特定ping链接），addr是客户端ip+port
	#收消息
	while True:  #用来基于一个链接重复接收消息
		try:  #朴拙客户端异常关闭
			recv_data=conn.recv(1024)  #收消息，阻塞
			if len(recv_data)==0: break  #客户端如果退出，服务端将接收空消息，退出

			#发消息
			p=subprocess.Popen(str(recv_data,encoding='utf8'), shell=True, stdout=subprocess.PIPE)

			res=p.stdout.read()  #获取标准输出
			if len(res)==0:  #执行错误命令，标准输出为空
				send_data='cmd err'
			else:
				send_data=str(res, encoding='gbk')  #命令执行ok，字节gbk->str->字节utf-8

			send_data=bytes(send_data, encoding='utf8')

			#解决粘包问题
			ready_tag='Ready!%s'%len(send_data)
			conn.send(bytes(ready_tag,encoding='utf8'))  #发送数据长度
			feedback=conn.recv(1024)  #接收确认信息
			feedback=str(feedback, encoding='utf8')

			if feedback.startswith('Start'):
				print('send_data',send_data)
				conn.send(send_data)  #发送命令的执行结果
		except Exception:
			break

	#挂断电话
	conn.close()



# '''