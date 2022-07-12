import socket
import threading 													# 导入多线程模块
import socketserver,struct,os

Hostport=('192.168.1.101',57793)
hostport=('192.168.1.101',57792)
true = True

#聊天功能
def chatsend():
	global trues
	print("Watiing to be connected....")
	global Hostport
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)			# 创建socket实例
	s.bind(Hostport)
	s.listen(1)
	conn,addr = s.accept()
	addr = str(addr)
	print("Connecting by: "+addr)
	def Receve(conn):												# 将接收定义成一个函数
		global true 												# 声明全局变量，当接收到的消息为quit时，则触发全局变量 true = False，则会将socket关闭
		while true:
			data = conn.recv(1024).decode('utf8')
			if data == "quit":										# 当接收的值为'quit'时，退出接收线程，否则，循环接收并打印
				true = False
			print("You have receve: "+data)
	thrd=threading.Thread(target=Receve,args=(conn,))				# 线程实例化，target为方法，args为方法的参数
	thrd.start()													# 启动线程
	while true:
		uesr_input = input("请输入>>> \n")
		conn.send(uesr_input.encode('utf8'))						# 循环发送消息
		if uesr_input == 'quit':                                    # s当发送为‘quit’时，关闭socket
			true = False
		elif uesr_input == "文件发送":
			filesend()												# 输入为文件发送时调用filesend()


# 文件传输功能
def filesend():
	try:
		class MyTCP(socketserver.BaseRequestHandler):
			def handle(self):
				try:
					print("已成功连接上: ",self.client_address)
					file_define_size = struct.calcsize('128sl')									# 定义文件大小信息，128s表示文件名为128bytes长，l表示一个int或log文件类型，在此为文件大小
					self.file=self.request.recv(file_define_size)								# 接受信息并且将文件信息大小代入
					global true
					while true:
						if self.file:															# 如果文件大小存在
							self.file_name,self.file_size=struct.unpack('128sl',self.file)		# 根据128sl解包信息,与client端的打包规则相同,开始解包。
							self.file_name=self.file_name.decode('utf8').strip('\00')			# 使用strip()删除打包时附加的多余空字符
							print('文件内容大小: ',self.file_size,'文件名字: ',self.file_name)
							self.file_new_name = os.path.join("d:\\",self.file_name)#文件路径
							print('文件存储的路径为',self.file_new_name)
							recvd_filesize = 0 													# 定义了接收的文件大小
							files = open(self.file_new_name,"wb")								# 写入文件
							print("开始接收文件...")
							while not recvd_filesize == self.file_size:
								if self.file_size==0:
									break
								elif self.file_size - recvd_filesize > 10:
									rdata = self.request.recv(10)								# 这里设置为10，方便cmd看文件过大如何进行增加size的
									recvd_filesize += len(rdata)
									print(str(recvd_filesize)+"被传输")
								else:
									rdata = self.request.recv(self.file_size - recvd_filesize)	# 这里将剩下的内容补上
									recvd_filesize = self.file_size 							# 退出while循环
									print(str(recvd_filesize)+"补全")
									tcpSever.shutdown()											# 相当于结束线程
								files.write(rdata)
							files.close()														# 关闭open
							print("接收完毕")
							chatsend()
				except:
					pass
		tcpSever = socketserver.ThreadingTCPServer(hostport,MyTCP)								# TCPServer是接收到请求后执行handle方法，这里是相当于建立新线程的方法运行handle
		tcpSever.serve_forever()																# 相当于循环启动线程
	except:
		pass

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