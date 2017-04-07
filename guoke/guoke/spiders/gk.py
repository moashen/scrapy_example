# -*- coding: utf-8 -*-
import scrapy
from guoke.items import GuokeItem

class GkSpider(scrapy.Spider):
    name = "gk"
    allowed_domains = ["guokr.com"]
    start_urls = ['http://www.guokr.com/scientific/']

    def parse(self, response):
        
        # item = GuokeItem()
        # item['title'] = response.xpath('//*[@id="waterfall"]/div[1]/h3/a/text()').extract()
        # //*[@id="waterfall"]/div[2]/h3/a
        # return item
        
        articles =  response.xpath('//*[@id="waterfall"]/div')
        for article in articles:
            # print(article)
            item = GuokeItem()
            item['title'] = article.xpath('h3/a/text()').extract()
            item['author'] = article.xpath('div/a[1]/text()').extract()
            item['summary'] = article.xpath('p/text()').extract()
            item['link'] = article.xpath('h3/a/@href').extract()
            yield item
