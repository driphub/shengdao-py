#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import re
from tqdm import tqdm
import os
import json
import urllib

users = []
class Batch_Client:
	def __init__(self,file):
		self.f = open(file)
		self.shoe_state = {'1':'未抽奖','2':'未中签','3':'已中签'}
		self.shengdaolist = []
		self.auths = []
		self.pre_process()

	
	def pre_process(self):
		self.file_process()
		self.get_auths()

	def file_process(self):
		try:
			for line in self.f:
				items = line.strip().split(' ')
				self.shengdaolist.append({'name':items[0],'userid':items[1],'password':items[2]})
		except:
			raise Exception("账号密码文件格式出错")

	def get_auths(self):
		for items in tqdm(self.shengdaolist):
			try:
				client = ShengdaoClient(items['userid'],items['password'],items['name'])
				self.auths.append({'name':items['name'],'auth':client.get_auth()})
			except KeyboardInterrupt:
				exit()
			except:
				print(items['name']+'获取auth失败，跳过')

	def search_register(self):
		for items in self.auths:
			result = requests.get('http://wx.yysports.com/limitelottery/activity/registitems',headers=items['auth'])
			print(items['name']+"登记数量:"+str(len(json.loads(result.text))))		
			for shoe in json.loads(result.text):
				print(shoe['itemName']+' '+shoe['activityShops'][0]['shopName']+' '+self.shoe_state[shoe['state']])

	def search_lucky(self):
		for items in self.auths:
			result = requests.get('http://wx.yysports.com/limitelottery/activity/registitems',headers=items['auth'])
			for shoe in json.loads(result.text):
				if self.shoe_state[shoe['state']] == '已中签':
					print(items['name'] +' '+ shoe['itemName']+' '+shoe['activityShops'][0]['shopName']+' 中签!')

class ShengdaoClient:
	def __init__(self,userid,password,name=None):
		self.userid = userid
		self.password = password
		if name == None:
			self.name = userid
		self.auth = None
		self.shoe_state = {'1':'未抽奖','2':'未中签','3':'已中签'}

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
												  
		result = session.get('http://wx.yysports.com/limitelottery/activity',headers=self.auth)
		print(result.text)

	def search_register(self):

		result = requests.get('http://wx.yysports.com/limitelottery/activity/registitems',headers=self.auth)
		print(self.name+"登记数量:"+str(len(json.loads(result.text))))		
		for shoe in json.loads(result.text):
			print(shoe['itemName']+' '+shoe['activityShops'][0]['shopName']+' '+self.shoe_state[shoe['state']])

Batch_Client('shengdao.txt')
