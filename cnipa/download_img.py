# -*-coding=utf-8-*-

# @Time : 2019/5/21 10:12
# @File : download_img.py
import requests
import time
import random
import os
os.chdir('data')
MAX_COUNT = 3000
start = 0
headers={
"Accept":"image/webp,image/apng,image/*,*/*;q=0.8",
"Accept-Encoding":"gzip, deflate",
"Accept-Language":"zh,en;q=0.9,en-US;q=0.8,zh-CN;q=0.7",
"Cache-Control":"no-cache",
"Connection":"keep-alive",
"Cookie":"IS_LOGIN=false; WEE_SID=AATYIgt_C9Tuu2GgKAFz20HON3CnShjARTlGnnD4LVosN8L9fhdS!-1627000008!275829341!1558404270975; JSESSIONID=AATYIgt_C9Tuu2GgKAFz20HON3CnShjARTlGnnD4LVosN8L9fhdS!-1627000008!275829341",
"Host":"pss-system.cnipa.gov.cn",
"Pragma":"no-cache",
"Referer":"http://pss-system.cnipa.gov.cn/sipopublicsearch/portal/uilogin-forwardLogin.shtml",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
}
while start<MAX_COUNT:

    try:
        r = requests.get(url='http://pss-system.cnipa.gov.cn/sipopublicsearch/portal/login-showPic.shtml',headers=headers)
    except Exception as e:
        print(e)
        continue
    else:
        with open('{}-{}.jpg'.format(str(int(time.time()*1000)),random.randint(1000,9999)),'wb') as f:
            f.write(r.content)

        start+=1