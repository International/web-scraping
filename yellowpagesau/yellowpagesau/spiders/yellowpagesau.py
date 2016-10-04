#scrapy crawl yellowpagesau -o items.json -t json

import scrapy
from scrapy import Request
from scrapy.http import TextResponse 

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC





class YellowpagesauItem(scrapy.Item):
    # define the fields for your item here like:
    page_url = scrapy.Field()
    link = scrapy.Field()
    name = scrapy.Field()
    phone = scrapy.Field()
    email = scrapy.Field()
    website = scrapy.Field() 
    address = scrapy.Field() 
    pass


class YellowpagesauSpider(scrapy.Spider):
    name = "yellowpagesau"
    allowed_domains = ["www.yellowpages.com.au"]
    start_urls = [
        "http://www.yellowpages.com.au"
    ]


    def __init__(self):
        self.driver = webdriver.Chrome(executable_path='F:/MyGitHub/Scraping/yellowpagesau/yellowpagesau/spiders/chromedriver/chromedriver.exe')


    def parse(self, response):

        def isElementPresent(driver, XPATH):
            if len(driver.find_elements_by_xpath(XPATH))>0:
                return True
            else:
                return False

        def handle_captcha(driver,captcha_xpath,home_xpath):
            #Captcha detection
            if isElementPresent(driver,captcha_xpath):
                #Waiting captcha entering
                WebDriverWait(driver, 10000).until(EC.presence_of_element_located((By.XPATH,home_xpath)))
                return True
            return False
        

        self.driver.get("http://www.yellowpages.com.au")
        handle_captcha(self.driver,"//div[@class='form']//form[@name='captcha']","//body[contains(@class, 'home-body')]")

        auStates=["NSW","QLD","VIC","WA","SA","TAS","ACT","NT"]

    
        for url in ["http://www.yellowpages.com.au/search/listings?clue=Caravan+Parks&locationClue=All+States&lat=&lon=&referredBy=www.yellowpages.com.au&selectedViewMode=list&eventType=refinement&state={}".format(state) for state in auStates]:
            
            while True:
                self.driver.get(url)
                #Selenium page_source to scrapy response
                response = TextResponse(url=url, body=self.driver.page_source, encoding='utf-8')

                #print(response.xpath("//div[contains(@class,'search-result')]//div[contains(@class,'in-area-cell')]").extract()[0])



                for info_block in response.xpath("//div[contains(@class,'search-result')]//div[contains(@class,'in-area-cell')]"):

                    item = YellowpagesauItem()
                    item['page_url'] = response.url
                    item['link'] = info_block.xpath(".//a[@class='listing-name']/@href").extract()
                    item['name'] = info_block.xpath(".//a[@class='listing-name']/text()").extract()
                    item['phone'] = info_block.xpath(".//span[@class='contact-text']/text()").extract_first()
                    item['email'] = info_block.xpath(".//a[contains(@class,'contact-email')]/@data-email").extract_first()
                    item['website'] = info_block.xpath(".//a[contains(@class,'contact-url')]/@href").extract_first()
                    item['address'] = info_block.xpath(".//p[contains(@class,'listing-address')]/text()").extract_first()
                    
                    yield item
                

                #Selenium next page
                if len(self.driver.find_elements_by_link_text('Next »'))>0:
                    url = self.driver.find_element_by_link_text('Next »').get_attribute("href");
                else:
                    #If "Next page" button not exist, stop pagination
                    break;
                    
       