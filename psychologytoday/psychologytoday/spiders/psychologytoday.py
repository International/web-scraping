#scrapy crawl psychologytoday -o items.json -t json

import scrapy
from scrapy import Request
from scrapy.http import TextResponse 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class PsychologytodayItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    terapist_type = scrapy.Field()
    phone = scrapy.Field()

    # Address
    address = scrapy.Field()
    address_2 = scrapy.Field()
    city = scrapy.Field()
    postal_code = scrapy.Field()
    street_address = scrapy.Field()

    image_link = scrapy.Field()
    description = scrapy.Field()
    specialties = scrapy.Field()
    mental_health = scrapy.Field()
    sexuality = scrapy.Field()
    issues = scrapy.Field()

    # Qualification
    qualifications_years_in_practice = scrapy.Field()
    qualifications_school = scrapy.Field()
    qualifications_year_graduated = scrapy.Field()
    qualifications_license_and_state = scrapy.Field()
    qualifications_other = scrapy.Field()
    # Finances
    finances_avg_cost = scrapy.Field()
    finances_sliding_scale = scrapy.Field()
    finances_accepts_insurence = scrapy.Field()
    finances_accepted_payment_methods = scrapy.Field()
    finances_accepted_insurance_plans = scrapy.Field()
    # Focus
    focus_age = scrapy.Field()
    focus_categories = scrapy.Field()
    focus_ethnicity = scrapy.Field()
    focus_religious_orientation = scrapy.Field()

    # Treatment Approach
    treatment_orientation = scrapy.Field()
    treatment_momodality = scrapy.Field()

    link = scrapy.Field()

