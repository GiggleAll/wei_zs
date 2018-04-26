# -*- coding: utf-8 -*-
import scrapy


class TestSpider(scrapy.Spider):
    name = 'test'
    # allowed_domains = ['http://blog.jobbole.com/all-posts/']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        pass
