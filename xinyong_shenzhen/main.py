# -*-coding=utf-8-*-

# @Time : 2019/3/7 19:29
# @File : main.py
import datetime
import logging
import random

import redis
import requests
from PIL import Image
import os
import time
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import cv2
import re
# from sklearn.cross_validation import train_test_split
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
import pandas as pd
from keras.models import load_model
import pymongo
from sqlalchemy import create_engine
import shutil
db = pymongo.MongoClient('10.18.6.26',27018)
doc = db['spider']['credit_sz_v5']
pic_url = 'https://www.szcredit.com.cn/XY2.OutSide/WebPages/Member/CheckCode.aspx'
pic_headers = {'Host': 'www.szcredit.com.cn',
               'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36(KHTML,likeGecko)Chrome/67.0.3396.99Safari/537.36',
               'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
               'Referer': 'https://www.szcredit.com.cn/XY2.OutSide/GSPT/ShowCheckCode.aspx',
               'Accept-Encoding': 'gzip,deflate,br', 'Accept-Language': 'zh,en;q=0.9,en-US;q=0.8',

               # 'Cookie': '__jsluid=a11ca0bac7aecb2a827c4750ce0f4eea;UM_distinctid=16874b135911e6-0504ab86b1e3e3-6114147a-144000-16874b1359234b;ASP.NET_SessionId=frvl0vvxq3rdpu5w1d2ekdmh;CNZZDATA1260729719=1354580564-1548143276-%7C1551956118'
               }
info_url = 'https://www.szcredit.com.cn/XY2.OutSide/AJax/Ajax.ashx'
info_headers = {'Host': 'www.szcredit.com.cn',
                'Accept': 'application/json,text/javascript,*/*;q=0.01', 'Origin': 'https://www.szcredit.com.cn',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': 'Mozilla/5.0)AppleWebKit/537.36(KHTML,likeGecko)Chrome/67.0.3396.99Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
                'Accept-Encoding': 'gzip,deflate,br', 'Accept-Language': 'zh,en;q=0.9,en-US;q=0.8',
                }
REDIS_HOST = '10.18.6.26'
r = redis.StrictRedis(host=REDIS_HOST, decode_responses=True)
model = load_model('xinyong_shenzhen_v2.h5')


def get_proxy(retry=10):
    proxyurl = 'http://101.132.235.98:8101/dynamicIp/common/getDynamicIp.do'
    count = 0
    for i in range(retry):
        try:
            r = requests.get(proxyurl, timeout=10)
        except Exception as e:
            print(e)
            count += 1
            print('代理获取失败,重试' + str(count))
            time.sleep(1)

        else:
            js = r.json()
            proxyServer = 'http://{0}:{1}'.format(js.get('ip'), js.get('port'))
            proxies_random = {
                'http': proxyServer
            }
            return proxies_random

    return None

def llogger(filename):
    logger = logging.getLogger(filename)  # 不加名称设置root logger
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '[%(asctime)s][%(filename)s][line: %(lineno)d]\[%(levelname)s] ## %(message)s)',
        datefmt='%Y-%m-%d %H:%M:%S')
    # 使用FileHandler输出到文件
    prefix = os.path.splitext(filename)[0]
    fh = logging.FileHandler(prefix + '.log')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    # 使用StreamHandler输出到屏幕
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    # 添加两个Handler
    logger.addHandler(ch)
    logger.addHandler(fh)
    # logger.info('this is info message')
    # logger.warning('this is warn message')
    return logger

logger = llogger('xinyong_shenzhen_{}'.format(datetime.date.today()))


