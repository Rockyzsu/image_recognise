# -*-coding=utf-8-*-

# @Time : 2019/5/22 10:27
# @File : mark_label.py
import os
import random
import time

import requests
from shutil import move,rmtree
import config


def training(filename):

    with open(filename, 'rb') as f:
        file_content = f.read()

    try:
        start=time.time()
        r=requests.post(url=config.code_url,data=file_content)
    except Exception as e:
        print(e)
        return
    print('识别用时{}ms'.format((time.time()-start)*1000))
    try:
        ret_json = r.json()
    except Exception as e:
        print(r.text)
        print(e)
        return

    if ret_json.get('success'):

        print(ret_json)
        new_name = ret_json.get('message')
        name='{}.png'.format(new_name)

        if os.path.exists(name):
            # 文件存在
            print('文件存在')
            name='{}-{}.png'.format(new_name,random.randint(1000,9999))

        try:
            move(filename,name)
        except Exception as e:
            print(e)
        else:
            print('命名成功')
    else:
        if ret_json.get('message')=='Invalid Image Format':
            os.remove(filename)
        # print(ret_json)

def loop_file():
    for file in os.listdir('.'):
        if len(file)<=13:
            continue

        if file.endswith('png'):
            print(file)
            training(file)

loop_file()