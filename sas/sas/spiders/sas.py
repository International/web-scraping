#scrapy crawl advanceautoparts -o items.json -t json
from scrapy import Request
import scrapy

from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError

'''
Scrap from www2.sas.com/proceedings/sugi30/toc.html
Interesting: PDF saving
'''

class SasItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pdf_url = scrapy.Field()
    paper_number = scrapy.Field()
    cite = scrapy.Field()
    name = scrapy.Field()
    category = scrapy.Field()

class SasSpider(scrapy.Spider):
    name = "sas"
    allowed_domains = ["www2.sas.com"]
    start_urls = ["http://www2.sas.com/proceedings/sugi30/toc.html"]

    def parse(self, response):

        for element in response.xpath("//p[a[contains(@href,'pdf')]/cite]"):
            #url = response.urljoin(link.extract())
            item = SasItem()
            #item['category'] = element.xpath("./ancestor::*//font[1]/text()").extract()
            item['category'] = element.xpath("./preceding-sibling::*//font[last()]/text()").extract()[-1]
            item['paper_number'] = element.xpath("./b/a/text()").extract_first()
            item['name'] = ''.join(elem.strip() for elem in element.xpath("./text()").extract() if elem.strip())
            item['pdf_url'] = element.xpath("a[contains(@href,'pdf')]/@href").extract_first()
            item['cite'] = element.xpath("a[contains(@href,'pdf')]/cite/text()").extract_first()

            yield item
            yield Request(item['pdf_url'], callback=self.save_pdf, errback=self.errback) 

    def save_pdf(self, response):
        path = response.url.split('/')[-1]
        self.logger.info('Saving PDF %s', path)
        with open(path, 'wb') as f:
            f.write(response.body)


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