class PsychologytodaySpider(scrapy.Spider):
    name = "psychologytoday"
    allowed_domains = ["therapists.psychologytoday.com","wikipedia.org"]
    start_urls = ["https://www.wikipedia.org"]
    
    def __init__(self):
        self.driver = webdriver.Firefox()


    def parse(self, response):
        page_url = "https://therapists.psychologytoday.com/rms/state/Michigan.html"
        while True:
            self.driver.get(page_url)

            url_list = []
            for link in self.driver.find_elements_by_class_name('result-name'):
                url_list.append(link.get_attribute("href"))
            
            for url in url_list:
                self.driver.get(url)
                
                response = TextResponse(url=url, body=self.driver.page_source, encoding='utf-8')
                item = PsychologytodayItem()
                item['name'] = (response.xpath("//h1[@itemprop='name']/text()").extract_first()).strip()
                item['terapist_type'] = ', '.join([(line.strip()).strip(',') for line in response.xpath("//div[contains(@class,'profile-middle')]//div[@class='profile-title']/h2//text()").extract() if line.strip() not in [',',''] ])
                item['phone'] = response.xpath("//span[@itemprop='telephone']/a/text()").extract_first()
                
                # Address (address duplicates in row)
                item['address'] = ' '.join([line.strip() for line in response.xpath("//div[@class='profile-address']//div[contains(@class,'address-rank-1')][1]/div[@itemprop='address'][1]//text()").extract() if line.strip()])
                # (address_2 Not using in pipelines)
                item['address_2'] = ' '.join([line.strip() for line in response.xpath("//div[contains(@class,'address-rank-2')][1]/div[@itemprop='address'][1]//text()").extract() if line.strip()])
                item['city'] = ''
                item['postal_code'] = ''
                item['street_address'] = ''
                if response.xpath("//span[@itemprop='addressLocality']/text()"):
                    item['city'] = (response.xpath("//span[@itemprop='addressLocality']/text()").extract_first()).strip()
                if response.xpath("//span[@itemprop='postalcode']/text()"):
                    item['postal_code'] = (response.xpath("//span[@itemprop='postalcode']/text()").extract_first()).strip()
                if response.xpath("//span[@itemprop='streetAddress']/text()"):   
                    item['street_address'] = (response.xpath("//span[@itemprop='streetAddress']/text()").extract_first()).strip()

                item['image_link'] = response.xpath("//img[@itemprop='image']/@src").extract_first()
                item['description'] = ' '.join([line.strip() for line in response.xpath("//div[@class='profile-statement']//text()").extract() if line.strip()])
                item['specialties'] = ', '.join([line.strip() for line in response.xpath("//ul[@class='specialties-list']//text()").extract() if line.strip()])
                item['issues'] = ', '.join([line.strip() for line in response.xpath("//h3[contains(text(),'Issues')]/following-sibling::*[1]//text()").extract() if line.strip()])
                item['mental_health'] = ', '.join([line.strip() for line in response.xpath("//h3[contains(text(),'Mental Health')]/following-sibling::*[1]//text()").extract() if line.strip()])
                item['sexuality'] = ', '.join([line.strip() for line in response.xpath("//h3[contains(text(),'Sexuality')]/following-sibling::*[1]//text()").extract() if line.strip()])
                item['link'] = self.driver.current_url

                # Qualification
                item['qualifications_years_in_practice'] = ''
                item['qualifications_school'] = ''
                item['qualifications_year_graduated'] = ''
                item['qualifications_license_and_state'] = ''
                for elem in response.xpath("//div[@class='profile-qualifications']/ul[1]/li"):
                    if elem.xpath("./strong[contains(text(),'Years in Practice:')]"):
                        item['qualifications_years_in_practice'] = ' '.join(line.strip() for line in elem.xpath("./text()").extract() if line.strip())
                    if elem.xpath("./strong[contains(text(),'School:')]"):
                        item['qualifications_school'] = ' '.join(line.strip() for line in elem.xpath("./text()").extract() if line.strip())
                    if elem.xpath("./strong[contains(text(),'Year Graduated:')]"):
                        item['qualifications_year_graduated'] = ' '.join(line.strip() for line in elem.xpath("./text()").extract() if line.strip())
                    if elem.xpath("./strong[contains(text(),'License No. and State:')]"):
                        item['qualifications_license_and_state'] = ' '.join(line.strip() for line in elem.xpath("./text()").extract() if line.strip())
                
                item['qualifications_other'] = response.xpath("//div[@class='profile-qualifications']/ul[1]//em/text()").extract_first()

                # Finances
                item['finances_avg_cost'] = ''
                item['finances_sliding_scale'] = ''
                item['finances_accepts_insurence'] = ''
                item['finances_accepted_payment_methods'] = ''
                for elem in response.xpath("//div[@class='profile-finances']/ul[1]/li"):
                    if elem.xpath("./strong[contains(text(),'Avg Cost (per session):')]"):
                        item['finances_avg_cost'] = ' '.join(line.strip() for line in elem.xpath("./text()").extract() if line.strip())
                    if elem.xpath("./strong[contains(text(),'Sliding Scale:')]"):
                        item['finances_sliding_scale'] = ' '.join(line.strip() for line in elem.xpath("./text()").extract() if line.strip())
                    if elem.xpath("./strong[contains(text(),'Accepts Insurance:')]"):
                        item['finances_accepts_insurence'] = ' '.join(line.strip() for line in elem.xpath("./text()").extract() if line.strip())
                    if elem.xpath("./strong[contains(text(),'Accepted Payment Methods:')]"):
                        item['finances_accepted_payment_methods'] = ' '.join(line.strip() for line in (' '.join(line.strip() for line in elem.xpath("./text()").extract() if line.strip())).split() if line.strip())
                
                item['finances_accepted_insurance_plans'] = ', '.join([line.strip() for line in response.xpath("//strong[contains(text(),'Accepted Insurance Plans')]/following-sibling::*[1]//text()").extract() if line.strip()])

                # Focus
                item['focus_ethnicity'] = ''
                item['focus_religious_orientation'] = ''
                item['focus_age'] = ', '.join([line.strip() for line in response.xpath("//h3[@class='spec-subcat'][contains(text(),'Age')]/following-sibling::*[1]//text()").extract() if line.strip()])
                item['focus_categories'] = ', '.join([line.strip() for line in response.xpath("//h3[contains(text(),'Categories')]/following-sibling::*[1]//text()").extract() if line.strip()])
                for elem in response.xpath("//h2[contains(text(),'Client Focus')]/following-sibling::div"):
                    if elem.xpath("./strong[contains(text(),'Ethnicity:')]"):
                        item['focus_ethnicity'] = ' '.join(line.strip() for line in elem.xpath("./span/text()").extract() if line.strip())
                    if elem.xpath("./strong[contains(text(),'Religious Orientation:')]"):
                        item['focus_religious_orientation'] = ' '.join(line.strip() for line in elem.xpath("./span/text()").extract() if line.strip())
                
                # Treatment Approach
                item['treatment_orientation'] = ', '.join([line.strip() for line in response.xpath("//h3[@class='spec-subcat'][contains(text(),'Treatment Orientation')]/following-sibling::*[1]//text()").extract() if line.strip()])
                item['treatment_momodality'] = ', '.join([line.strip() for line in response.xpath("//h3[@class='spec-subcat'][contains(text(),'Modality')]/following-sibling::*[1]//text()").extract() if line.strip()])
                yield item


            self.driver.get(page_url)
            #Selenium next page
            if len(self.driver.find_elements_by_link_text('Next'))>0:
                page_url = self.driver.find_element_by_link_text('Next').get_attribute("href");
            else:
                #If "Next page" button not exist, stop pagination
                break;
