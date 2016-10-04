#scrapy crawl simplifyem -o items.json -t json

import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import scrapy
from scrapy import Request

from scrapy.http import TextResponse 
from scrapy.http import HtmlResponse 

class GreentechItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    link = scrapy.Field()
    company_name = scrapy.Field()
    email = scrapy.Field()
    website = scrapy.Field()
    address = scrapy.Field()


class GreentechSpider(scrapy.Spider):
    name = "greentech"
    allowed_domains = ["greentech.nl"]
    start_urls = [
        "http://www.greentech.nl/amsterdam/exhibitors/"
    ]

    def __init__(self):
        self.driver = webdriver.Firefox()

    def parse(self, response):
        self.driver.get("http://www.greentech.nl/amsterdam/exhibitors/")

        #Scroll to end
        for i in range(10):
            self.driver.find_element_by_xpath("//div[@class='async-content']").send_keys(Keys.PAGE_DOWN)
            time.sleep(1)

        #Get links
        for link in self.driver.find_elements_by_xpath("//div[@class='table-responsive']//tr/td[2]/a"):
            yield scrapy.Request(link.get_attribute("href"), self.parse_company)

    def parse_company(self, response):
        print(response.url)
        item = GreentechItem()
        item['link'] = response.url
        item['company_name'] = (response.xpath("//div[@class='Companytitle']/h1[@class='title']/text()").extract_first()).strip()
        item['email'] = response.xpath("//a[contains(text(),'Email us »')]/@href").extract_first()[7:]
        item['website'] = response.xpath("//a[@class='exh_website']/@href").extract_first()
        item['address'] =  (' '.join([address.strip() for address in response.xpath("//div[@class='formatAddress']//text()").extract()])).strip()
        yield item

