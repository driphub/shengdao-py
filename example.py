from shengdao import ShengdaoClient,Batch_Client

file_name = input("输入文件完整路径:")	
activityId = input("输入微信公众号中的商品编号进行登记,如查询中签结果,请输入0:")	
bc = Batch_Client(file_name,activityId)
bc.server()
