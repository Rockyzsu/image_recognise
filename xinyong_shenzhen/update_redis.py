# -*-coding=utf-8-*-

# @Time : 2019/3/8 18:53
# @File : update_redis.py
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
# from keras.utils import np_utils
# from keras.models import Sequential
# from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
import pandas as pd
# from keras.models import load_model
import pymongo
from sqlalchemy import create_engine
import shutil
db = pymongo.MongoClient('10.18.6.26',27018)
doc = db['spider']['credit_sz_v4']
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
REDIS_HOST = '10.18.6.24'
r = redis.StrictRedis(host=REDIS_HOST, port=7001, decode_responses=True)
for i in doc.find({'result':'1'}):
    name=i.get('entname')
    print(r.lrem('creditsz',1,name))