#scrapy crawl yellowpages -o items.json -t json

import scrapy


class YellowpagesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    raiting_value = scrapy.Field()
    review_count = scrapy.Field()

    street_address = scrapy.Field()
    locality_address = scrapy.Field()
    region_address = scrapy.Field()
    postal_code = scrapy.Field()
    country_address = scrapy.Field()
    phone = scrapy.Field()

    website = scrapy.Field()
    email = scrapy.Field()
    slogan = scrapy.Field()


class YellowpagesSpider(scrapy.Spider):
    name = "yellowpages"
    allowed_domains = ["yellowpages.com"]
    start_urls = ["http://www.yellowpages.com/search?search_terms=Veterinary+Clinics+%26+Hospitals&geo_location_terms=Hollywood%2C+FL"]

    def parse(self, response):
        for company_link in response.xpath("//div[@id='main-content']//div[@class='info']/h3/a/@href"):
            url = response.urljoin(company_link.extract())
            yield scrapy.Request(url, callback=self.parse_company_info)      
        
        #pagination
        next_page=response.xpath("//div[@class='pagination']/ul/li/a[@class='next ajax-page']/@href")
        url = response.urljoin(next_page.extract_first())
        yield scrapy.Request(url, self.parse)


    def parse_company_info(self, response):
        item = YellowpagesItem()

        item['title']=response.xpath("//div[@class='business-card-wrapper']//h1[@itemprop='name']/text()").extract()
        item['raiting_value']=response.xpath("//div[@class='business-card-wrapper']//meta[@itemprop='ratingValue']/@content").extract()
        item['review_count']=response.xpath("//div[@class='business-card-wrapper']//span[@itemprop='reviewCount']/text()").extract()

        item['street_address']=response.xpath("//div[@class='business-card-wrapper']//div[@class='contact']//div[@itemprop='address']//p[@itemprop='streetAddress']/text()").extract()
        item['locality_address']=response.xpath("//div[@class='business-card-wrapper']//div[@class='contact']//div[@itemprop='address']//span[@itemprop='addressLocality']/text()").extract()
        item['region_address']=response.xpath("//div[@class='business-card-wrapper']//div[@class='contact']//div[@itemprop='address']//span[@itemprop='addressRegion']/text()").extract()
        item['postal_code']=response.xpath("//div[@class='business-card-wrapper']//div[@class='contact']//div[@itemprop='address']//span[@itemprop='postalCode']/text()").extract()
        item['country_address']=response.xpath("//div[@class='business-card-wrapper']//div[@class='contact']//div[@itemprop='address']//meta[@itemprop='addressCountry']/@content").extract()

        item['phone']=response.xpath("//div[@class='business-card-wrapper']//div[@class='contact']//p[@itemprop='telephone']/text()").extract()
        item['website']=response.xpath("//div[@class='business-card-wrapper']//a[@class='custom-link']/@href").extract()
        item['email']=response.xpath("//div[@class='business-card-wrapper']//a[@class='email-business']/@href").extract()
        item['slogan']=response.xpath("//section[@id='business-details']/div[@class='slogan']/text()").extract()

        yield item