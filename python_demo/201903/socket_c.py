#!/usr/bin/python
import socket
ip_port=('127.0.0.1', 9999)
#买手机
s=socket.socket()
#拨号
s.connect(ip_port)  #链接服务端， 如果存在则挂起

while True:
	send_data=input(">>:").strip()
	if send_data=='exit':break
	if len(send_data)==0:continue
	s.send(bytes(send_data, encoding='utf8'))

	#解决粘包问题
	ready_tag=s.recv(1024)  #收取带 数据长度 的字节
	ready_tag=str(ready_tag,encoding='utf8')
	if ready_tag.startswith('Ready'):
		msg_size=int(ready_tag.split('!')[-1])  #获取待接收数据长度
	start_tag='Start'
	s.send(bytes(start_tag, encoding='utf8'))  #发送确认信息

	#基本已经收到的待接收数据长度，循环接收数据
	recv_size=0
	recv_msg=b''

	while recv_size<msg_size:
		recv_data=s.recv(1024)
		recv_msg+=recv_data
		recv_size+=len(recv_data)
		print('MSG SIZE %s RECE SIZE %s' %(msg_size, recv_size))

	print(str(recv_msg, encoding='utf8'))

s.close()
