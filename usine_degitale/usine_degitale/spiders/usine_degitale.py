#scrapy crawl usine_degitale -o items.json -t json

import re
import scrapy
from scrapy import Request
from scrapy.http import TextResponse 

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class UsineDegitaleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    link = scrapy.Field()
    name = scrapy.Field()
    ceo = scrapy.Field()
    phone = scrapy.Field()
    city = scrapy.Field()
    website = scrapy.Field()
    email = scrapy.Field()

class IdoctorsSpider(scrapy.Spider):
    name = "usine_degitale"
    allowed_domains = ["usine-digitale.fr"]
    start_urls = ["http://www.usine-digitale.fr/annuaire-start-up/start-up-du-web/"]

    def __init__(self):
        self.driver = webdriver.Firefox()

    def parse(self, response):
        for link in response.xpath("//section[@itemprop='isPartOf']/a[@class='contenu']/@href"):
            url = response.urljoin(link.extract())
            yield Request(url, callback=self.parse_element) 

        #pagination
        for page in response.xpath("//div[@class='pagination']/a[@rel='next']/@href"):
            url = response.urljoin(page.extract())
            yield Request(url, callback=self.parse) 


    def parse_element(self, response):
        url = response.request.url
        #Email address shows by js
        self.driver.get(url)
        response = TextResponse(url=url, body=self.driver.page_source, encoding='utf-8')


        item = UsineDegitaleItem()
        item['link'] = url
        item['name'] = response.xpath("//div[@class='artSectTypeDeux']//h1[@itemprop='name']/text()").extract_first()
        item['ceo'] = ', '.join([(founder.strip().replace('-','')).strip() for founder in response.xpath("//div[@itemprop='founders']/p/text()").extract()])
        item['phone'] = response.xpath("//div[@id='infoPratiq']//p[@itemprop='telephone']/text()").extract_first()
        if len(response.xpath("//div[@id='infoPratiq']//p[@itemprop='address']/text()").extract())>1:
            item['city'] = (re.sub(r"\d+", "", (response.xpath("//div[@id='infoPratiq']//p[@itemprop='address']/text()").extract())[-1])).strip()
        else:
            item['city'] = response.xpath("//div[@id='infoPratiq']//p[@itemprop='address']/text()").extract_first()
        item['website'] = response.xpath("//div[@id='infoPratiq']//a[@itemprop='url']/text()").extract_first()
        item['email'] = response.xpath("//p[@itemprop='email']/text()").extract_first()
        yield item
