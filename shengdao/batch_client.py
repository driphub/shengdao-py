import requests
import re
from tqdm import tqdm
import os
import json
import urllib
import time
import threading
from .shengdaoclient import ShengdaoClient

shoe_state = {'1':'未抽奖','2':'未中签','3':'已中签'}
max_thread = 4

def thread(func):
    thread_list = []
    for i in range(0,max_thread):
        t = threading.Thread(target=func)
        thread_list.append(t)
    for i in thread_list:
        i.start()
    for i in thread_list:
        i.join()

class Batch_Client:
	def __init__(self,file):
		self.f = open(file)
		self.path = os.getcwd()
		self.shengdaolist = []
		self.clients = []
		self.activities = []
		self.pre_process()

	def pre_process(self):
		self.file_process()
		print('正在获取auths...')
		thread(self.get_auths())
		self.activities = self.clients[0]['client'].search_activity()

	def file_process(self):
		try:
			for line in self.f:
				items = line.strip().split(' ')
				self.shengdaolist.append({'name':items[0],'userid':items[1],'password':items[2]})
		except:
			print('='*50+'此行格式错误'+'='*50)
			print(line)
			raise Exception("账号密码文件格式出错")

	def get_auths(self):
		for items in tqdm(self.shengdaolist):
			try:
				client = ShengdaoClient(items['userid'],items['password'],items['name'])
				self.clients.append({'name':items['name'],'client':client})
				# self.auths.append({'name':items['name'],'auth':client.get_auth()})
			except KeyboardInterrupt:
				exit()
			except IndexError:
				print(items['name']+'密码错误,跳过')

	def search_activity_print(self):
		self.clients[0]['client'].search_activity_print()

	def register_all(self):
		print('开始登记')
		for items in tqdm(self.clients):
			 items['client'].register_all()
		print('批量登记完毕')

	def register(self,activityItemId,activityShopId):
		print('开始登记')
		for items in tqdm(self.clients):
			items['client'].register(activityItemId,activityShopId)
		print('批量登记完毕')

	def print_activity_then_register(self):
		self.search_activity_print()
		if len(self.activities) == 0:
			return
		itemid = input('请输入登记商品的编号:')
		shopid = input('请输入门店编号:')
		self.register(itemid,shopid)

	def search_register(self):
		for items in self.clients:
			shoes = items['client'].search_register()
			# result = requests.get('http://wx.yysports.com/limitelottery/activity/registitems',headers=items['auth'])
			# print(items['name']+"登记数量:"+str(len(json.loads(result.text))))		
			print(items['name']+'登记'+str(len(shoes))+'双:')
			for shoe in shoes:
				print(shoe['itemName']+' '+shoe['shopName']+' '+shoe['state'])

	def search_lucky(self):
		print('中签名单:')
		for items in self.clients:
			shoes = items['client'].shoes
			for shoe in shoes: 
				if shoe['state'] == '已中签':
					print(items['name']+' '+shoe['itemName']+' '+shoe['shopName']+' 中签!')

	def make_file(self):
		text = []
		print('当前中签鞋:')
		lucky_shoes = set()
		for items in self.clients:
			shoes = items['client'].shoes
			for shoe in shoes: 
				if shoe['state'] == '已中签':
					lucky_shoes.add(shoe['itemName'])
		for shoe in lucky_shoes:
			print(shoe)
		shoeName = input('请输入需要生成鞋子的名称:')
		for items in self.clients:
			shoes = items['client'].shoes
			for shoe in shoes: 
				if shoe['itemName'] == shoeName:
					if shoe['state'] == '已中签':
						text.append(items['name']+' '+items['client'].userid+' ')
		path = os.path.join(self.path,shoeName+'.txt')
		with open(path, 'w') as f:
			f.write('\n'.join(text))
			f.close()
		print('文件已成:'+path)