# 识别
def get_code(filename):
    im = cv2.imread(filename)
    g_im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    ret2, th2 = cv2.threshold(g_im, 200, 255, cv2.THRESH_BINARY)
    (new_img, contours, hiera) = cv2.findContours(th2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    result = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if h > 5 and w < 60 and w > 4:
            box = np.int0([[x, y], [x + w, y], [x + w, y + h], [x, y + h]])
            result.append(box)

    result_img = []
    result = sorted(result, key=lambda x: x[0][0])
    for index, box in enumerate(result):
        roi = th2[:, box[0][0]:box[1][0]]

        new_i = cv2.resize(roi, (20, 30))
        ret, new_i = cv2.threshold(new_i, 1, 255, cv2.THRESH_BINARY_INV)
        #     new_i =cv2.resize(new_i,(15,30))
        #     plt.figure(figsize=(10,10))
        try:
            result_img.append(new_i)
            # plt.subplot(1, l, index + 1)
            # plt.imshow(new_i)
        except Exception as e:
            print('error')

    map_dict = {}
    for i in range(10):
        map_dict[str(i)] = i

    map_dict['d'] = 10
    map_dict['j'] = 11
    map_dict['m'] = 12
    map_dict['w'] = 13

    dict_reverse = {0: '0',
                    1: '1',
                    2: '2',
                    3: '3',
                    4: '4',
                    5: '5',
                    6: '6',
                    7: '7',
                    8: '8',
                    9: '9',
                    10: 'd',
                    11: 'j',
                    12: 'm',
                    13: 'w'}

    dict_reverse[11] = '+'
    dict_reverse[12] = '*'

    real_data = np.array(result_img)
    X_real = real_data.reshape(real_data.shape[0], 30, 20, 1).astype('float32')
    X_real_norm = X_real / 255
    ret = model.predict_classes(X_real_norm)

    result_str = []
    for i in ret:
        if i == 10 or i == 13:
            continue
        else:
            result_str.append(dict_reverse.get(i, ''))

    r = ''.join(result_str)
    try:
        calc_ret = eval(r)
    except Exception as e:
        logger.error('运算出错')
        logger.error(r)
        logger.error('>>>{}'.format(filename))
        logger.error(e)
        return 0
    else:
        logger.info('计算结果{}'.format(calc_ret))
        return calc_ret

def get_enterprise_info(name):
    session = requests.Session()
    proxy = get_proxy()
    s1 = session.get(pic_url, headers=pic_headers,proxies=proxy)
    filename = 'test.png'
    with open(filename, 'wb') as f:
        f.write(s1.content)

    code = get_code(filename)
    ent_name = name
    post_data = {
        'action': 'GetEntList',
        'keyword': ent_name,
        'type': 'load',
        'ckfull': 'false',
        'yzmResult': code,
        'source': ''
    }


    proxy2=get_proxy()
    s2=session.post(url=info_url,headers=info_headers,data=post_data,proxies=proxy2)

    js_data=s2.json()
    content = js_data.get('msg')

    if '计算错误' in content:
        random_str =datetime.datetime.now().strftime('%Y%m%d%H%M%S')+str(random.randint(10000,99999))
        logger.error('计算出错 >>>> {}.png'.format(random_str))
        try:
            shutil.copy(filename,'{}.png'.format(random_str))
        except Exception as e:
            logger.error('copy file errorr')
        finally:
            # r = {'entname': name, 'result': '-1','crawltime':datetime.datetime.now()}
            doc.update({'entname':name},{'$set':{'result':'-1','crawltime':datetime.datetime.now()}})
            session.close()
            return None


    if '未查询到该企业的信息' in content:
        r={'entname':name,'result':'0','crawltime':datetime.datetime.now()}
        doc.update({'entname':name},{'$set':{'result':'0','crawltime':datetime.datetime.now()}})
    else:
        doc.update({'entname':name},{'$set':{'result':'1','resultlist':js_data.get('resultlist'),'crawltime':datetime.datetime.now()}})

    session.close()

def get_ent_name():

    mongo_ret1 = doc.find({'result':'1'})
    mongo_ret2 = doc.find({'result':'0'})
    crawl_name = []

    for item in mongo_ret1:
        crawl_name.append(item.get('entname'))
    for item in mongo_ret2:
        crawl_name.append(item.get('entname'))
    while 1:
        name = r.lpop('credit_sz_yunlan')
        if not name:
            break
        if doc.find({'entname':name,'result':'1'}):
            if name not in crawl_name:
                get_enterprise_info(name)


def get_ent_name_failed():

    # mongo_ret1 = doc.find({'result':'1'})
    # mongo_ret2 = doc.find({'result':'0'})
    # crawl_name = []

    # for item in mongo_ret1:
    #     crawl_name.append(item.get('entname'))
    # for item in mongo_ret2:
    #     crawl_name.append(item.get('entname'))
    # while 1:
    #     name = r.lpop('credit_sz_yunlan')
    #     if not name:
    #         break
    #     if doc.find({'entname':name,'result':'1'}):
    #         if name not in crawl_name:
    failed = doc.find({'result':'-1'})
    for item in failed:
        name = item.get('entname')
        get_enterprise_info(name)

def upload_redis():
    user = 'yzplatform'
    password = 'yzplatform'
    host = '10.18.6.105'
    port = 3306
    db = 'creditreport_sz'
    engine = create_engine(
        'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(user, password, host, port, db))
    df = pd.read_sql('sz_enterprise_name', con=engine)
    name_list = list(set(list(df['entname'].values)))


    for i in name_list:
        r.lpush('creditsz',i)

if __name__ == '__main__':
    # get_ent_name()
    get_ent_name_failed()
    # upload_redis()