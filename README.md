# shengdao-py
shengdao-py : 胜道体育非官方API库 with Python3

YySport unofficial api library with Python3


尝试解析出胜道体育官方未开放的Auth接口，并提供优雅的使用方式，目前已经不在维护

Try to analyse the Auth API which is not provided by official website, and provide elegant use, which is no longer maintained.

## To shoes lover

本库纯属本人一时兴起而产生。如将本库用于非法用途及商业行为，本人概不承担后果，请谨慎用之，愿所有爱鞋人士终得爱鞋。

This library is born by my purely intereting. If the library is used for illegal purposes and commercial activities, I will not bear the consequences, please use it with caution. Wish all shoes lovers get own shoes.


## Funtion

提供的功能一句话概括为，提供模拟登陆，查询中签或者登记商品，认证账号，和批量操作

The function provided is summarized in one sentence, providing simulated login, querying for signing or registering goods, authentication account, and batch operation.

由此引申出的4个工具，server.py,FastRegist.py,id_verify_processing.py,yysport_regist.py 分别用于快速全面服务，快速登记，id验证和批量注册账号

The four tools that were derived from this are server.py, FastRegist.py, id_verify_processing.py, and yysport_regist.py for fast full service, fast registration, id verification, and batch registration.

Simple uses:
```
from shengdao import ShengdaoClient

client = ShengdaoClient('123','123','小明')

client.id_verify('小明','123','123456')

client.search_activity()

client.search_register()

```

Result:
```

身份验证成功!

现在无活动

小明登记数量:5

AIR JORDAN 13 RETRO LOW NRG/CT 京朝阳世贸天阶胜道NK JD-YY 未中签

YEEZY BOOST 350 V2 京东城王府井中环AC 未中签

AIR JORDAN 1 RETRO HIGH OG 京朝阳世贸天阶胜道NK JD-YY 未中签

AIR JORDAN 1 RETRO HIGH OG BG 京朝阳世贸天阶胜道NK JD-YY 未中签

WMNS AIR JORDAN 1 HIGH OG NRG 京朝阳世贸天阶胜道NK JD-YY 中签


```
解析思路
https://download.csdn.net/download/m0_37694033/10878453
