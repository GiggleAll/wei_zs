# -*- encoding: utf-8 -*-

from scrapy.cmdline import execute
import sys
import os
sys.path.append(os.path.dirname(__file__))
execute(['scrapy', 'crawl', 'weizs'])
# execute(['scrapy', 'crawl', 'test'])


