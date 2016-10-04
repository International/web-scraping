#scrapy crawl idoctors -o items.json -t json
import scrapy
from scrapy import Request

class IdoctorsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    link = scrapy.Field()
    prof = scrapy.Field()
    name = scrapy.Field()
    specialization = scrapy.Field()
    photo_link = scrapy.Field()
    calendar = scrapy.Field()

class IdoctorsSpider(scrapy.Spider):
    name = "idoctors"
    allowed_domains = ["idoctors.it"]
    start_urls = ["https://www.idoctors.it"]

    def parse(self, response):
        for link in response.xpath("//div[@id='home-medici-specialisti']//ul[@class='list-unstyled']//a/@href"):
            url = response.urljoin(link.extract())
            yield Request(url, callback=self.parse_provinces)    

    def parse_provinces(self, response):
        for link in response.xpath("//div[contains(@class,'regioni-view')]//ul[@class='list-unstyled']//a/@href"):
            url = response.urljoin(link.extract())
            yield Request(url, callback=self.parse_element)      
        
    def parse_element(self, response):
        print(response.url)
        for link in response.xpath("//div[contains(@class,'medico')]//div[contains(@class,'prestazioni-medico')]/a[1]/@href"):
            url = response.urljoin(link.extract())
            yield Request(url, callback=self.parse_doctor) 

        #pagination
        for page in response.xpath("//div[@id='paginatediv']/a/@href"):
            url = page.extract()
            yield Request(url, callback=self.parse_element) 

    def parse_doctor(self, response):
        item = IdoctorsItem()
        item['link'] = response.request.url
        item['prof'] = response.xpath("//span[@class='nome-medico']/text()").extract_first().split()[0]
        item['name'] = (response.xpath("//span[@class='nome-medico']/text()").extract_first()).replace(item['prof'],'').strip()
        item['specialization'] = response.xpath("//h2[@class='specializzazione-medico']/text()").extract_first()
        item['photo_link'] = response.xpath("//img[contains(@class,'foto-medico')]/@src").extract_first()
        item['calendar'] = len(response.xpath("//div[@id='prest-top-acc-0']//ul[contains(@class,'prest-top')]/li").extract())
        yield item