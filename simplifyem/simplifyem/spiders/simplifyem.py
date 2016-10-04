#scrapy crawl simplifyem -o items.json -t json


import scrapy
from scrapy import Request

class SimplifyemItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    link = scrapy.Field()
    company_name = scrapy.Field()
    address = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    zip_code = scrapy.Field()
    description = scrapy.Field()



class SimplifyemSpider(scrapy.Spider):
    name = "simplifyem"
    allowed_domains = ["simplifyem.com"]
    start_urls = ["http://www.simplifyem.com/property-management-companies"]


    def parse(self, response):
        for link in response.xpath("//div[@id='container']//table[1]//table[1]//td[@valign='top']/a/@href"):
            url = response.urljoin(link.extract())
            yield Request(url, callback=self.parse_state)    
        

    def parse_state(self, response):
        for link in response.xpath("//div[@id='home']//div[@class='lst pb15 mt15']//h2/a/@href"):
            url = response.urljoin(link.extract())
            yield Request(url, callback=self.parse_page)     
        
        #pagination
        next_page=response.xpath("//div[@id='home']/div[@class='paginateButtons']/a[@class='next']/@href")
        url = response.urljoin(next_page.extract_first())
        yield scrapy.Request(url, self.parse_state)
        

    def parse_page(self, response):
        item = SimplifyemItem()
        item['link'] = response.request.url
        item['company_name'] = response.xpath("//*[@id='contentcolumn']/div/h2/text()").extract_first()
        item['address'] = response.xpath("//*[@id='contentcolumn']/div/table//table//tr[2]/td[2]/text()").extract_first()
        item['city'] = response.xpath("//*[@id='contentcolumn']/div/table//table//tr[3]/td[2]/text()").extract_first()
        item['state'] = response.xpath("//*[@id='contentcolumn']/div/table//table//tr[4]/td[2]/text()").extract_first()
        item['zip_code'] = response.xpath("//*[@id='contentcolumn']/div/table//table//tr[5]/td[2]/text()").extract_first()
        item['description'] = response.xpath("//*[@id='featured_comp_b']/p/text()").extract_first()
        yield item