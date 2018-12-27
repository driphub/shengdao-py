# shengdao-py
shengdao-py : 胜道体育非官方API库 with Python3

尝试解析出胜道体育官方未开放的Auth接口，并提供优雅的使用方式，目前还在开发阶段

## 功能
由于胜道体育没有公开API，加上受到zhihu-python项目的启发，在Python3下重新写了一个胜道体育的数据解析模块。

提供的功能一句话概括为，提供模拟登陆，查询中签或者登记数据，登记商品，和批量操作

示例代码:
```
import shengdao.ShengdaoClient

client = ShengdaoClient('123','123','小明')

client.search_activity()

client.search_register()
```

返回:
```
现在无活动

小明登记数量:5

AIR JORDAN 13 RETRO LOW NRG/CT 京朝阳世贸天阶胜道NK JD-YY 未中签

YEEZY BOOST 350 V2 京东城王府井中环AC 未中签

AIR JORDAN 1 RETRO HIGH OG 京朝阳世贸天阶胜道NK JD-YY 未中签

AIR JORDAN 1 RETRO HIGH OG BG 京朝阳世贸天阶胜道NK JD-YY 未中签

WMNS AIR JORDAN 1 HIGH OG NRG 京朝阳世贸天阶胜道NK JD-YY 未中签
```
解析思路
https://download.csdn.net/download/m0_37694033/10878453
