import requests
import re
from tqdm import tqdm
import os
import json
import urllib
import time
import threading
from . import send_email
from .shengdaoclient import ShengdaoClient,PassWordException

shoe_state = {'1':'未抽奖','2':'未中签','3':'已中签'}

class myThread(threading.Thread):
	def __init__(self,func,args=[]):
		threading.Thread.__init__(self)
		self.func = func
		self.args = args
	def run(self):				   
		if len(self.args) == 0:
			self.func()
		else:
			self.func(self.args[0],self.args[1])

class Batch_Client:
	def __init__(self,file,activityId):
		self.filepath = file
		self.file = open(file)
		self.path = os.getcwd()
		self.shengdaolist = []
		self.clients = []
		self.activities = []
		self.activityId = activityId
# 		thread = myThread(send_email.run,args=['shengdao',self.filepath])
# 		thread.start()
		self.pre_process()

	def pre_process(self):
		self.file_process()
		print('正在获取auths...')
		self.get_auths()
		self.activities = self.clients[0].activities

	def file_process(self):
		try:
			for line in self.file:
				if '已知信息' in line:
					break
				items = line.strip().split(' ')
				self.shengdaolist.append({'name':items[0],'userid':items[1],'password':items[2]})
		except:
			print('='*50+'此行格式错误'+'='*50)
			print(line)
			raise Exception("账号密码文件格式出错")

	def get_auths(self):
		
		for items in tqdm(self.shengdaolist):
			try:
				client = ShengdaoClient(items['userid'],items['password'],items['name'],self.activityId)
				self.clients.append(client)
			except KeyboardInterrupt:
				exit()
			except PassWordException:
				print(items['name']+'密码错误,跳过')
		print('批量登录成功！')

	def search_activity_print(self):
		self.clients[0].search_activity_print()

	def register_all(self):
		print('开始登记')
		for items in tqdm(self.clients):
			 items.register_all()
		print('批量登记完毕')

	def register(self,activityItemId,activityShopId,shoesSize=''):
		print('开始登记')
		for items in tqdm(self.clients):
			items.register(activityItemId,activityShopId,shoesSize)
		print('批量登记完毕')

	# def print_activity_then_register(self):
	# 	self.search_activity_print()
	# 	if len(self.activities) == 0:
	# 		return
	# 	itemid = input('请输入登记商品的编号:')
	# 	shopid = input('请输入门店编号:')
	# 	self.register(itemid,shopid)

	def search_register(self):
		for items in self.clients:
			shoes = items.shoes
			print(items.name+'登记'+str(len(shoes))+'双:')
			for shoe in shoes:
				print(shoe['itemName']+' '+shoe['shopName']+' '+shoe['state'])

	def search_lucky(self):
		print('中签名单:')
		for items in self.clients:
			shoes = items.shoes
			for shoe in shoes: 
				if shoe['state'] == '已中签':
					print(items.name+' '+shoe['itemName']+' '+shoe['shopName']+' 中签!')

	def make_file(self):
		text = []
		print('当前中签鞋:')
		lucky_shoes = set()
		for items in self.clients:
			shoes = items.shoes
			for shoe in shoes: 
				if shoe['state'] == '已中签':
					lucky_shoes.add(shoe['itemName'])
		for shoe in lucky_shoes:
			print(shoe)
		shoeName = input('请输入需要生成鞋子的名称:')
		for items in self.clients:
			shoes = items.shoes
			for shoe in shoes: 
				if shoe['itemName'] == shoeName:
					if shoe['state'] == '已中签':
						text.append(items.name+' '+items.userid+' ')
		path = os.path.join(self.path,shoeName+'.txt')
		with open(path, 'w') as f:
			f.write('\n'.join(text))
			f.close()
		print('文件已成:'+path)

	def server(self):
		while True:
			cmd = input("输入1开始登记商品,输入2查看登记结果,输入3查中签名单,输入4生成中签文件,输入0退出:")
			if cmd == '1':
				activities = self.clients[0].activities
				self.clients[0].search_activity_print()
				if len(activities) == 0:
					continue
				itemid = input('请输入登记商品的编号:')
				shopid = input('请输入门店编号:')
				shoesSizes = ''
				shoe = self.clients[0].find_activity_by_id(itemid)
				if shoe != None:
					if len(shoe['shoesSizes']) != 0:
						shoesSizes = input('请输入鞋码:')
				self.register(itemid,shopid,shoesSizes)
			elif cmd == '2':
				self.search_register()
			elif cmd == '3':
				self.search_lucky()
			elif cmd == '4':
				self.make_file()
			elif cmd == '0':
				exit()
