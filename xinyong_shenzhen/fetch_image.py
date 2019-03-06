# -*-coding=utf-8-*-

# @Time : 2019/3/6 0:16
# @File : fetch_image.py
import requests

url = 'https://www.szcredit.com.cn/XY2.OutSide/WebPages/Member/CheckCode.aspx'
import os
os.chdir('image_data')
headers={
'Accept':'image/webp,image/apng,image/*,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
'Cache-Control':'no-cache',
'Connection':'keep-alive',
'Cookie':'ASP.NET_SessionId=3nc0c0blg5x5pykoshxo2jqo; __jsluid=c6c5a8658c48cac9cc1e6e59e2a59ff5; UM_distinctid=1694d46d47342-0a925b5900efb4-414e0e2a-1fa400-1694d46d4745a0; CNZZDATA1260729719=1561997532-1551776692-%7C1551776692',
'Host':'www.szcredit.com.cn',
'Pragma':'no-cache',
'Referer':'https://www.szcredit.com.cn/XY2.OutSide/GSPT/ShowCheckCode.aspx',
'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
}
for _ in range(5):
    try:
        r = requests.get(url,headers=headers)
    except Exception as e:
        print(e)

    else:
        with open('{}.jpg'.format(_),'wb') as f:
            f.write(r.content)