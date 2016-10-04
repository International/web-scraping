#scrapy crawl manta -o items.json -t json


import scrapy
from scrapy import Request
from scrapy.http import TextResponse 
from scrapy.http import HtmlResponse 

from scrapy.selector import Selector

import os


class MantaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    phone = scrapy.Field()
    company_name = scrapy.Field()
    address = scrapy.Field()


class MantaSpider(scrapy.Spider):
    name = "manta"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org"]
 
    '''
    manta.com using http://www.distilnetworks.com firewall 
    that detects selenium and scrapy.
    '''

    def parse(self, response):
        #Scrapping local html page
        files = os.listdir(path="spiders\pages")
        for file in files:
            with open(os.path.join(os.getcwd(),"spiders","pages", file)) as page:
                page_content = page.read()
                response = HtmlResponse(url="MyHTML", body=page_content, encoding='utf-8')
                item = MantaItem()

                for info_block in response.xpath("//li[contains(@class,'list-group-item')]"):
                    if info_block.xpath(".//div[@class='media-body']//h2/a[@itemprop='name']/strong/text()"):
                        item['company_name'] = (info_block.xpath(".//div[@class='media-body']//h2/a[@itemprop='name']/strong/text()").extract_first()).strip()
                    if info_block.xpath(".//div[@itemprop='telephone']//text()"):
                        item['phone'] = (info_block.xpath(".//div[@itemprop='telephone']//text()").extract_first()).strip()
                    if info_block.xpath(".//div[@itemprop='address']//text()"):
                        item['address'] = ' '.join([address.strip() for address in info_block.xpath(".//div[@itemprop='address']//text()").extract()]) 
                    yield item
   
