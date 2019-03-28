# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class SXRItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    ent_name=Field()
    case_no=Field()
    court = Field()
    current_state = Field()
    according_no = Field()
    mediation_date = Field()
    # crawltime = Field()

class XZCFItem(Item):
    ent_name=Field()
    punish_no=Field()
    punish_gist = Field()
    punish_dept = Field()
    punish_date = Field()
    # crawltime = Field()

