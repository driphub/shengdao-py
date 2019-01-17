from shengdao import ShengdaoClient,Batch_Client

bc = Batch_Client('shengdao.txt')
while True:
	cmd = input("输入1开始登记商品,输入2查看登记结果,输入3查中签名单,输入0退出:")
	if cmd == '1':
		bc.print_activity_then_register()
	elif cmd == '2':
		bc.search_register()
	elif cmd == '3':
		bc.search_lucky()
	elif cmd == '0':
		exit()