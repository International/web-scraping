from scrapy import Request
import scrapy

from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError

import string

class SimpleSpiderItem(scrapy.Item):
    shopName = scrapy.Field()
    shopNumber = scrapy.Field()
    streetAddress = scrapy.Field()
    addressLocality = scrapy.Field()
    addressRegion = scrapy.Field()
    postalCode = scrapy.Field()
    addressCountry = scrapy.Field()
    telephone = scrapy.Field()
    storeLink = scrapy.Field()

class SimpleSpider(scrapy.Spider):
    ## Http cache enabled
    ## Errorlog

    ## To send item: meta{'item':item}
    ## To get item: driver = response.meta['item']

    name = "advanceautoparts"
    allowed_domains = ["stores.advanceautoparts.com"]
    start_urls = ["http://stores.advanceautoparts.com"]

    def parse(self, response):
        # states
        for link in response.xpath("//div[@class='country_listing_wrapper']//a/@href"):
            url = response.urljoin(link.extract())
            yield Request(url, callback=self.parse_cities, errback=self.errback)    

    def parse_cities(self, response):
        # cities
        for link in response.xpath("//div[@id='content']/div[@class='itemlist']/a/@href"):
            url = response.urljoin(link.extract())
            yield Request(url, callback=self.parse_info, errback=self.errback)

    def parse_info(self, response):
        for info in response.xpath("//ul[@class='city_contentlist']//div[@itemprop='address']"):
            item = SimpleSpiderItem()
            item['shopName'] = info.xpath(".//div[@itemprop='name']//text()").extract()
            item['shopNumber'] = info.xpath(".//span[@itemprop='streetAddress']/a/@href").extract_first()
            item['streetAddress'] = info.xpath(".//span[@itemprop='streetAddress']//text()").extract() 
            item['addressLocality'] = info.xpath(".//span[@itemprop='addressLocality']//text()").extract_first()
            item['addressRegion'] = info.xpath(".//span[@itemprop='addressRegion']//text()").extract_first()
            item['postalCode'] = info.xpath(".//span[@itemprop='postalCode']//text()").extract_first()
            item['addressCountry'] = info.xpath(".//span[@itemprop='addressCountry']//text()").extract_first()
            item['telephone'] = info.xpath(".//span[@itemprop='telephone']//text()").extract_first()
            item['storeLink'] = info.xpath(".//span[@itemprop='streetAddress']/a/@href").extract_first()
            yield item

    def errback(self, failure):
        # log all errback failures,
        # in case you want to do something special for some errors,
        # you may need the failure's type
        self.logger.error(repr(failure))

        #if isinstance(failure.value, HttpError):
        if failure.check(HttpError):
            # you can get the response
            response = failure.value.response
            #self.logger.error('HttpError on %s', response.url)
            with open('EERORLOG.txt','a') as f:
                f.write("HttpError Response_url: {}\n".format(response.url))

        #elif isinstance(failure.value, DNSLookupError):
        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            #self.logger.error('DNSLookupError on %s', request.url)
            with open('EERORLOG.txt','a') as f:
                f.write("DNSLookupError Request_url: {}\n".format(request.url))

        #elif isinstance(failure.value, TimeoutError):
        elif failure.check(TimeoutError):
            request = failure.request
            #self.logger.error('TimeoutError on %s', request.url)    
            with open('EERORLOG.txt','a') as f:
                f.write("TimeoutError Request_url: {}\n".format(request.url))


    ## Save file
    '''
    def save_pdf(self, response):
        path = response.url.split('/')[-1]
        self.logger.info('Saving PDF %s', path)
        with open(path, 'wb') as f:
            f.write(response.body)
    '''