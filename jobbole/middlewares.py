# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from fake_useragent import UserAgent


class JobboleUserAgentMiddleware(object):
    def __init__(self):
        self.ua = UserAgent()

    def process_request(self, request, spider):
        user_agent = self.ua.random
        request.headers.setdefault('User-Agent', user_agent)






