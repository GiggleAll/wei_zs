# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class WeiNumberItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class WeiZSItem(scrapy.Item):
    group = Field()
    keys = Field()
    date = Field()
    value = Field()
    pc_value = Field()
    mobile_value = Field()