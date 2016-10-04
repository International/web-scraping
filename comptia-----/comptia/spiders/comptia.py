#scrapy crawl simplifyem -o items.json -t json
#username : marc.spring@evolvedoffice.com
#password : Comptiacrawl


from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import scrapy
from scrapy import Request

class ComptiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    company_name = scrapy.Field()



class ComptiaSpider(scrapy.Spider):
    name = "comptia"
    allowed_domains = ["comptia.com"]
    start_urls = [
        "https://www.comptia.org/insight-tools/individual-directory?c=27546&c=27195"
    ]

    def __init__(self):
        self.driver = webdriver.Firefox()



    def parse(self, response):

        def isElementPresent(driver, XPATH):
            if len(driver.find_elements_by_xpath(XPATH))>0:
                return True
            else:
                return False

        def wait_login(driver,captcha_xpath,home_xpath):
            #Captcha detection
            if isElementPresent(driver,captcha_xpath):
                #Waiting captcha entering
                WebDriverWait(driver, 10000).until(EC.presence_of_element_located((By.XPATH,home_xpath)))
                return True
            return False


        self.driver.get("https://www.comptia.org/insight-tools/individual-directory")
        wait_login(self.driver,"//div[@id='PageSecurityControls_C003_UserLoginForm2_pnlLogin']","//div[@id='ctl00_LeftColumn_C001_RadSearchBox1']")

        #A-Z
        self.driver.find_element_by_xpath("//div[@id='LeftColumn_C001_pnlBasicSearch']/div[2]/a").click()


        for current_letter in ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]:


            self.driver.get("https://www.comptia.org/insight-tools/individual-directory")
            #A-Z
            self.driver.find_element_by_xpath("//div[@id='LeftColumn_C001_pnlBasicSearch']/div[2]/a").click()

            print(current_letter)
            self.driver.find_element_by_xpath("//a[@id='LeftColumn_C001_alphaSearch09']").text
            #To next letter
            for letter in self.driver.find_elements_by_xpath("//nav[@class='namefilter']/a"):
                print(letter.text)
                if letter.text == current_letter:
                    letter.click

            break

            #Getting information from all pages
            while True:
                #Get urls list
                urls = []
                for element in self.driver.find_elements_by_xpath("//table[@id='ctl00_LeftColumn_C001_RadGrid1_ctl00']//tr/td[2]/a"):
                    urls.append(response.urljoin(element.get_attribute("href")))

                #Sxrap elements
                for url in urls:
                    self.driver.get(url)
                    response = TextResponse(url=url, body=self.driver.page_source, encoding='utf-8')
                    item = ComptiaItem()
                        
                    item['company_name'] = response.xpath("//div[@class='profile']//h2/span//text()").extract_first()
                    yield item
                        

                #Selenium next page
                if len(self.driver.find_elements_by_xpath("//a[@rel='next']"))>0:
                    self.driver.find_element_by_xpath("//a[@rel='next']").click()
                else:
                    break



            




       
    