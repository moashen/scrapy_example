# -*- coding: utf-8 -*-
import scrapy
from meizitu.items import MeizituItem
# import time
# from scrapy.crawler import CrawlerProcess


class MzituSpider(scrapy.Spider):
    name = "mzitu"
    allowed_domains = []

    start_urls = ['http://www.mzitu.com/']

    def parse(self, response):
        links = response.xpath('//li/span[1]/a/@href').extract()
        for link in links:
            yield scrapy.Request(link, callback=self.parse_next)

        next_url = response.xpath('//a[@class="next page-numbers"]/@href').extract()
        if next_url:
            yield scrapy.Request(next_url[0], callback=self.parse)

    def parse_next(self, response):

        item = MeizituItem()
        item['name'] = response.xpath('/html/body/div[2]/div[1]/div[3]/p/a/img/@alt').extract()[0]
        item['img_url'] = response.xpath('/html/body/div[2]/div[1]/div[3]/p/a/img/@src').extract()
        yield item

        # max_page = response.xpath('//div[@divclass="pagenavi"]/a/text()')[-2].extract()
        next_page = response.xpath('/html/body/div[2]/div[1]/div[4]/a/@href').extract()[-1]
        maxp = next_page.split('/')[-1]
        print(maxp)
        # now_page = response.url.split('/')[-1]

        if int(maxp) < 500:
            yield scrapy.Request(next_page, callback=self.parse_next)
