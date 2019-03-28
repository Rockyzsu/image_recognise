# -*-coding=utf-8-*-

# @Time : 2018/9/26 9:25
# @File : models.py

from sqlalchemy import Column, String, DateTime, Integer, Text, create_engine, DATE
from sqlalchemy.ext.declarative import declarative_base
import datetime
from sqlalchemy.orm import sessionmaker
from sandbox import config

Base = declarative_base()
engine = create_engine('mysql+pymysql://{}:{}@{}:3306/creditreport_sz?charset=utf8'.format(config.username,config.password,config.mysql_ip))
DBSession = sessionmaker(bind=engine)


# ORM 模型，根据项目需求修改
class SXRModels(Base):
    __tablename__ = 'sz_credit_spider_sx_yulan'


    # 根据项目修改字段
    id = Column(Integer, primary_key=True, autoincrement=True)
    ent_name=Column(String(300), comment='企业名称')
    case_no=Column(String(300), comment='案号')
    court = Column(String(300), comment='执行法院')
    current_state = Column(String(300), comment='履行状态')
    according_no = Column(String(500), comment='执行依据文号')
    mediation_date = Column(String(500), comment='立案时间')
    crawltime = Column(DateTime, default=datetime.datetime.now(), comment='爬取时间')

class XZCFModels(Base):
    __tablename__ = 'sz_credit_spider_xzcf_yulan'

    # 根据项目修改字段
    id = Column(Integer, primary_key=True, autoincrement=True)
    ent_name=Column(String(300), comment='企业名称')
    punish_no=Column(String(300), comment='决定书文号')
    punish_gist = Column(String(300), comment='类型')
    punish_dept = Column(String(300), comment='决定机关')
    punish_date = Column(String(500), comment='决定日期 ')
    crawltime = Column(DateTime, default=datetime.datetime.now(), comment='抓取时间')


Base.metadata.create_all(engine)