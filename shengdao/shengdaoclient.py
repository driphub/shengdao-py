import requests
import re
from tqdm import tqdm
import os
import json
import urllib
import time
import threading

shoe_state = {'1':'未抽奖','2':'未中签','3':'已中签'}

class ShengdaoClient:
	def __init__(self,userid,password,name=None):
		self.userid = userid
		self.password = password
		if name == None:
			self.name = userid
		else:
			self.name = name
		self.pre_process()

	def pre_process(self):
		self.auth = self.get_auth()
		self.activities = self.search_activity()
		self.shoes = self.search_register()

	def get_auth(self):	
		session = requests.session()

		headers = {
			'Origin': 'https://sso-prod.yysports.com',
			'Accept-Encoding': 'gzip, deflate, br',
			'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
			'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Mobile Safari/537.36',
			'Content-Type': 'application/json',
			'Accept': '*/*',
			'Referer': 'https://sso-prod.yysports.com/login?redirect_uri=http://wx.yysports.com/limitelottery/form.html&from=200000211&fromType=1&client_id=matrix',
			'x-requested-with': 'XMLHttpRequest',
			'Connection': 'keep-alive',
		}
		data = {"username":self.userid,"password":self.password,"client_id":"matrix","redirect_uri":"http://wx.yysports.com/limitelottery/form.html","response_type":"code"}
		data = json.dumps(data)

		response = session.post('https://sso-prod.yysports.com/api/member/pousheng/account/login', headers=headers, data=data)
		cookies = requests.utils.dict_from_cookiejar(session.cookies)['tssoid']

		cookies = {
			'tssoid': cookies
		}
		headers = {
			'Connection': 'keep-alive',
			'Upgrade-Insecure-Requests': '1',
			'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Mobile Safari/537.36',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'Referer': 'https://sso-prod.yysports.com/login?redirect_uri=http://wx.yysports.com/limitelottery/form.html&from=244000018&fromType=1&client_id=matrix&state=9934af259a69498f86644851cea1e122',
			'Accept-Encoding': 'gzip, deflate, br',
			'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
		}

		params = (
			('client_id', 'matrix'),
			('redirect_uri', 'http://wx.yysports.com/limitelottery/form.html'),
			('response_type', 'code'),
			('state', '9934af259a69498f86644851cea1e122'),
		)

		response = requests.get('https://sso-prod.yysports.com/oauth/authorize', headers=headers, params=params, cookies=cookies)
		code = response.url.split('code=')[1].split('&')[0]


		result = requests.get('http://wx.yysports.com/limitelottery/regist/checkssologin?code='+code+'&redirecturl=form.html')

		token = json.loads(result.text)['jwt']

		header = {
			"Authorization": "Bearer " + token
		}
		self.auth = header
		return header

	def search_activity(self): 
		activities = []										  
		result = requests.get('http://wx.yysports.com/limitelottery/activity',headers=self.auth)
		# print(result.text)
		for shoe in json.loads(result.text):
			activities.append({'activityItemId':shoe['activityItemId'],'itemName':shoe['itemName'],"activityShops":shoe['activityShops']})
		return activities

	def search_activity_print(self): 
		if len(self.activities) == 0:
			print(self.name+'现在没有可登记商品')
		else:
			print(self.name+"现可登记:")
			for shoe in self.activities:
				# activities.append({'activityItemId':shoe['activityItemId'],'name':shoe['itemName']})
				print('商品编号:'+str(shoe['activityItemId']))
				print(shoe['itemName'])
				print('可登记鞋店:')
				for shop in shoe['activityShops']:
					print('鞋店编号:'+str(shop['activityShopId']))
					print('鞋店名称:'+str(shop['shopName']))
				print('='*50)

	def register_all(self):

		headers = {
			'Authorization': self.auth['Authorization'],
			'Origin': 'http://wx.yysports.com',
			'Accept-Encoding': 'gzip, deflate',
			'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
			'Content-Type': 'application/json', # 必要
			'Accept': '*/*',
			'Referer': 'http://wx.yysports.com/limitelottery/product-list.html',
			'X-Requested-With': 'XMLHttpRequest',
			'Connection': 'keep-alive',
		}

		for shoe in self.activities:
			data = [{"activityItemId":shoe['activityItemId'],"activity ShopId":"1640"}]
			data = json.dumps(data)
			response = requests.post('http://wx.yysports.com/limitelottery/activity', headers=headers,data=data)
			if response.status_code == 200:
				print(self.name + ' ' + shoe['itemName'] + ' ' + '登记成功')
			else:
				print(self.name + ' ' + shoe['itemName'] + ' ' + '登记失败')
			return
		print(self.name+'现在没有可登记商品')

	def register(self,activityItemId,activityShopId):
		headers = {
			'Authorization': self.auth['Authorization'],
			'Origin': 'http://wx.yysports.com',
			'Accept-Encoding': 'gzip, deflate',
			'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
			'Content-Type': 'application/json', # 必要
			'Accept': '*/*',
			'Referer': 'http://wx.yysports.com/limitelottery/product-list.html',
			'X-Requested-With': 'XMLHttpRequest',
			'Connection': 'keep-alive',
		}

		for shoe in self.activities:
			if str(activityItemId)== str(shoe['activityItemId']):
				shoeName = shoe['itemName']

		data = [{"activityItemId":activityItemId,"activityShopId":activityShopId}]
		data = json.dumps(data)
		response = requests.post('http://wx.yysports.com/limitelottery/activity', headers=headers,data=data)
		if response.status_code == 200:
			print(self.name + ' ' + shoeName + ' ' + '登记成功')
		else:
			print(self.name + ' ' + shoeName + ' ' + '登记失败')
		return
		print(self.name+'现在没有可登记商品')



	def search_register(self):
		shoes = []
		result = requests.get('http://wx.yysports.com/limitelottery/activity/registitems',headers=self.auth)
		for shoe in json.loads(result.text):
			shoes.append({'itemName':shoe['itemName'],'shopName':shoe['activityShops'][0]['shopName'],'state':shoe_state[shoe['state']]})
		return shoes

	def search_register_print(self):

		result = requests.get('http://wx.yysports.com/limitelottery/activity/registitems',headers=self.auth)
		print(self.name+"登记数量:"+str(len(json.loads(result.text))))		
		for shoe in json.loads(result.text):
			print(shoe['itemName']+' '+shoe['activityShops'][0]['shopName']+' '+shoe_state[shoe['state']])


