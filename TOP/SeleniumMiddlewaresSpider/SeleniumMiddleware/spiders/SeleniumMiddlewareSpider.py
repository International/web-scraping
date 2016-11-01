import string 
import copy

import scrapy
from scrapy import Request
from scrapy.http import TextResponse 
from scrapy.http import HtmlResponse 


class SeleniumMiddlewareItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    company_name = scrapy.Field()

    address = scrapy.Field()
    street = scrapy.Field()
    city = scrapy.Field()
    province = scrapy.Field()
    postal_code = scrapy.Field()

    company_email = scrapy.Field()
    company_phone = scrapy.Field()
    company_website = scrapy.Field()
    description = scrapy.Field()

    year_established = scrapy.Field()
    primary_industry = scrapy.Field()
    employee = scrapy.Field()

    contact_name = scrapy.Field()
    contact_title = scrapy.Field()
    contact_email = scrapy.Field()
    contact_phone = scrapy.Field()

    URL = scrapy.Field()

class SeleniumMiddlewareSpider(scrapy.Spider):
    ## Selenium documentation http://selenium-python.readthedocs.io/navigating.html
    ## To get driver: driver = response.meta['driver']
    #  Example:
    #  driver.find_element_by_xpath("//a[@id='ic-header']").click()

    ## To disable selenium middleware: meta={'selenium':False}

    name = "industry_canada"
    allowed_domains = ["ic.gc.ca"]
    start_urls = ["http://www.ic.gc.ca/app/ccc/sld/cmpny.do?lang=eng&profileId=1921&naics=333"]

    def parse(self, response):
        for link in response.xpath("//li[@class='mrgn-bttm-sm']//a/@href"):
            url = response.urljoin(link.extract())   
            yield Request(url, callback=self.parse_item, meta={'selenium':False})

        for link in response.xpath("//ul[@class='alphaPicklist']//a/@href"):
            url = response.urljoin(link.extract())
            yield Request(url, callback=self.parse)

    def parse_item(self, response):
        item = SeleniumMiddlewareItem()
        item['URL'] = response.request.url
        item['company_name'] = response.xpath("//h1[@id='cn-cont']/text()").extract_first()
        item['address'] = response.xpath("//strong[contains(text(),'Location Address')]/following-sibling::text()").extract()
        item['company_phone'] = response.xpath("//div[@class='span-4']/div[contains(@class,'icRow')][div[contains(@class,'ic2col1')]/abbr[@title='Telephone']]/div[contains(@class,'ic2col2')]/text()").extract()
        item['company_website'] = response.xpath("//a[@title='Website URL']/@href").extract_first()
        item['company_email'] = response.xpath("//a[contains(@href,'mailto:')]/@href").extract_first()
        item['description'] = response.xpath("//p[@class='comment more']/text()").extract_first()
        item['year_established'] = response.xpath("//div[@class='active']//tr[@class='boxInside'][td[1]/strong[contains(text(),'Year Established')]]/td[2]/text()").extract_first()
        item['primary_industry'] = response.xpath("//div[@class='active']//tr[@class='boxInside'][td[1]/strong[contains(text(),'Primary Industry')]]/td[2]/text()").extract_first()
        item['employee'] = response.xpath("//div[@class='active']//tr[@class='boxInside'][td[1]/strong[contains(text(),'Number of Employees')]]/td[2]/text()").extract_first()
                
        print(len(response.xpath("//div[@class='active']//tr[@class='boxInside'][td[@colspan='2']/strong]")))
        for contact in response.xpath("//div[@class='active']//tr[@class='boxInside'][td[@colspan='2']/strong]"):
            contact_exist = True
            # create new copy of item
            new_item = copy.deepcopy(item)
            new_item['contact_name'] = contact.xpath("./td[@colspan='2']/strong/text()").extract()

            for contact_elem in contact.xpath("./following-sibling::*"):
                if contact_elem.xpath("./td[@class='contactLine']"):
                    break
                if contact_elem.xpath(".//strong[contains(text(),'Title')]"):
                    new_item['contact_title'] = contact_elem.xpath(".//strong[contains(text(),'Title:')]/../text()").extract()
                if contact_elem.xpath(".//strong[contains(text(),'Email')]"):
                    new_item['contact_email'] = contact_elem.xpath(".//strong[contains(text(),'Email:')]/../text()").extract()
                if contact_elem.xpath(".//strong[contains(text(),'Telephone')]"):
                    new_item['contact_phone'] = contact_elem.xpath(".//strong[contains(text(),'Telephone:')]/../text()").extract()
            yield new_item

        if not contact_exist:
            yield item

