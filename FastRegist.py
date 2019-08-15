from shengdao.shengdaoclient import ShengdaoClient
from tqdm import tqdm

file_name = input("输入文件完整路径：")	
activityId = input("输入微信公众号中的商品编号进行登记:")
shengdaolist = []
try:
	for line in open(file_name):
		if '已知信息' in line:
			break
		items = line.strip().split(' ')
		shengdaolist.append({'name':items[0],'userid':items[1],'password':items[2]})
except:
	print('='*50+'此行格式错误'+'='*50)
	print(line)
	raise Exception("账号密码文件格式出错")

firstpeople = ShengdaoClient(shengdaolist[0]['userid'],shengdaolist[0]['password'],shengdaolist[0]['name'],activityId)
firstpeople.search_activity_print()
activities = firstpeople.activities
shoe = activities[0]
if len(activities) == 0:
	print('尝试将第一位用户换成他人')
else:
	itemid = input('请输入登记商品的编号:')
	shopid = input('请输入门店编号:')
	shoesSizes = ''
	if len(shoe['shoesSizes']) != 0:
		shoesSizes = input('请输入鞋码:')
	for item in tqdm(shengdaolist):
		shengdaoclient = ShengdaoClient(item['userid'],item['password'],item['name'],activityId)
		shengdaoclient.register(itemid,shopid,shoesSizes)