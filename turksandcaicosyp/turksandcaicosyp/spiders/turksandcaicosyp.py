#scrapy crawl turksandcaicosyp -o items.json -t json

import string
import scrapy
from scrapy import Request

class TurksandcaicosypItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    name = scrapy.Field()
    area = scrapy.Field()
    phone = scrapy.Field()



class TurksandcaicosypSpider(scrapy.Spider):
    name = "turksandcaicosyp"
    allowed_domains = ["turksandcaicosyp.com"]
    start_urls = [
        "http://turksandcaicosyp.com/Turks-Caicos/Residential/A"
    ]


    def parse(self, response):

        #string.ascii_lowercase - alphabet a-z
        #more information - help(string)
        for letter in list(string.ascii_lowercase):
            url = "http://turksandcaicosyp.com/Turks-Caicos/Residential/"+letter
            yield Request(url, callback=self.parse_page)  


    def parse_page(self, response):
        item = TurksandcaicosypItem()

        for info_block in response.xpath("//div[@class='listdiv']/div[@class='listbox']"):
            item['name'] = info_block.xpath("div/div[4]/div[@class='lname']/text()").extract()
            item['area'] = info_block.xpath("div/div[4]/text()").extract()
            item['phone'] = info_block.xpath("div/div[4]/b/text()").extract()
            yield item

        #pagination
        next_page=response.xpath("//div[@class='listdiv']/a[contains(small/b/text(),'NEXT ')]/@href")
        url = response.urljoin(next_page.extract_first())
        yield Request(url, self.parse_page)


       