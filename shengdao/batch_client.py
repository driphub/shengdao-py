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
		self.shengdaolist = []
		self.clients = []
		self.pre_process()

	def pre_process(self):
		self.file_process()
		print('正在获取auths...')
		thread(self.get_auths())

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
		
	def register(self):
		for items in self.clients:
			 items['client'].register()
		print('批量登记完毕')

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
					print(items['name'] +' '+ shoe['itemName']+' '+shoe['shopName']+' 中签!')
