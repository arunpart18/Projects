#!/usr/bin/env python3

import scrapy

class MySpider(scrapy.Spider):

    name = 'myspider'

    start_urls = [
          'https://www.alloschool.com/element/43082',
    ]

    def parse(self, response):

        def extract_with_css(query):
            return response.css(query).get(default='').strip()
        yield {
          'file_urls': [extract_with_css('a.btn.btn-primary::attr(href)')],
        }


from scrapy.crawler import CrawlerProcess

c = CrawlerProcess({
    'ITEM_PIPELINES': {'scrapy.pipelines.files.FilesPipeline': 1},
    'FILES_STORE': 'D:/Arunkumar.P/01_Projects/Anaconda',
})
c.crawl(MySpider)
c.start()