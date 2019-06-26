import requests
import re
from tqdm import tqdm
import os
import json
import urllib
import time
import threading
from retrying import retry

shoe_state = {'1':'未抽奖','2':'未中签','3':'已中签'}

class PassWordException(Exception):
	def __init__(self):
		pass

def retry_log(attempts, delay):
	print('retry')


def retry_if_not_passworderror(exception):
	if isinstance(exception, PassWordException) or isinstance(exception, KeyboardInterrupt):
		return False
	else:
		return True
	# 当密码错误时不重试，只有在网络不好的状况下重试

class ShengdaoClient:

	@retry(stop_func=retry_log,retry_on_exception=retry_if_not_passworderror)
	def __init__(self,userid,password,name=None):
		self.userid = userid
		self.password = password
		if name == None:
			self.name = userid
		else:
			self.name = name
		self.auth = self.get_auth()
		self.shoes = self.search_register()
		self.activities = self.search_activity()
		# shoes 和 activities 永远维持最新状态,避免每次都要调用search方法

	# def pre_process(self):
	# 	self.activities = self.search_activity()
	# 	self.shoes = self.search_register()


	def get_auth(self):	
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

		response = requests.post('https://sso-prod.yysports.com/api/member/pousheng/account/login', headers=headers, data=data)
		cookies = response.headers['Set-Cookie'].split('tssoid=')[1].split(';Path')[0]
		# cookies = requests.utils.dict_from_cookiejar(session.cookies)['tssoid']
		# 这里是set-cookies，所以cookies已经在session里了，也可以从response-header拿
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
		try:
			self.code = response.url.split('code=')[1].split('&')[0]
		except:
			raise PassWordException
		result = requests.get('http://wx.yysports.com/limitelottery/regist/checkssologin?code='+self.code+'&redirecturl=form.html')
		
		if 'jwt' in json.loads(result.text).keys():
			token = json.loads(result.text)['jwt']

		# while 'jwt' not in json.loads(result.text).keys():
		# 	print('retry jwt')
		# 	result = requests.get('http://wx.yysports.com/limitelottery/regist/checkssologin?code='+code+'&redirecturl=form.html')
		# 	if 'jwt' in json.loads(result.text).keys():
		# 		token = json.loads(result.text)['jwt']

		header = {
			"Authorization": "Bearer " + token
		}
		self.auth = header
		return header

	def id_verify(self,name,uid,mobile):
		headers = {
			'Authorization':self.auth,
			'Origin': 'http://wx.yysports.com',
			'Accept-Encoding': 'gzip, deflate',
			'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
			'Content-Type': 'application/json',
			'Accept': '*/*',
			'Referer': 'http://wx.yysports.com/limitelottery/form.html?code='+self.code+'&state=284a5e319abb4833bdaf39322beb4d7b',
			'X-Requested-With': 'XMLHttpRequest',
			'Connection': 'keep-alive',
		}
		data = '{"userName":'+name+',"personalId":"320705199704293514"'+uid+',"mobile":'+mobile+'}'

		response = requests.post('http://wx.yysports.com/limitelottery/regist', headers=headers, data=data)

	def search_activity(self): 
		activities = []										  
		result = requests.get('http://wx.yysports.com/limitelottery/activity',headers=self.auth)
		# print(result.text)
		for shoe in json.loads(result.text):
			activities.append({'activityItemId':shoe['activityItemId'],'itemName':shoe['itemName'],"activityShops":shoe['activityShops'],"shoesSizes":shoe['shoesSizes']})
		return activities

	def search_activity_print(self): 
		self.activities = self.search_activity()
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
				print('可登记鞋码:'+str(shoe['shoesSizes']))
				print('='*50)

	def find_activity_by_id(self,_id):
		for shoe in self.activities:
			if str(_id) == str(shoe['activityItemId']):
				return shoe
		return

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
				self.activities = self.search_activity()
				self.shoes = self.search_register()
			else:
				print(self.name + ' ' + shoe['itemName'] + ' ' + '登记失败')
			return
		print(self.name+'现在没有可登记商品')

	def register(self,activityItemId,activityShopId,shoesSize=''):
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
		try:
			# for shoe in self.activities:
			# 	if str(activityItemId) == str(shoe['activityItemId']):
			# 		shoeName = shoe['itemName']
			shoe = self.find_activity_by_id(activityItemId)
			shoeName = shoe['itemName']

			data = [{"activityItemId":activityItemId,"activityShopId":activityShopId}]
			if shoesSize != '':
				data = [{"activityItemId":activityItemId,"activityShopId":activityShopId,"shoesSize":shoesSize}]

			data = json.dumps(data)
			response = requests.post('http://wx.yysports.com/limitelottery/activity', headers=headers,data=data)
			if response.status_code == 200:
				print(self.name + ' ' + shoeName + ' ' + '登记成功')
				self.activities = self.search_activity()
				self.shoes = self.search_register()
			else:
				print(self.name + ' ' + shoeName + ' ' + '登记失败')
			return
		except:
			print(self.name + ' ' + '登记失败')
			return
		print(self.name+'现在没有可登记商品')



	def search_register(self):
		shoes = []
		result = requests.get('http://wx.yysports.com/limitelottery/activity/registitems',headers=self.auth)
		for shoe in json.loads(result.text):
			if len(shoe['activityShops']) != 0: # 存在没有shop的情况
				shoes.append({'itemName':shoe['itemName'],'shopName':shoe['activityShops'][0]['shopName'],'state':shoe_state[shoe['state']]})
			else:
				shoes.append({'itemName':shoe['itemName'],'shopName':'','state':shoe_state[shoe['state']]})
		return shoes

	def search_register_print(self):
		shoes = self.search_register()
		print(self.name+"登记数量:"+str(len(result)))		
		for shoe in shoes:
			print(shoe['itemName']+' '+shoe['activityShops'][0]['shopName']+' '+shoe['state'])

