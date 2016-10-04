#scrapy crawl ioof -o items.json -t json

import scrapy
from scrapy import Request

class IoofItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    page_url = scrapy.Field()
    secretary = scrapy.Field()
    email = scrapy.Field()
    webpage = scrapy.Field()
    phone = scrapy.Field()
    pass


class IoofSpider(scrapy.Spider):
    name = "ioof"
    allowed_domains = ["www.ioof.org"]
    start_urls=["http://www.ioof.org/IOOF/Jurisdictions/IOOF/Jurisdictions/Jurisdictions.aspx?hkey=8c8441c5-fe89-4663-a5ef-8bd165c19bc1"]



    def parse(self, response):

        for link in response.xpath("//div[@id='ctl00_TemplateBody_WebPartManager1_gwpciUSA_ciUSA_Panel_USA']//a/@href"):
            url = response.urljoin(link.extract())
            yield Request(url, callback=self.parse_info)
      

    def parse_info(self, response):
        item = IoofItem()
        
        item['page_url'] = response.request.url
        for info_cell in response.xpath("//table[@class='rgMasterTable']//tr//td[2]"):
            item['secretary'] = (info_cell.xpath("text()").extract_first()).strip()
            item['email'] = info_cell.xpath("a[1]/text()").extract_first()
            item['webpage'] = info_cell.xpath("a[2]/text()").extract_first()
            item['phone'] = (info_cell.xpath("text()").extract()[-1]).strip()
            yield item


        