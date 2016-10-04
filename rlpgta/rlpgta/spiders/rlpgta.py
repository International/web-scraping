#scrapy crawl simplifyem -o items.json -t json


import scrapy
from scrapy import Request

class RlpgtaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    link = scrapy.Field()
    agent_name = scrapy.Field()
    agent_awards = scrapy.Field()
    personal_link = scrapy.Field()
    phone = scrapy.Field()
    email = scrapy.Field()
    agent_office_name = scrapy.Field()
    agent_office_address = scrapy.Field()


class SimplifyemSpider(scrapy.Spider):
    name = "rlpgta"
    allowed_domains = ["rlpgta.ca"]
    start_urls = [
        "http://www.rlpgta.ca/menuagent.asp?Search=&Filter=&Page=1"
    ]


    def parse(self, response):
        
        for link in response.xpath("//div[@class='agents']/div[@class='agent_info']/div[@class='ai_name']/a/@href"):
            print(link.extract())
            url = response.urljoin(link.extract())
            print(url)
            yield Request(url, callback=self.parse_element)    
         
        
        #pagination
        next_page=response.xpath("//table//a[contains(text(),'Next >>')]/@href")
        url = response.urljoin(next_page.extract_first())
        yield scrapy.Request(url, self.parse_state)
        


    def parse_element(self, response):

            item = RlpgtaItem()
            #НЕ ДОПИСАНО ДО КІНЦЯ...................................................................................................................
            item['link'] = response.request.url
            item['agent_name'] = response.xpath("//div[@class='agent_profile_name']/text()").extract_first().strip()
            item['agent_awards'] = response.xpath("//div[@class='agent_profile_awards']/text()").extract_first().strip()
            item['personal_link'] = response.xpath("//div[@class='agent_profile_personal_link']/text()").extract_first().strip()
            item['phone'] = response.xpath("//div[@class='agent_profile_phone']/text()").extract_first().strip()
            item['email'] = response.xpath("//div[@class='agent_profile_fax']/text()").extract_first().strip()
            item['agent_office_name'] = response.xpath("//div[@class='agent_profile_office_name']/text()").extract_first().strip()
            item['agent_office_address'] = response.xpath("//div[@class='agent_profile_office_address']/text()").extract_first().strip()

            yield item