# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from ..items import WeiZSItem
import json
import os
import logging


class WeizsSpider(scrapy.Spider):
    name = 'weizs'
    allowed_domains = ['data.weibo.com']
    logger = logging.getLogger(__name__)

    def start_requests(self):
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'source/keys.csv')
        for index, line in enumerate(open(path, 'r')):
            data = line.split(',')
            group = data[0].strip()
            keys = data[1].strip('\n').lower()
            url = 'http://data.weibo.com/index/hotword?wid=1091324253315&wname={0}'.format(keys)
            yield Request(url=url, meta={'cookiejar': keys, 'keys': keys, 'group': group},
                          callback=self.parse, dont_filter=True)

    def parse(self, response):
        url = 'http://data.weibo.com/index/ajax/getchartdata?month=default&__rnd=1521119820675'
        cookie_id = response.meta['cookiejar']
        keys = response.meta['keys']
        group = response.meta['group']
        yield Request(url=url, callback=self.detail_page,
                      meta={'keys': keys, 'group': group, 'cookiejar': cookie_id, 'proxy': response.meta.get('proxy')}, dont_filter=True)

    def detail_page(self, response):
        message = json.loads(response.text)
        yd_data_groups = message['data'][0]['yd']
        keyword = response.meta['keys']
        try:
            keywords = message['keyword'][0].encode('utf-8')
        except Exception:
            keywords = None
        if keywords and keyword != keywords:
            self.logger.warning('关键词匹配错误, <From meta %s> <From data %s>' % (keyword, keywords))
        if isinstance(yd_data_groups, bool):
            self.logger.warning('非高匿代理,被反爬, <name %s> <Proxy %s> <GET %s>' % (response.meta['keys'], response.meta.get('proxy', 'None'), response.url))
            return None
        items = []
        for data in yd_data_groups:
            weizs_item = WeiZSItem()
            weizs_item['group'] = response.meta['group']
            weizs_item['keys'] = keyword
            weizs_item['date'] = data.get('daykey', '')
            pc = int(data.get('pc', ''))
            mobile = int(data.get('mobile', ''))
            weizs_item['pc_value'] = pc  # int
            weizs_item['mobile_value'] = mobile
            weizs_item['value'] = pc + mobile
            items.append(weizs_item)
        self.logger.info('<{0}>写入item数据, url<GET {1}>'.format(keyword, response.url))
        return items
