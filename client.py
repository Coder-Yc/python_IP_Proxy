import socket,os,struct
import threading
import time
true=True
#聊天
def chatsend():
	global true
	hostport=('127.0.0.1',12303)										# 这是本地的可以采用cmd的netstat查看IP和端口,端口数字往后移动一位
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)				# 创建socket实例
	s.connect(hostport)													# 连接IP和端口
	def Receve(s):
		global true
		while true:
			data=s.recv(1024).decode("utf8")
			if data == "quit":
				true = False
			elif data == "文件发送":
				sendfile()
			print('receve news: '+data)
	thrd=threading.Thread(target=Receve,args=(s,))						# 线程实例化，target为方法，args为方法的参数
	thrd.start()														# 启动线程
	while true:
		uesr_input=input("请输入: \n")
		s.send(uesr_input.encode("utf8"))
		if uesr_input == "quit":										# 当发送为‘quit’时，关闭socket
			true = False

#发送文件
def sendfile():
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.connect(('127.0.0.1',12304))								
	true = True
	def xunhuanchuanshu(s):
		filepath = input("对方请求发送文件，请输入文件的绝对路径:\r\n")												# 换行符为各系统默认的换行符（\n, \r, or \r\n, ）
		if os.path.isfile(filepath):
			file_pack =struct.pack('128sl',os.path.basename(filepath).encode('utf8'),os.stat(filepath).st_size) # pack需要定义文件头信息，包含文件名和文件大小
			s.send(file_pack)																					# 发送包
			print('客户端传输文件绝对路径: ', filepath)
			open_file = open(filepath,'rb')																		# 读取成二进制格式数据
			while True:
				file_data = open_file.read(1024)
				if not file_data:																				# 判断文件是否存在,并且进行传输
					break
				s.send(file_data)																				# 发送数据
			open_file.close()
			print('传输完成！')
	thrd=threading.Thread(target=xunhuanchuanshu,args=(s,))														# 线程实例化，target为方法，args为方法的参数
	thrd.start()

if __name__ == '__main__':
	print('''
请选择功能：
	1.聊天(附带文件发送功能。输入文件发送)
		''')
	sda=True
	while sda:
		keyboard_input=input()
		if keyboard_input=="1":
			chatsend()
			sda=False
		else:
			print("输入选择项错误请重新输入")
			continue