from shengdao import ShengdaoClient
import requests
import json
import xlrd,xlwt

id_file_path = input("输入证件文件完整路径：")  
id_file = xlrd.open_workbook(id_file_path)
names = id_file.sheets()[0].col_values(0)
ids = id_file.sheets()[0].col_values(1)

account_file_path = input("输入账号文件完整路径：")  
account_file = open(account_file_path)

shengdaolist = []
idlist = []
successlist = []

workbook = xlwt.Workbook(encoding = 'ascii')
worksheet = workbook.add_sheet('My Worksheet')

# import IPython
# IPython.embed()
for line in account_file:
    if '已知信息' in line:
        break
    items = line.strip().split(' ')
    shengdaolist.append({'userid':items[0],'password':items[1]})

count = 0
for i in range(0,len(shengdaolist)-1):
    client = ShengdaoClient(shengdaolist[i]['userid'],shengdaolist[i]['password'])
    status = client.id_verify(names[i],ids[i],shengdaolist[i]['userid'][1:])
    if status == 1:
        worksheet.write(count, 0, names[i])
        worksheet.write(count, 1, ids[i])
        worksheet.write(count, 2, shengdaolist[i]['userid'])
        worksheet.write(count, 3, shengdaolist[i]['password'])
        count += 1

workbook.save('accounts.xls')


