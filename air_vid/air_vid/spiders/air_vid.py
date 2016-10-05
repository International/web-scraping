#scrapy crawl air_vid -o items.json -t json
import scrapy
from scrapy import Request

class AirVidItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    email = scrapy.Field()

class AirVidSpider(scrapy.Spider):
    name = "air_vid"
    allowed_domains = ["air-vid.com"]
    start_urls = ["http://air-vid.com/wp/listings/?fwp_paged=1"]

    def start_requests(self):
        for i in range(1,20):
            url="http://air-vid.com/wp/listings/?fwp_paged="+str(i)
            print(url)
            yield Request(url, callback=self.parse) 

    def parse(self, response):
        for block in response.xpath("//div[@class='card__content']"):    
            item = AirVidItem()
            item['email'] =(block.xpath(".//a[contains(@href,'mailto')]/@href").extract_first())[7:]
            yield item