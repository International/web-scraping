from scrapy.http import TextResponse 
from scrapy.http import HtmlResponse 

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SeleniumMiddleware(object):

    def __init__(self):
       self.driver = webdriver.Firefox()

    def process_request(self, request, spider):
        self.driver.get(request.url)
        response = HtmlResponse(self.driver.current_url, body=self.driver.page_source, encoding='utf-8', request=request)
        return TextResponse(request.url, body=self.driver.page_source.encode('utf-8'), encoding='utf-8')












        '''
        try:
            self.driver.set_page_load_timeout(10)
            self.driver.get(request.url)
            return HtmlResponse(self.driver.current_url, body=self.driver.page_source, encoding='utf-8', request=request)
        except:
            print ('TIMEOUT')
            page = self.driver.find_element_by_tag_name('body')
            page.send_keys(Keys.ESCAPE)
            #password.send_keys("abcdef", Keys.ENTER, Keys.ESCAPE) # works for Firefox driver 
            #drive.execute_script("window.stop();") # works for Chrome driver
            return HtmlResponse(self.driver.current_url, body=self.driver.page_source, encoding='utf-8', request=request)
        '''



