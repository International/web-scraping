#scrapy crawl yellowpages_states -o items.json -t json
import scrapy
import string

'''
Scrap state, state name and city from yellowpages.com
Example:
    {'city': 'Ashby', 'state': 'MA', 'state_name': 'Massachusetts'}
    {'city': 'Mount Washington', 'state': 'MA', 'state_name': 'Massachusetts'}
'''

class YellowpagesStatesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    state = scrapy.Field()
    state_name = scrapy.Field()
    city = scrapy.Field()

class YellowpagesStatesSpider(scrapy.Spider):
    name = "yellowpages_states"
    allowed_domains = ["yellowpages.com"]

    start_urls = ["http://www.yellowpages.com/sitemap"]

    def parse(self, response):
        for state in response.xpath("//div[contains(section/h2/text(),'Local Yellow Pages')]//a"):
            url = response.urljoin(state.xpath("@href").extract_first())
            
            item = YellowpagesStatesItem()
            item['state'] = ((state.xpath("@href").extract_first()).split('-')[-1]).upper()
            item['state_name'] = state.xpath("text()").extract_first()

            yield scrapy.Request(url, meta={'item': item}, callback=self.parse_state)      

    def parse_state(self, response):
        for letter in string.ascii_lowercase:
            url = response.urljoin('?page='+letter)
            yield scrapy.Request(url, meta={'item': response.meta['item']}, callback=self.get_cities)

    def get_cities(self, response):
        for city in response.xpath("//div[contains(section/h2/text(),'Cities')]//a/text()"):
            item = response.meta['item']
            item['city'] = city.extract()
            yield item
