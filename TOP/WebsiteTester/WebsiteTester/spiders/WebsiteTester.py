import string 
import copy

import scrapy
from scrapy import Request
from scrapy.http import TextResponse 
from scrapy.http import HtmlResponse 


class WebsiteTesterItem(scrapy.Item):
    #scrapy_status = scrapy.Field()
    #selenium_status = scrapy.Field()
    pass

class WebsiteTester(scrapy.Spider):
    ## Selenium documentation http://selenium-python.readthedocs.io/navigating.html
    ## To get driver: driver = response.meta['driver']
    #  Example:
    #  driver.find_element_by_xpath("//a[@id='ic-header']").click()

    ## To disable selenium middleware: meta={'selenium':False}

    name = "test"
    allowed_domains = ["ic.gc.ca"]
    start_urls = ["http://www.ic.gc.ca/app/ccc/sld/cmpny.do?lang=eng&profileId=1921&naics=333"]

    def parse(self, response):
        item = WebsiteTesterItem()
        print("######################################################################")
        print("#####             Succssesful conection by SELENIUM              #####")
        print("######################################################################")
        yield Request(response.request.url, callback=self.test_scrapy, meta={'selenium':False})

    def test_scrapy(self, response):
        print("######################################################################")
        print("#####              Succssesful conection by SCRAPY               #####")
        print("######################################################################")


