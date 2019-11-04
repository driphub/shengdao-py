from shengdao import Batch_Client

file_name = input("输入文件完整路径:")
method = input("输入登录方式,1为账号密码登录,2为auth:")
city = input("请输入登记地区(如北京):")
activityId = input("输入微信公众号中的商品编号进行登记,如查询中签结果,请输入0:")	
bc = Batch_Client(file_name,activityId,city,int(method))
# bc = Batch_Client('1.txt','0','北京',int(1))

bc.server()

# 登录方式1已经开始封ip，所以现在主要用登陆方式1获取auth，会自动整理出登陆方式2的文件保存为auths.txt
# 登录方式2是用auth直接发请求，跳过登陆部分。