# -*- coding: utf-8 -*-

import scrapy
from scrapy.settings import Settings


class DownloadSpider(scrapy.Spider):
    name = 'download'
    #allowed_domains = ['http://sysveda.co.in/']
    start_urls = ['https://www.researchgate.net/publication/312442303_An_Introduction_to_Deep_Learning']

    def parse(self, response):

        def extract_with_css(query):
            return response.css(query).get(default='').strip()
        yield {
          'file_urls': ['https://www.researchgate.net/profile/Sylvain_Chevallier/publication/312442303_An_Introduction_to_Deep_Learning/links/5c41f922299bf12be3d194a0/An-Introduction-to-Deep-Learning.pdf'],
        } 