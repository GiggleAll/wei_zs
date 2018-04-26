# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.downloadermiddlewares.redirect import RedirectMiddleware
from scrapy.exceptions import IgnoreRequest
from scrapy import Request
import logging


class WeiNumberSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class CustomRedirectMiddleware(RedirectMiddleware):
    def process_response(self, request, response, spider):
        logger = logging.getLogger('{module}.CustomRedirectMiddleware'.format(module=__name__))
        not_allowed_url = {'http://data.weibo.com/index'}
        proxy = request.meta.get('proxy', 'None')
        if request.url in not_allowed_url:
            logger.info('状态码%s,重定向到index被忽略, <Proxy %s>, url<GET %s>' % (response.status, proxy, response.url))
            raise IgnoreRequest
        else:
            code = response.status
            if code == 403:
                keys = request.meta['keys']
                group = request.meta['group']
                url = 'http://data.weibo.com/index/hotword?wid=1091324253315&wname={0}'.format(keys)
                logger.info('状态码%s, IP失效,返回重新建立Session, <Proxy %s>, current_url<GET %s>' % (code, proxy, request.url))
                return Request(url=url, meta={'cookiejar': keys, 'keys': keys, 'group': group}, callback=spider.parse,
                               dont_filter=True)
            elif code == 302:
                type_ = '重定向到crazycache'
            else:
                type_ = '请求成功'
            logger.info('状态码%s, %s, <Proxy %s>, url<GET %s>' % (code, type_, proxy, response.url))
            return response


class RandomUserAgentMiddleware(UserAgentMiddleware):
    def __init__(self, user_agent_list):
        self.user_agent_list = user_agent_list

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            user_agent_list=crawler.settings.get('USER_AGENT')
        )

    def process_request(self, request, spider):
        random_user_agent = random.choice(self.user_agent_list)
        request.headers.setdefault('User-Agent', random_user_agent)


class ProxyMiddleware(object):
    logger = logging.getLogger('{module}.ProxyMiddleware'.format(module=__name__))

    def __init__(self):
        self.proxy_list = [
            'http://127.0.0.1:80'
            # 'http://202.100.83.139:80',
            # 'http://120.92.88.202:10000',
                      ]

    def process_request(self, request, spider):
        if request.meta.has_key('proxy') and request.meta['proxy']:
            return
        random_ip = random.choice(self.proxy_list)
        request.meta['proxy'] = random_ip