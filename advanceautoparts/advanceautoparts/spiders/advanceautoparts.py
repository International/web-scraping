#scrapy crawl advanceautoparts -o items.json -t json
import string

from scrapy import Request
import scrapy

from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError

'''
Scrap from stores.advanceautoparts.com
Example:
    {'addressCountry': 'US',
     'addressLocality': 'Waverly',
     'addressRegion': 'TN',
     'postalCode': '37185',
     'shopName': 'Advance Auto Parts',
     'shopNumber': '3860',
     'storeLink': 'http://tn.waverly.stores.advanceautoparts.com/auto_parts_waverly_tn_3860.html',
     'streetAddress': '421 W Main St',
     'telephone': '931-296-2499'}
'''

class AdvanceautopartsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    shopName = scrapy.Field()
    shopNumber = scrapy.Field()
    streetAddress = scrapy.Field()
    addressLocality = scrapy.Field()
    addressRegion = scrapy.Field()
    postalCode = scrapy.Field()
    addressCountry = scrapy.Field()
    telephone = scrapy.Field()
    storeLink = scrapy.Field()

class AdvanceautopartsSpider(scrapy.Spider):
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
            item = AdvanceautopartsItem()
            item['shopName'] = ' '.join([line.strip() for line in info.xpath(".//div[@itemprop='name']//text()").extract() if line.strip()])
            item['shopNumber'] = (info.xpath(".//span[@itemprop='streetAddress']/a/@href").extract_first().split('_')[-1]).split('.')[0]
            item['streetAddress'] = ' '.join([line.strip() for line in info.xpath(".//span[@itemprop='streetAddress']//text()").extract() if line.strip()])
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