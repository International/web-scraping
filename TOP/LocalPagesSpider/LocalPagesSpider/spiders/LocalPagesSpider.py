#scrapy crawl manta -o items.json -t json
import scrapy
from scrapy import Request
from scrapy.http import TextResponse 
from scrapy.http import HtmlResponse 

import os


class LocalPagesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    phone = scrapy.Field()
    company_name = scrapy.Field()
    address = scrapy.Field()

class LocalPagesSpider(scrapy.Spider):
    name = "manta"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org"]

    def parse(self, response):
        ## File names list os.listdir(path="pages_to_scrap")
        for file in os.listdir(path="pages_to_scrap"):
            with open(os.path.join("pages_to_scrap", file)) as page:
                response = HtmlResponse(url="MyHTML", body=page.read(), encoding='utf-8')

                for info_block in response.xpath("//li[contains(@class,'list-group-item')]"):
                    item = LocalPagesItem()
                    item['company_name'] = info_block.xpath(".//div[@class='media-body']//h2/a[@itemprop='name']/strong/text()").extract_first()
                    item['phone'] = info_block.xpath(".//div[@itemprop='telephone']//text()").extract_first()
                    item['address'] = info_block.xpath(".//div[@itemprop='address']//text()").extract()
                    yield item
   
