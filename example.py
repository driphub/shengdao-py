from shengdao import ShengdaoClient,Batch_Client

file_name = input("输入文件完整路径：")
try:
	username = '13141350678'
	password = 'shengdaotiyu'
	client = ShengdaoClient(username,password,'123')
except:
	raise RuntimeError()	
	print("网站革新了，请找作者联系")
	import time
	time.sleep(5)
	exit()
bc = Batch_Client(file_name)
print('批量登录成功！')

while True:
	cmd = input("输入1开始登记商品,输入2查看登记结果,输入3查中签名单,输入4生成中签文件,输入0退出:")
	if cmd == '1':
		bc.clients[0]['client'].search_activity_print()
		if len(bc.clients[0]['client'].search_activity()) == 0:
			continue
		itemid = input('请输入登记商品的编号:')
		shopid = input('请输入门店编号:')
		bc.register(itemid,shopid)
	elif cmd == '2':
		bc.search_register()
	elif cmd == '3':
		bc.search_lucky()
	elif cmd == '4':
		bc.make_file()
	elif cmd == '0':
		exit()
