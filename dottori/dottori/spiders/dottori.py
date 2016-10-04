#scrapy crawl dottori -o items.json -t json


import scrapy
from scrapy import Request

class DottoriItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    link = scrapy.Field()
    name = scrapy.Field()


class DottoriSpider(scrapy.Spider):
    name = "dottori"
    allowed_domains = ["dottori.it"]
    start_urls = [
        "https://www.dottori.it/medici"
    ]


    def parse(self, response):
        for link in response.xpath("//li[contains(@class,'list-group-item')]//a[@class='docResultLink']/@href"):
            url = response.urljoin(link.extract())
            print(url)
            yield Request(url, callback=self.parse_doctor)    

        for link in response.xpath("//ul[@class='pager']/li[@class='next']/a[@rel='next']/@href"):
            url = response.urljoin(link.extract())
            yield Request(url, callback=self.parse)     
        

    def parse_doctor(self, response):
        item = DottoriItem()

        item['link'] = response.request.url
        item['name'] = response.xpath("//h1[@itemprop='name']/text()").extract_first()
        yield item