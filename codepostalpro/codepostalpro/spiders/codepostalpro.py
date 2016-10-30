#scrapy crawl advanceautoparts -o items.json -t json
from scrapy import Request
import scrapy

import base64

from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError

'''
Scrap from www.codepostalpro.com/tunisie.html
Interesting: base64 decoding
'''

class CodepostalproItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    URL = scrapy.Field()
    region = scrapy.Field()
    city = scrapy.Field()
    area = scrapy.Field()
    latitude_url = scrapy.Field()
    longitude_url = scrapy.Field()
    post_code = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    latitude_decoded = scrapy.Field()
    longitude_decoded = scrapy.Field()

class CodepostalproSpider(scrapy.Spider):
    name = "codepostalpro"
    allowed_domains = ["codepostalpro.com"]
    start_urls = ["http://www.codepostalpro.com/tunisie.html"]

    def parse(self, response):
        # states
        for link in response.xpath("//table[@class='table table-striped']//a/@href"):
            url = response.urljoin(link.extract())
            yield Request(url, callback=self.parse_cities, errback=self.errback)    

    def parse_cities(self, response):
        # cities
        for link in response.xpath("//table[@class='table table-striped']//a/@href"):
            url = response.urljoin(link.extract())
            yield Request(url, callback=self.parse_areas, errback=self.errback)

    def parse_areas(self, response):
        # cities
        for link in response.xpath("//table[@class='table table-striped']//a/@href"):
            url = response.urljoin(link.extract())
            yield Request(url, callback=self.parse_info, errback=self.errback)


    def parse_info(self, response):
        item = CodepostalproItem()
        item['URL'] = response.request.url
        item['region'] = response.xpath("//table[@class='table1']/tr[1]//h4/text()").extract_first()
        item['city'] = response.xpath("//table[@class='table1']/tr[2]//h4/text()").extract_first()
        item['area'] = response.xpath("//table[@class='table1']/tr[3]//h4/text()").extract_first()
        item['post_code'] = response.xpath("//table[@class='table1']/tr[4]//h4/img/@title").extract_first()

        item['latitude_url'] = response.xpath("//table[@class='table1']/tr[5]//h4//img/@src").extract_first()
        item['longitude_url'] = response.xpath("//table[@class='table1']/tr[6]//h4//img/@src").extract_first()

        try:
            if '%' in response.xpath("//table[@class='table1']/tr[5]//h4//img/@src").extract_first():
                item['latitude'] = ((response.xpath("//table[@class='table1']/tr[5]//h4//img/@src").extract_first()).split('%')[0]).split('=')[-1]
            else:
                item['latitude'] = ((response.xpath("//table[@class='table1']/tr[5]//h4//img/@src").extract_first()).split('&')[0]).split('=')[-1]
        except:
            item['latitude'] = 'Error'
           
        try:
            if '%' in response.xpath("//table[@class='table1']/tr[6]//h4//img/@src").extract_first():
                item['longitude'] = ((response.xpath("//table[@class='table1']/tr[6]//h4//img/@src").extract_first()).split('%')[0]).split('=')[-1]
            else:
                item['longitude'] = ((response.xpath("//table[@class='table1']/tr[6]//h4//img/@src").extract_first()).split('&')[0]).split('=')[-1]
        except:
            item['longitude'] = 'Error'

        try:
            item['latitude_decoded'] = (base64.b64decode('{}{}'.format(item['latitude'],'==')))
            item['longitude_decoded'] = (base64.b64decode('{}{}'.format(item['longitude'],'==')))
        except:
            item['latitude_decoded'] = ''
            item['longitude_decoded'] = ''


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