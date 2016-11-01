from scrapy import signals

from scrapy.http import TextResponse 
from scrapy.http import HtmlResponse 

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SeleniumMiddleware(object):
    #TODO: Process timeouts, 404, 503,  and other server codes

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.spider_opened, signals.spider_opened)
        crawler.signals.connect(middleware.spider_closed, signals.spider_closed)
        return middleware

    def spider_opened(self, spider):
        self.driver = webdriver.Firefox()

    def spider_closed(self, spider):
        self.driver.close()


    def process_request(self, request, spider):
        ## If selenium not enabled
        if request.meta.get('selenium') is not False:
            self.driver.get(request.url)
            request.meta['driver'] = self.driver # to access driver from response

            response = HtmlResponse(self.driver.current_url, body=self.driver.page_source, encoding='utf-8', request=request)
            return HtmlResponse(request.url, body=self.driver.page_source.encode('utf-8'), encoding='utf-8')

            #?
            #from scrapy.utils.python import to_bytes
            #body = to_bytes(self.driver.page_source)  # body must be of type bytes 




