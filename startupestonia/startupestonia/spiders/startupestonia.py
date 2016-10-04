#scrapy crawl startupestonia -o items.json -t json

import scrapy
from scrapy import Request
from scrapy.http import TextResponse 

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from validate_email_address import validate_email


class StartupestoniaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    link = scrapy.Field()
    name = scrapy.Field()
    email = scrapy.Field()
    team = scrapy.Field()
    role = scrapy.Field()
    validation = scrapy.Field()
    pass


class StartupestoniaSpider(scrapy.Spider):
    name = "startupestonia"
    allowed_domains = ["startupestonia.ee","funderbeam.com"]
    start_urls = ["http://www.startupestonia.ee/startups"]


    def __init__(self):
        #self.driver = webdriver.Chrome(executable_path='spiders/chromedriver/chromedriver.exe')
        self.driver = webdriver.Firefox()


    def parse(self, response):
        self.driver.get(response.url)
        self.driver.find_element_by_class_name('funderbeam-show-button').click()
        self.driver.find_element_by_class_name('funderbeam-show-button').click()
        self.driver.find_element_by_class_name('funderbeam-show-button').click()

        #Selenium page_source to scrapy
        response = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
        for url in response.xpath("//a[@class='funderbeam-startup-url']/@href").extract():
            yield scrapy.Request(url, self.parse_startup)


    def parse_startup(self, response):
        if response.xpath("//div[@class='description']//address/a[contains(@href,'mailto:')]/text()"):
            item = StartupestoniaItem()
            item['link'] = response.url
            item['name'] = (response.xpath("//div[@class='details']//h1/text()").extract_first()).strip()
            item['email'] = (response.xpath("//div[@class='description']//address/a[contains(@href,'mailto:')]/text()").extract_first()).strip()
            item['team'] = [line.strip() for line in response.xpath("//div[@class='tab-content']/div[@id='team-all']//div[@class='infocard']/a[contains(@class,'cardlink')]/h2/text()").extract()]
            item['role'] = [line.strip() for line in response.xpath("//div[@class='tab-content']/div[@id='team-all']//div[@class='infocard']/a[contains(@class,'cardlink')]/h3/text()").extract()]

            #Email validation
            item['validation'] = validate_email(item['email'])
            yield item


  
            
