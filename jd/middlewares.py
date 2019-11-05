# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals, Request
import time
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options



class SeleniumDownloaderMiddleware(object):
    def __init__(self):
        self.browser_options = Options()
        self.browser_options.add_argument('-headless')
        self.browser = webdriver.Chrome(options=self.browser_options)

    def process_request(self, request, spider):
        self.browser.get(request.url)
        self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(3)
        self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(3)
        return HtmlResponse(url=request.url, request=request, encoding='utf-8', body=self.browser.page_source,
                            status=200, )



    def __del__(self):
        self.browser.close()
