#scrapy crawl classifieds -o items.json -t json

import scrapy
from scrapy import Request

class ClassifiedsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    page_url = scrapy.Field()
    text = scrapy.Field()
    year = scrapy.Field()
    country = scrapy.Field()
    pass


class ClassifiedsSpider(scrapy.Spider):
    name = "classifieds"
    allowed_domains = ["classifieds.sunherald.com"]
    start_urls=["http://classifieds.sunherald.com/ms/biloxi-foreclosures/search"]

    def parse(self, response):
        for link in response.xpath("//div[@class='post-summary-title']/a/@href"):
            url = response.urljoin(link.extract())
            yield Request(url, callback=self.parse_info)
      
        #pagination
        next_page=response.xpath("//div[@class='ap_paginator']//li[contains(@class,'ap_paginator_next_page')]/a/@href")
        url = response.urljoin(next_page.extract_first())
        yield Request(url, self.parse)

    def parse_info(self, response):
        item = ClassifiedsItem()
        item['page_url'] = response.request.url
        item['text'] = response.xpath("//div[@class='details-ad-body']/text()").extract_first()
        yield item


        


