#scrapy crawl idoctors -o items.json -t json

import re
import scrapy
from scrapy import Request


class TopdoctorsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    link = scrapy.Field()
    prof = scrapy.Field()
    name = scrapy.Field()
    specialization = scrapy.Field()
    photo_link = scrapy.Field()
    services = scrapy.Field()
    about = scrapy.Field()
    indentity_number = scrapy.Field()
    calendar = scrapy.Field()

    facility_name = scrapy.Field()
    facility_phone = scrapy.Field()
    facility_direct = scrapy.Field()
    option = scrapy.Field()

    spec = scrapy.Field()

class IdoctorsSpider(scrapy.Spider):
    name = "topdoctors"
    allowed_domains = ["topdoctors.it"]
    start_urls = [
        "https://www.topdoctors.it"
    ]


    def parse(self, response):
    
        urlist=[
        "http://www.topdoctors.it/specializzazione/Oculistica",
        "http://www.topdoctors.it/specializzazione/Allergologia",
        "http://www.topdoctors.it/specializzazione/Andrologia",
        "http://www.topdoctors.it/specializzazione/Angiologia ",
        "http://www.topdoctors.it/specializzazione/audiologia-foniatria",
        "http://www.topdoctors.it/specializzazione/Cardiochirurgia",
        "http://www.topdoctors.it/specializzazione/Cardiologia",
        "http://www.topdoctors.it/specializzazione/Cardiologia-pediatrica",
        "http://www.topdoctors.it/specializzazione/Chirurgia-generale",
        "http://www.topdoctors.it/specializzazione/Chirurgia-Maxillo-facciale",
        "http://www.topdoctors.it/specializzazione/Chirurgia-Pediatrica",
        "http://www.topdoctors.it/specializzazione/Chirurgia-plastica-e-estetica",
        "http://www.topdoctors.it/specializzazione/Chirurgia-toracica",
        "http://www.topdoctors.it/specializzazione/Chirurgia-vascolare",
        "http://www.topdoctors.it/specializzazione/Colonproctologia",
        "http://www.topdoctors.it/specializzazione/Dermatologia ",
        "http://www.topdoctors.it/specializzazione/Diabetologia",
        "http://www.topdoctors.it/specializzazione/Ematologia",
        "http://www.topdoctors.it/specializzazione/endocrinologia e-malattie-del-metabolismo",
        "http://www.topdoctors.it/specializzazione/Gastroenterologia",
        "http://www.topdoctors.it/specializzazione/Geriatria-e-Gerontologia",
        "http://www.topdoctors.it/specializzazione/Ginecologia-e-Ostetricia",
        "http://www.topdoctors.it/specializzazione/malattie-infettive-especialidad",
        "http://www.topdoctors.it/specializzazione/medicina-dello-sport",
        "http://www.topdoctors.it/specializzazione/Medicina-estetica",
        "http://www.topdoctors.it/specializzazione/Medicina-Fisica-e-Riabilitazione",
        "http://www.topdoctors.it/specializzazione/Medicina-interna",
        "http://www.topdoctors.it/specializzazione/Nefrologia",
        "http://www.topdoctors.it/specializzazione/Neurochirurgia",
        "http://www.topdoctors.it/specializzazione/Neurologia",
        "http://www.topdoctors.it/specializzazione/Odontoiatria",
        "http://www.topdoctors.it/specializzazione/Oncologia",
        "http://www.topdoctors.it/specializzazione/Ortopedia-e-Traumatologia ",
        "http://www.topdoctors.it/specializzazione/Ortopedia-pediatrica",
        "http://www.topdoctors.it/specializzazione/Otorinolaringoiatria",
        "http://www.topdoctors.it/specializzazione/Pediatria",
        "http://www.topdoctors.it/specializzazione/Pneumologia-e-Malattie-Respiratorie",
        "http://www.topdoctors.it/specializzazione/Procreazione-assistita",
        "http://www.topdoctors.it/specializzazione/Psichiatria",
        "http://www.topdoctors.it/specializzazione/Psicologia",
        "http://www.topdoctors.it/specializzazione/Radiologia",
        "http://www.topdoctors.it/specializzazione/Radioterapia",
        "http://www.topdoctors.it/specializzazione/Reumatologia",
        "http://www.topdoctors.it/specializzazione/scienze-dell-alimentazione",
        "http://www.topdoctors.it/specializzazione/terapia-del-dolore-especialidad",
        "http://www.topdoctors.it/specializzazione/Urologia"
        ]

        for url in urlist:
            yield Request(url, callback=self.parse_page) 

  
        
    def parse_page(self, response):
        print(response.url)
        for link in response.xpath("//a[@class='demi']/@href"):
            url = response.urljoin(link.extract())
            #Test url
            #url = 'http://www.topdoctors.it/dottor/valerio-sansone'
            yield Request(url, callback=self.parse_doctor) 

        #Pagination
        for page in response.xpath("//div[@class='next']/a[@id='flecha_siguiente_pagina']/@href"):
            url = response.urljoin(page.extract())
            yield Request(url, callback=self.parse_page)    


    def parse_doctor(self, response):
        item = TopdoctorsItem()

        item['link'] = response.request.url
        item['prof'] = response.xpath("//span[@itemprop='name']/text()").extract_first().split()[0]
        item['name'] = (response.xpath("//span[@itemprop='name']/text()").extract_first()).replace(item['prof'],'').strip()
        item['specialization'] = (response.xpath("//span[@itemprop='jobTitle']/text()").extract_first()).strip()
        item['photo_link'] = response.urljoin(response.xpath("//div[@class='image_perfil_over']/a[1]/@href").extract_first())
        item['services'] = ''.join([elem.strip()+';' for elem in response.xpath("//div[@id='ficha_experto_en_doctor']//a/text()").extract()])
        item['about'] = ''.join(response.xpath("//div[@id='texto_primer_nivel_corto']//*/text()").extract())
        if response.xpath("//div[@id='top_articulos']//li[3]//span[@itemprop='title']"):
            item['spec'] = (response.xpath("//div[@id='top_articulos']//li[3]//span[@itemprop='title']/text()").extract_first()).strip() 
        else:
            item['spec'] = ''
        if response.xpath("//p[@id='num_colegiado']"):
            item['indentity_number'] = (response.xpath("//p[@id='num_colegiado']/text()").extract_first()).strip()
        else:
            item['indentity_number'] = ''
        if response.xpath("//div[@class='valor_comment']"):
            item['option'] = ''.join([elem.strip()+';' for elem in response.xpath("//div[@class='valor_comment']/text()").extract()])
        else:
            item['option'] = ''
        
        if response.xpath("//div[@class='infomed_dr_view_right']/form"):
            item['calendar'] = len(response.xpath("//div[@class='infomed_dr_view_right']/form").extract())
            #If exist calendar form and item_clinica
            if response.xpath("//div[@id='ficha_clinicas']/div[@class='item_clinica']"):
                #Get popup url
                url = response.xpath("//div[@id='ficha_clinicas']/div[@class='item_clinica']//a/@href").extract_first()
                #Request information from popup
                yield Request(url, callback=self.parse_popup, meta={'item': item})  
        else:
            item['calendar'] = ''
            item['facility_name'] = response.xpath("//p[@class='nombre_clinica negrita']/text()").extract_first()
            item['facility_phone'] = ''
            item['facility_direct'] = response.xpath("//span[@itemprop='streetAddress']/p/text()").extract_first()
            yield item
        


    def parse_popup(self, response):
        item = response.meta['item']
        item['facility_name'] = response.xpath("//select[@id='address_cita_popup']/option/text()").extract_first()
        item['facility_phone'] = response.xpath("//div[@id='contenedor_direcciones']//a[@class='telefono']/text()").extract_first()
        item['facility_direct'] = response.xpath("//div[@id='contenedor_direcciones']/div/p[@class='direccion']/text()").extract_first()
        yield item
