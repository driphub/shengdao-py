from shengdao import ShengdaoClient,Batch_Client

file_name = input("输入文件完整路径：")	
bc = Batch_Client(file_name)
bc.server()
