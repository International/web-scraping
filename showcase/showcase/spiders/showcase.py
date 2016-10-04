#scrapy crawl showcase -o items.json -t json

import scrapy
from scrapy import Request
from scrapy.http import TextResponse 

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class HttpProxyMiddleware(object):
    def process_request(self, request, spider):
        request.meta['proxy'] = "162.144.57.157:443"


class ShowcaseItem(scrapy.Item):
    # define the fields for your item here like:
    link = scrapy.Field()
    position = scrapy.Field()
    brokers_name = scrapy.Field()
    company_name = scrapy.Field()
    street_address1 = scrapy.Field()
    street_address2 = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    zip_code = scrapy.Field()
    phone_number = scrapy.Field()
    email_address = scrapy.Field()
    website_address = scrapy.Field()
    pass


class ShowcaseSpider(scrapy.Spider):
    name = "showcase"
    allowed_domains = ["showcase.com"]
    start_urls = [
        "http://www.showcase.com/b/Commercial-Real-Estate/Alan-Davidson/2261463"
    ]
 
    def __init__(self):
        profile = webdriver.FirefoxProfile() 
        #Selenium PROXY
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.http", "169.50.87.249")
        profile.set_preference("network.proxy.http_port", 80)
        ## Disable CSS
        #profile.set_preference('permissions.default.stylesheet', 2)
        ## Disable images
        profile.set_preference('permissions.default.image', 2)
        ## Disable Flash
        profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so','false')
        profile.update_preferences() 
        
        self.driver = webdriver.Firefox(firefox_profile=profile)

    def parse(self, response):

        myfile="PortlandArea.txt"
        with open("F:/MyGitHub/Scraping/showcase/showcase/urls/"+myfile, "r") as f:
            for url in f:
                print(url)

                self.driver.get(url)
                #Selenium page source to scrapy
                response = TextResponse(url=url, body=self.driver.page_source, encoding='utf-8')
                
                #If information exist
                if response.xpath("//div[@class='divBrokerFullName']/text()"):
                    item = ShowcaseItem()

                    mylist=[elem.strip() for elem in response.xpath("//div[@class='fontBrokerLocAdd']/text()").extract() if elem.strip() is not '']

                    print(len(mylist))

                    if len(mylist) <= 2:
                        item['company_name'] = ((response.xpath("//div[@class='fontBrokerLocAdd']/text()").extract())[0]).strip()
                        item['street_address1'] = ((response.xpath("//div[@class='fontBrokerLocAdd']/text()").extract())[1]).strip()


                    if len(mylist) > 2:
                        item['position'] = ((response.xpath("//div[@class='fontBrokerLocAdd']/text()").extract())[0]).strip()
                        item['company_name'] = ((response.xpath("//div[@class='fontBrokerLocAdd']/text()").extract())[1]).strip()
                        item['street_address1'] = ((response.xpath("//div[@class='fontBrokerLocAdd']/text()").extract())[2]).strip()

                    item['link'] = response.url
                    item['brokers_name'] = (response.xpath("//div[@class='divBrokerFullName']/text()").extract_first()).replace('Property Listings','').strip()
                    if response.xpath("//span[@id='ctl00_cphMain_wfMain_ctl00_ctl00_Search1_ctl01_ctl00_ShowcaseHeader_ctl00_BrokerInfoView_bofSuite']/span[3]/text()"):
                        item['street_address2']=(response.xpath("//span[@id='ctl00_cphMain_wfMain_ctl00_ctl00_Search1_ctl01_ctl00_ShowcaseHeader_ctl00_BrokerInfoView_bofSuite']/span[3]/text()").extract_first()).strip()
                    else:
                        item['street_address2']=''

                    if response.xpath("//span[@id='ctl00_cphMain_wfMain_ctl00_ctl00_Search1_ctl01_ctl00_ShowcaseHeader_ctl00_BrokerInfoView_bofCityStatePostCode']/span[3]/text()"):
                        item['city'] = (((response.xpath("//span[@id='ctl00_cphMain_wfMain_ctl00_ctl00_Search1_ctl01_ctl00_ShowcaseHeader_ctl00_BrokerInfoView_bofCityStatePostCode']/span[3]/text()").extract_first()).split(','))[0])
                        item['state'] = (((((response.xpath("//span[@id='ctl00_cphMain_wfMain_ctl00_ctl00_Search1_ctl01_ctl00_ShowcaseHeader_ctl00_BrokerInfoView_bofCityStatePostCode']/span[3]/text()").extract_first()).split(','))[-1]).strip()).split(' '))[0]
                        item['zip_code'] = (((response.xpath("//span[@id='ctl00_cphMain_wfMain_ctl00_ctl00_Search1_ctl01_ctl00_ShowcaseHeader_ctl00_BrokerInfoView_bofCityStatePostCode']/span[3]/text()").extract_first()).split(' '))[-1])
                    else:
                        item['city'] = ''
                        item['state'] = ''
                        item['zip_code'] =''
                    if response.xpath("//span[@id='ctl00_cphMain_wfMain_ctl00_ctl00_Search1_ctl01_ctl00_ShowcaseHeader_ctl00_BrokerInfoView_bofPhone']/span[3]/text()"):
                        item['phone_number'] = (response.xpath("//span[@id='ctl00_cphMain_wfMain_ctl00_ctl00_Search1_ctl01_ctl00_ShowcaseHeader_ctl00_BrokerInfoView_bofPhone']/span[3]/text()").extract_first()).strip()
                    else:
                        item['phone_number'] = ''
                    if response.xpath("//a[@id='ctl00_cphMain_wfMain_ctl00_ctl00_Search1_ctl01_ctl00_ShowcaseHeader_ctl00_BrokerInfoView_lnkBrokerEmail']/text()"):
                        item['email_address'] = (response.xpath("//a[@id='ctl00_cphMain_wfMain_ctl00_ctl00_Search1_ctl01_ctl00_ShowcaseHeader_ctl00_BrokerInfoView_lnkBrokerEmail']/text()").extract_first()).strip()
                    else:
                        item['email_address'] = ''
                    if response.xpath("//a[@id='ctl00_cphMain_wfMain_ctl00_ctl00_Search1_ctl01_ctl00_ShowcaseHeader_ctl00_BrokerInfoView_website']/text()"):
                        item['website_address'] = (response.xpath("//a[@id='ctl00_cphMain_wfMain_ctl00_ctl00_Search1_ctl01_ctl00_ShowcaseHeader_ctl00_BrokerInfoView_website']/text()").extract_first()).strip()
                    else:
                        item['website_address'] = ''
                    yield item

                else:
                    #Can't open url
                    with open("404.txt", "a") as f:
                        f.write(url)
    