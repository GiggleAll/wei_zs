# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from scrapy.conf import settings
import pymongo
from pymongo.errors import ServerSelectionTimeoutError
import logging

path = '/home/hjliang/tmp/data/wzs.json'


class WeiZSPipeline(object):
    def process_item(self, item, spider):
        json_data = json.dumps(dict(item))
        with open(path, 'a') as fl:
            fl.write("{0}\n".format(json_data))
        return item


class SaveMongoPipeline(object):
    def __init__(self):
        ms_host = settings['MS_MONGODB_HOST']
        sa_host = settings['SA_MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbname = settings['MONGODB_DBNAME']  # 数据库名
        try:
            client = pymongo.MongoClient(host=ms_host, port=port)
        except ServerSelectionTimeoutError:
            client = pymongo.MongoClient(host=sa_host, port=port)
        tdb = client[dbname]
        self.port = tdb[settings['MONGODB_DOCNAME']]  # 表名

    def process_item(self, item, spider):
        agentinfo = dict(item)
        self.port.update_one(agentinfo, {"$set": agentinfo}, upsert=True)
        return item
