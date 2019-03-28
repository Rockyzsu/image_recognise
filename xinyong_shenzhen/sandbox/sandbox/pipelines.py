# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sandbox.models import SXRModels,XZCFModels, DBSession
import logging
import pymongo
from sandbox import config
from sandbox import settings
from sandbox.items import SXRItem,XZCFItem
from sqlalchemy import func,or_,not_,and_
class SQLPipeline(object):
    def __init__(self):
        self.session = DBSession()

    def process_item(self, item, spider):
        if isinstance(item,SXRItem):
            try:
                is_exist = self.session.query(SXRModels).filter(and_(SXRModels.ent_name == item['ent_name'],SXRModels.case_no == item['case_no'])).first()
            except Exception as e:
                print(e)
                self.session =DBSession()
                is_exist = self.session.query(SXRModels).filter(and_(SXRModels.ent_name == item['ent_name'],SXRModels.case_no == item['case_no'])).first()
            print('查看是否已存在库里 >>>',item['ent_name'])
            if not is_exist:

                obj = SXRModels(
                ent_name=item['ent_name'],
                case_no = item['case_no'],
                court = item['court'],
                current_state = item['current_state'],
                according_no = item['according_no'],
                mediation_date = item['mediation_date'],
                )
                self.session.add(obj)

                try:
                    self.session.commit()

                except Exception as e:
                    logging.error('>>>> 插入数据库失败{}'.format(e))
                # return item
                else:
                    print('插入失信人数据成功 >>>> {}'.format(item['ent_name']))

        if isinstance(item,XZCFItem):
            try:
                is_exist_ = self.session.query(XZCFModels).filter(and_(XZCFModels.ent_name == item['ent_name'],XZCFModels.punish_gist == item['punish_gist'])).first()
            except Exception as e:
                self.session=DBSession()
                is_exist_ = self.session.query(XZCFModels).filter(and_(XZCFModels.ent_name == item['ent_name'],XZCFModels.punish_gist == item['punish_gist'])).first()

            print('查看是否已存在库里 >>>',item['ent_name'])

            if not is_exist_:
                obj = XZCFModels(
                ent_name=item['ent_name'],
                punish_no=item['punish_no'],
                punish_gist=item['punish_gist'],
                punish_dept=item['punish_dept'],
                punish_date=item['punish_date'],
            )
                self.session.add(obj)

                try:
                    self.session.commit()

                except Exception as e:
                    logging.error('>>>> 插入数据库失败{}'.format(e))
                # return item
                else:
                    print('插入行政处罚数据成功 >>>> {}'.format(item['ent_name']))

