# -*- coding: utf-8 -*-
import scrapy,csv
from scrapy.crawler import CrawlerProcess
from scrapy import *
from selenium import webdriver

class DynaSpider(scrapy.Spider):
    name = 'dyna'
    allowed_domains = ['https://www.moneycontrol.com/']
    start_urls = ['https://www.moneycontrol.com/techmvc/ajaxcontent/latest_news/mc_homepage/english']
    custom_settings = {
    'FEED_FORMAT': 'csv',
    'FEED_URI' : 'NewsFeed.csv'
        }
    def parse(self, response):
      strA='A'
      for base in response.css("ul li"):
            if strA =='A':
                yield({'News':'\nLATEST NEWS','RSS_Link':''})
                strA='B'
            for data in base.css("a"):
                yield({'News': data.css('::attr(title)').extract()[0].replace(",", " " ).strip(), 'RSS_Link': data.css('::attr(href)').extract()[0].strip()})
                #strA = 'B'            
      
class DownloadSpider(scrapy.Spider):
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



class WebpageSpider(scrapy.Spider):
    name = 'static'
    #allowed_domains = ['www.moneycontrol.com']
    start_urls = ['https://www.moneycontrol.com/india/stockpricequote/refineries/relianceindustries/RI']

    def parse(self, response):
        file_name = open('StockInfo.csv', 'w' ,newline='')
        fieldnames = ['Stockinfo','Value'] 
        writer = csv.DictWriter(file_name, fieldnames=fieldnames)
        writer.writeheader()
        #strA =""
        for base in response.css('.pcstname, .bsns_pcst'):
            writer.writerow({'Stockinfo':base.css('::text').extract(),'Value':''})
        writer.writerow({'Stockinfo':'Initial & closing Stock Price','Value':''})
        for base in response.css('.open_lhs1 li'):    
            writer.writerow({'Stockinfo':base.xpath('p[1]/text()').get(),'Value':base.xpath('p[2]/text()').get()})
        writer.writerow({'Stockinfo':'Current Stock Price','Value':''})
        for base in response.css('.open_lhs2 li'): 
            writer.writerow({'Stockinfo':base.xpath('normalize-space(p[1]/text())').get(),'Value':base.xpath('p[2]/text()').get()})   

class AngularSpider(scrapy.Spider):
    name = 'angular_spider'
    start_urls = [
        'http://sysveda.co.in/#/solutions/capital-market'
    ]    
    # Initalize the webdriver    
    def __init__(self):
        self.driver = webdriver.Chrome('D:/Arunkumar.P/09_Applications/chromedriver_win32/chromedriver.exe')

    
    # Parse through each Start URLs
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)    
    

   # Parse function: Scrape the webpage and store it
    def parse(self, response):
        self.driver.get('http://sysveda.co.in/#/about-us/company-profile')
        # Output filename
        filename = "angular_data.csv"
        with open(filename, 'a+') as f:
            writer = csv.writer(f)
            # Selector for all the names from the link with class 'ng-binding'
            names = self.driver.find_elements_by_css_selector(".col-md-6 ul li")
            for name in names:
                title = name.text
                writer.writerow([title])
        self.log('Saved file %s' % filename)



c = CrawlerProcess({
    'ITEM_PIPELINES': {'scrapy.pipelines.files.FilesPipeline': 1},
    'FILES_STORE': 'D:/Arunkumar.P/01_Projects/Anaconda',
})
c.crawl(WebpageSpider)
c.crawl(DynaSpider)
c.crawl(DownloadSpider)
c.crawl(AngularSpider)
c.start()