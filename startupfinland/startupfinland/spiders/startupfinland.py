#scrapy crawl startupfinland -o items.json -t json
import scrapy
from scrapy import Request
from scrapy.http import TextResponse 

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from validate_email_address import validate_email

class StartupfinlandItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    link = scrapy.Field()
    name = scrapy.Field()
    email = scrapy.Field()
    team = scrapy.Field()
    role = scrapy.Field()
    validation = scrapy.Field()
    pass

class StartupfinlandSpider(scrapy.Spider):
    name = "startupfinland"
    allowed_domains = ["funderbeam.com"]
    start_urls = ["https://www.funderbeam.com/startups?searchBio=0&hqLocations=FIN"]

    def __init__(self):
        self.driver = webdriver.Firefox()

    def parse(self, response):
        self.driver.get(response.url)

        #Open all page (Click button show more, until it exist)
        while len(self.driver.find_elements_by_class_name('load-more-startups'))>0:
            try:
                self.driver.find_element_by_class_name('load-more-startups').click()
            except:
                self.driver.implicitly_wait(1)
        
        #Selenium page_source to scrapy
        response = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
        for link in response.xpath("//td[@data-column-name='name']/h1/a/@href"):
            url = response.urljoin(link.extract())
            yield scrapy.Request(url, self.parse_startup)
   
    def parse_startup(self, response):
        if response.xpath("//div[@class='description']//address/a[contains(@href,'mailto:')]/text()"):
            item = StartupfinlandItem()
            item['link'] = response.url
            item['name'] = (response.xpath("//div[@class='details']//h1/text()").extract_first()).strip()
            item['email'] = (response.xpath("//div[@class='description']//address/a[contains(@href,'mailto:')]/text()").extract_first()).strip()
            if response.xpath("//div[@class='tab-content']/div[@id='team-all']//div[@class='infocard']/a[contains(@class,'cardlink')]/h2/text()"):
                item['team'] = (response.xpath("//div[@class='tab-content']/div[@id='team-all']//div[@class='infocard']/a[contains(@class,'cardlink')]/h2/text()").extract_first()).strip()
            else:
                item['team'] = ''
            if response.xpath("//div[@class='tab-content']/div[@id='team-all']//div[@class='infocard']/a[contains(@class,'cardlink')]/h3/text()"):
                item['role'] = (response.xpath("//div[@class='tab-content']/div[@id='team-all']//div[@class='infocard']/a[contains(@class,'cardlink')]/h3/text()").extract_first()).strip()
            else:
                item['role'] = ''
            item['validation'] = validate_email(item['email'])
            yield item

  
            
