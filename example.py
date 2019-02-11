from shengdao import ShengdaoClient,Batch_Client

file_name = input("输入文件完整路径：")
try:
	username = '13141350678'
	password = '123456'
	client = ShengdaoClient(username,password,'123')
except:
	raise RuntimeError()	
	print("网站革新了，请找作者联系")
	import time
	time.sleep(5)
	exit()
	
bc = Batch_Client(file_name)
bc.server()
