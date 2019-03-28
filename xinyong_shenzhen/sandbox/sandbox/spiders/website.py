# -*- coding: utf-8 -*-
import json
import pymongo
import re
import scrapy
from scrapy import Request, FormRequest
import logging
import redis
from sqlalchemy import create_engine
import pandas as pd
from sandbox.items import SXRItem,XZCFItem
from sandbox.utility import get_header


# get
class WebGetSpider(scrapy.Spider):
    name = 'website1'
    # headers = {
    #     "User-Agent": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko)",
    # }
    URL = 'https://www.szcredit.com.cn/xy2.outside/gspt/newGSPTDetail3.aspx?ID={}'

    def __init__(self):

        super(WebGetSpider, self).__init__()
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip,deflate,br', 'Accept-Language': 'zh,en;q=0.9,en-US;q=0.8',
            'Cache-Control': 'no-cache', 'Connection': 'keep-alive',
            # 'Cookie': '__jsluid=a11ca0bac7aecb2a827c4750ce0f4eea;UM_distinctid=16874b135911e6-0504ab86b1e3e3-6114147a-144000-16874b1359234b;ASP.NET_SessionId=frvl0vvxq3rdpu5w1d2ekdmh;CNZZDATA1260729719=1354580564-1548143276-%7C1552008357',
            'Host': 'www.szcredit.com.cn', 'Pragma': 'no-cache', 'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0(;WOW64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/67.0.3396.99Safari/537.36'
        }
        self.db=pymongo.MongoClient('10.18.6.26',27018)
        user = '********'
        password = '********'
        host = '10.18.6.105'
        port = 3306
        db = 'creditreport_sz'
        engine = create_engine(
            'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(user, password, host, port, db))
        # df = pd.read_sql('sz_credit_spider_sx', con=engine)
        # self.name_list = list(set(list(df['ent_name'].values)))
        # self.r = redis.StrictRedis('10.18.6.26', decode_responses=True)

        self.record_ent = self.db['spider']['credit_sz_no_info']
        

    def start_requests(self):
        # TO DO
        ent_info = self.db['spider']['credit_sz_v5'].find({'result':'1'})
        crawl_ent = self.record_ent.find({})
        crawl_ent_list = []
        
        for c_ent in crawl_ent:
            crawl_ent_list.append(c_ent.get('ent_name'))
            
        for each_item in ent_info:
            for sub_item in each_item.get('resultlist'):
                # print(sub_item)
                rec_id = sub_item.get('RecordID')
                # name=sub_item.get('EntName')
                ent_name=each_item.get('entname')
                # if (ent_name not in self.name_list) and (ent_name not in crawl_ent_list):
                    # print(ent_name)
                yield Request(url=self.URL.format(rec_id),
                      headers=self.headers,
                              meta={'name':ent_name}
                      )

    def parse(self, response):
        # logging.info(response.text)
        # logging.info('pass')
        # ret_data = json.loads(response.body_as_unicode())
        content = response.text
        ent_name=response.meta['name']

        if '最高法院失信被执行人名单' in content:

            case_no = response.xpath('//td[contains(text(),"执行案号")]/following-sibling::*[1]/text()').extract_first()
            court = response.xpath('//td[contains(text(),"执行法院")]/following-sibling::*[1]/text()').extract_first()
            current_state = response.xpath('//td[contains(text(),"当前状态")]/following-sibling::*[1]/text()').extract_first()
            according_no=''
            mediation_date=''

            sxrItem = SXRItem()

            for field in sxrItem.fields:
                try:
                    sxrItem[field] = eval(field)
                except Exception as e:
                    logging.warning('can not find define of {}'.format(field))
                    logging.warning(e)

            yield sxrItem

        if '市场监管行政处罚信息' in content:
            xzcfItem = XZCFItem()
            punish_no = response.xpath('//td[contains(text(),"处罚文号")]/following-sibling::*[1]/text()').extract_first()
            punish_gist = response.xpath('//td[contains(text(),"处罚依据")]/following-sibling::*[1]/text()').extract_first()
            punish_dept = ''
            punish_date = response.xpath('//td[contains(text(),"处罚日期")]/following-sibling::*[1]/text()').extract_first()

            for field in xzcfItem.fields:
                try:
                    xzcfItem[field] = eval(field)
                except Exception as e:
                    logging.warning('can not find define of {}'.format(field))
                    logging.warning(e)

            yield xzcfItem

        if ('最高法院失信被执行人名单' not in content) and ('市场监管行政处罚信息' not in content):
            # 无数据的企业
            self.record_ent.update({'ent_name':ent_name},{'$set':{'ent_name':ent_name}},True,False)
# post
class WebPostSpider(scrapy.Spider):
    name = 'website2'
    headers = {
        "Host": "cha.zfzj.cn",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko)",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "https://cha.zfzj.cn/mainPage.html",
    }
    post_url = 'https://cha.zfzj.cn/bankCardDetail/select'

    def start_requests(self):
        # TO DO
        URL = 'https://cha.zfzj.cn/'
        yield Request(url=URL, callback=self.query)

    def query(self, response):
        # TO DO
        rds = redis.StrictRedis('10.18.6.102', db=7, decode_responses=True)

        data = {
            "limit": "500",
            "offset": '1',
            "sortOrder": "asc",
            "inputValue": '',
        }

        while 1:
            card = rds.lpop('cardbin0925')
            if not card:
                break
            logging.info('query card >>>> {}'.format(card))
            data['inputValue'] = card
            yield FormRequest(url=self.post_url, formdata=data, headers=self.headers, callback=self.parse,
                              meta={'card': card, 'page': 1})

    def parse(self, response):
        # logging.info(response.text)
        # logging.info('pass')
        ret_data = json.loads(response.body_as_unicode())
        card = response.meta['card']
        rows = ret_data['rows']

        if not rows:
            return

        for row in rows:
            accountLength = row['accountLength']
            cardName = row['cardName']
            cardType = row['cardType']
            mainAccount = row['mainAccount']
            mainValue = row['mainValue']
            orgName = row['orgName']

            spiderItem = SpiderItem()

            for field in spiderItem.fields:
                try:
                    spiderItem[field] = eval(field)
                except Exception as e:
                    logging.warning('can not find define of {}'.format(field))
                    logging.warning(e)

            yield spiderItem

        total = ret_data['total']
        pages = int(total / 500) if total % 500 == 0 else int(total / 500) + 1
        current_page = response.meta['page']
        if pages > current_page:
            current_page += 1
            data = {
                "limit": "500",
                "offset": str(current_page),
                "sortOrder": "asc",
                "inputValue": card,
            }
            yield FormRequest(url=self.post_url, headers=self.headers, formdata=data,
                              meta={'page': current_page, 'card': card})
