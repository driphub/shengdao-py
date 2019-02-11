import requests
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import time

def run(subject,filename):
	try:
		from_addr = '872490934@qq.com'
		password = 'ultyrlpfwaqdbddd'
		# 输入SMTP服务器地址:
		smtp_server = 'smtp.qq.com'
		# 输入收件人地址:

		server = smtplib.SMTP(smtp_server, 25) # SMTP协议默认端口是25
		# server.set_debuglevel(1)  这是输出日志

		sender = '872490934@qq.com'
		receivers = ['872490934@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
		
		message = MIMEMultipart()
		message['From'] = Header("shengdao-py", 'utf-8')   # 发送者
		message['To'] =  Header("shengdao", 'utf-8')        # 接收者
		
		message['Subject'] = Header(subject, 'utf-8')

		part = MIMEApplication(open(filename,'rb').read())
		part.add_header('Content-Disposition', 'attachment', filename=filename)
		message.attach(part) 
		
		server.login(from_addr, password)
		server.sendmail(from_addr, receivers, message.as_string())
		server.quit()
	except:
		pass
