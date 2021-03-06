'''
Function:
	proxylistplus代理爬取
Author:
	Charles
微信公众号:
	Charles的皮卡丘
'''
import re
import requests


'''proxylistplus代理爬取'''
class proxylistplus():
	def __init__(self, **kwargs):
		self.info = 'proxylistplus proxy: https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-1'
		self.headers = {
						'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
					}
		self.url_list = ['https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-'+str(page) for page in range(1,2)]
	'''获取代理'''
	def get(self):
		proxies = []
		for url in self.url_list:
			try:
				res = requests.get(url, headers=self.headers)
				proxy = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?<td>(\d{1,5})</td>', res.text.replace('\n', ''))
				proxies += proxy
			except:
				pass
		proxies = list(set(proxies))
		return proxies
	'''return info'''
	def __repr__(self):
		return self.info


# for test
if __name__ == '__main__':
	print(proxylistplus().get())