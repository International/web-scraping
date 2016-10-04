#scrapy crawl rackspace -o items.json -t json


import scrapy
from scrapy import Request

class RackspaceItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    link = scrapy.Field()
    company_name = scrapy.Field()
    address = scrapy.Field()
    website = scrapy.Field()
    phone = scrapy.Field()
    partner = scrapy.Field()


class RackspaceSpider(scrapy.Spider):
    name = "rackspace"
    allowed_domains = ["partners.rackspace.com"]
    start_urls = []

     #"http://partners.rackspace.com/directory/search?f0=Business+Type&f0v0=Digital+Agency&p=1"
    def start_requests(self):
        for page_number in range(0,81):
            url = "http://partners.rackspace.com/directory/search?f0=Business+Type&f0v0=Digital+Agency&p="+str(page_number)
            print(url)
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        
        for element in response.xpath("//article[@class='mktPartnerDetail']"):
            item = RackspaceItem()
            
            item['link'] = response.urljoin(element.xpath("./h3[@class='mktPartnerDetailHeader']/a/@href").extract_first())
            item['company_name'] = element.xpath("./h3[@class='mktPartnerDetailHeader']/a/text()").extract_first()
            item['address'] = ' '.join([line.strip() for line in element.xpath("./address/text()").extract() if line.strip()])
            item['website'] = element.xpath("./div[contains(text(),'Visit')]/a/@href").extract_first()
            item['phone'] = ''.join([line.strip() for line in element.xpath("./text()").extract() if line.strip()])[7:]
            item['partner'] = element.xpath("./div/span[@class='mktDetailsGroupItems']/text()").extract_first()
            yield item


            

