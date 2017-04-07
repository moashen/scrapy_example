# -*- coding:utf-8 -*-
import scrapy
from freebuf.items import FreebufItem
import time
from scrapy.crawler import CrawlerProcess


class freebufSpider(scrapy.Spider):
    name = 'freebuf'
    allowed_domains = []

    start_urls = ["http://www.freebuf.com/"]

    def parse(self, response):
        links = response.xpath('//div[contains(@class, "news_inner news-list")]/div/a/@href').extract()
        for link in links:
            yield scrapy.Request(link, callback=self.parse_next)

        next_url = response.xpath('//div[@class="news-more"]/a/@href').extract()
        if next_url:
            yield scrapy.Request(next_url[0], callback=self.parse)

    def parse_next(self, response):
        item = FreebufItem()
        item['title'] = response.xpath('//*[@id="getWidth"]/div[1]/div/div[1]/h2/text()').extract()
        item['tags'] = response.xpath('// *[ @ id = "getWidth"] / div[1] / div / div[1] / div / span[5] / a/text()').extract()
        item['date'] = response.xpath('//*[@id="getWidth"]/div[1]/div/div[1]/div/span[3]/text()').extract()
        item['url'] = response.url
        yield item
