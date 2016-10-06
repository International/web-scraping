#scrapy crawl applebees -o items.json -t json


import scrapy
from scrapy import Request

class ApplebeesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    link = scrapy.Field()
    state = scrapy.Field()
    restaurant_name = scrapy.Field()
    street = scrapy.Field()
    city = scrapy.Field()
    region = scrapy.Field()
    postal = scrapy.Field()
    phone = scrapy.Field()



class ApplebeesSpider(scrapy.Spider):
    name = "applebees"
    allowed_domains = ["restaurants.applebees.com"]
    start_urls = ["http://restaurants.applebees.com/sitemap.html"]


    def parse(self, response):
        for state in response.xpath("//div[@class='card sitemap-list']/div[@class='row']"):
            
            item = ApplebeesItem()
            item['state'] = state.xpath("./h3/text()").extract_first()
            for link in state.xpath(".//a/@href"):
                url = response.urljoin(link.extract())
                yield Request(url, meta={'item':item}, callback=self.parse_restaurant)    
        

    def parse_restaurant(self, response):
        item = response.request.meta['item']
        item['link'] = response.request.url
        item['restaurant_name'] = response.xpath("//div[@itemprop='name']/text()").extract_first()
        item['street'] = response.xpath("//span[@itemprop='streetAddress']/text()").extract_first()
        item['city'] = response.xpath("//span[@itemprop='addressLocality']/text()").extract_first()
        item['region'] = response.xpath("//span[@itemprop='addressRegion']/text()").extract_first()
        item['postal'] = response.xpath("//span[@itemprop='postalCode']/text()").extract_first()
        item['phone'] = response.xpath("//strong[@itemprop='telephone']/text()").extract_first()

        yield item