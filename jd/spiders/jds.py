# -*- coding: utf-8 -*-
import math
import re
import scrapy
from jd.items import JdItem
from urllib.parse import quote




class JdsSpider(scrapy.Spider):
    name = 'jds'
    allowed_domains = ['jd.com']


    def start_requests(self):
        for thing in self.settings.get('THING'):
            a = 'https://search.jd.com/Search?keyword='
            b = quote(thing)
            c = '&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=shou&page=1&s=1&click=0'
            url = a + b + c
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        max = self.settings.get('MAX_PAGE')
        projects = response.xpath('//*[@id="J_goodsList"]/ul/li')
        print(projects)
        for project in projects:
            item = JdItem()
            item['title'] = project.xpath('./div/div[4]/a/em/text()').getall()
            if item['title'] == []:
                item['title'] = project.xpath('./div/div[3]/a/em/text()').getall()
            item['price'] = project.xpath('./div/div[3]/strong/i/text()').get()
            if item['price'] == None:
                item['price'] = project.xpath('./div/div[2]/strong/i/text()').get()
            item['picture'] = project.xpath('./div/div[1]/a/img/@data-lazy-img').get()
            print(item)
        url = response.url
        a = int(re.search(r'page=(\d+)', url).group(1)) + 2
        b = re.sub((r'page=(\d+)'), 'page=' + str(a), url)
        c = int(re.search(r's=(\d+)', url).group(1)) + 60
        d = re.sub((r's=(\d+)'), 's=' + str(c), b)
        a = a/2
        if math.ceil(a) < max+1:
            yield scrapy.Request(
                url=d,
                callback=self.parse
            )










