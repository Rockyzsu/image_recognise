# -*-coding=utf-8-*-

# @Time : 2019/1/30 15:15
# @File : fetch_image.py
import requests

PHOTO_NUM = 5000
headers={'User-Agent':'IQIYI QQ Android'}
def download(count):
    url ='http://www.qhcredit.gov.cn//servlet/validateCodeServlet'
    try:
        r = requests.get(url=url,headers=headers)
    except Exception as e:
        print(e)
        return False

    else:
        with open('{}.jpg'.format(count),'wb') as f:
            f.write(r.content)
        return True

import os
os.chdir('data')
for i in range(1,PHOTO_NUM):
    download(i)