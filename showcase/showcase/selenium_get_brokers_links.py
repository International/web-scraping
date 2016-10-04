from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC




def isElementPresent(driver, XPATH):
    if len(driver.find_elements_by_xpath(XPATH))>0:
        return True
    else:
        return False

def enterProperties(driver,form_xpath,home_xpath):
    #Captcha detection
    if isElementPresent(driver,form_xpath):
        #Waiting captcha entering
        WebDriverWait(driver, 10000).until(EC.presence_of_element_located((By.XPATH,home_xpath)))
        return True
    return False


#Chrome proxy
'''
PROXY = "206.128.159.17:3128" # IP:PORT or HOST:PORT
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=%s' % PROXY)
driver = webdriver.Chrome(executable_path='F:/MyGitHub/Scraping/showcase/showcase/spiders/chromedriver/chromedriver.exe',chrome_options=chrome_options)
'''
#206.128.159.17:3128
#174.129.204.124:80
#173.192.21.89:8080
  

## get the Firefox profile object
profile = webdriver.FirefoxProfile() 
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

driver = webdriver.Firefox(firefox_profile=profile)

driver.get("http://www.showcase.com")

#CheckBox
office = driver.find_element_by_xpath("//table[@class='cbx-list']//tr[1]/td[1]/input");
office.click()
#CheckBox
industrial = driver.find_element_by_xpath("//table[@class='cbx-list']//tr[2]/td[1]/input");
industrial.click()
#Round
lease = driver.find_element_by_xpath("//table[@class='rbn-list']//tr[1]/td[1]/input");
lease.click()



enterProperties(driver,"//div[@class='frm-search']","//div[@id='divSearchResults']");
enterProperties(driver,"//div[@class='frm-search']","//div[@id='divSearchResults']");



#Disable scroll pagination (Don't know why it works)
driver.find_element_by_xpath("//div[@id='divMainResultsGrid']").send_keys(Keys.PAGE_DOWN)
driver.find_element_by_xpath("//div[@id='divMainResultsGrid']").send_keys(Keys.PAGE_DOWN)
driver.find_element_by_xpath("//div[@id='divMainResultsGrid']").send_keys(Keys.PAGE_DOWN)
driver.find_element_by_xpath("//div[@id='divMainResultsGrid']").send_keys(Keys.PAGE_DOWN)


urls=[]
while True:
    try:
        for link in driver.find_elements_by_xpath("//a[@class='lnkBrokerName']"):
            url=link.get_attribute("href")
            if url not in urls:
                urls.append(url)
                print(len(urls),"   ",url,"  ",driver.find_element_by_xpath("//span[@class='PageNavigationSelectedPage']").text)
                
            
        #Selenium pagination
        if len(driver.find_elements_by_xpath("//div[@id='divNext']/input"))>0:
            driver.find_element_by_xpath("//div[@id='divNext']/input").click()
        else:
            #If "Next page" button not exist, stop pagination
            break;

        #Save url list to file
        with open("PortlandOR.txt", 'w') as f:
            for url in list(urls):
                f.write(url + '\n')

    except:
            driver.implicitly_wait(1) 


