import requests
import json
import time
from tqdm import tqdm

def check(mobile):
	cookies = {
	    'taid': '',#需要填充
	    'msidPousheng': '',#需要填充
	}

	headers = {
	    'Accept-Encoding': 'gzip, deflate, br',
	    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
	    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
	    'Accept': '*/*',
	    'Referer': 'https://sso-prod.yysports.com/register?client_id=matrix&from=244000018&fromType=1&redirect_uri=http%3A%2F%2Fwx.yysports.com%2Flimitelottery%2Fform.html&response_type=code&state=99dea57a1f7e4616b74d67254964065a',
	    'x-requested-with': 'XMLHttpRequest',
	    'Connection': 'keep-alive',
	}

	params = (
	    ('mobile', ''),#需要填充
	)

	response = requests.get('https://sso-prod.yysports.com/api/member/pousheng/account/check-mobile', headers=headers, params=params, cookies=cookies)
	return response.text

def get_message(phone):
	print('正在获取验证码')
	time.sleep(20)
	r = requests.get('http://w6888.cn:9180/service.asmx/GetYzmStr?token='+token+'&hm='+phone+'&xmid=4351')
	headers = {
		 'Referer': 'https://sso-prod.yysports.com/register?client_id=matrix&from=244000018&fromType=1&redirect_uri=http%3A%2F%2Fwx.yysports.com%2Flimitelottery%2Fform.html&response_type=code&state=b2ad0e92cf96453b9fc0c66ad018d07f',
		 'Origin': 'https://sso-prod.yysports.com',
		 'x-requested-with': 'XMLHttpRequest',
		 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
		 'Content-Type': 'application/json',
	}
	result = r.text	
	if result == '1':
		return False
	print(result)
	result = result.split('胜道体育】注册验证码为 ')[1].split('，')[0]
	print('验证码为:'+result)
	return str(result)

def lianzhong(s):
	url = 'https://v2-api.jsdama.com/upload'
	data = {
		'softwareId': 14529,
		'softwareSecret': "", #需要填充
		'username': "",#需要填充
		'password': "",#需要填充
		'captchaData': s,
		'captchaType': 1038,
		'captchaMinLength': 0,
		'captchaMaxLength': 0,
		'workerTiosId': 0,
	}
	session = requests.session()
	res = session.post(url=url, data=json.dumps(data), timeout=10)
	while "data" not in res.json().keys():
		print('联众打码重试')
		res = session.post(url=url, data=json.dumps(data), timeout=10)
	return res.json()["data"]["recognition"]


accounts = set()
print('【胜道体育注册程序】')
r = requests.get('http://w6888.cn:9180/service.asmx/UserLoginStr?name=15372204&psw=970429')
token = r.text
for i in tqdm(range(0,1000)):
	r = requests.get('http://w6888.cn:9180/service.asmx/RjGetKsHMStr?token='+token+'&xmid=4351&sl=1&lx=0&a1=&a2=&ks=0&rj=0')
	try:
		print(r.text)
		phones = r.text.split('=')[1].split(',')
	except KeyboardInterrupt:
		exit()
	except:
		time.sleep(120)
		continue
	for phone in phones:
		print('='*50)
		print('手机号:'+phone)
		if check(phone) == 'false':
			print('手机号已经注册!')
			continue
		else:
			print('手机号未注册')
		# 胜道
		headers = {
			'Referer': 'https://sso-prod.yysports.com/register',
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
			'x-requested-with': 'XMLHttpRequest',
		}
		message = '图形验证码不正确'
		while message == '图形验证码不正确':
			response = requests.get('https://sso-prod.yysports.com/api/member/pousheng/account/captcher', headers=headers)
			base64 = response.json()['captcha_image'].split('base64,')[1]
			code = lianzhong(base64)
			captcha_token = response.json()['captcha_token']
			headers = {
				'Referer': 'https://sso-prod.yysports.com/register',
				'Origin': 'https://sso-prod.yysports.com',
				'x-requested-with': 'XMLHttpRequest',
				'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
				'Content-Type': 'application/json',
			}
			data = '{"mobile":"%s","captcha_token":"%s","captcha_answer":"%s"}'%(str(phone),captcha_token,code)
			response = requests.post('https://sso-prod.yysports.com/api/member/pousheng/account/sms-verification-code/send', headers=headers, data=str(data))
			print(response.text)
			
			if 'success' in response.json().keys():
				message = '正确'
				print('识别验证码成功,发送信息成功')
			else:
				if 'message' in response.json().keys():
					if '不合法' in response.json()['message']:
						message = '不合法'	
					else:
						print('验证码识别失败。重试')
		
		if message == '不合法':
			continue
			
		phone_message = get_message(phone)
		if phone_message == False:
			print(phone+'跳过')
			continue

		headers = {
			'Referer': 'https://sso-prod.yysports.com/register?fromType=1&response_type=code',
			'Origin': 'https://sso-prod.yysports.com',
			'x-requested-with': 'XMLHttpRequest',
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
			'Content-Type': 'application/json',
		}
		data = '{"realName":"realname","username":"%s","mobile":"%s","gender":"1","birthday":"1986-05-26","verifyCode":"%s","password":"123456","response_type":"code","fromType":"1"}'%('a'+phone,phone,phone_message)
		# data = '{"realName":"%s","username":"%s","mobile":"%s","gender":"1","birthday":"1986-05-26","verifyCode":"%s","password":"970429","response_type":"code","fromType":"1"}'%("wangdana",phone,phone,phone_message)
		response = requests.post('https://sso-prod.yysports.com/api/member/pousheng/account', headers=headers, data=data)
		accounts.add('a'+phone)
		print('a'+phone+'注册成功！')

		with open('出售'+'.txt','w') as f:
			for account in accounts:
				f.write(account+' '+'123456\n')
			f.close()