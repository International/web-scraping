# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import xlsxwriter

import re
class TopdoctorsPipeline(object):
    def __init__(self):
        self.workbook = xlsxwriter.Workbook('Topdoctors.xlsx')
        self.worksheet = self.workbook.add_worksheet('Topdoctors')
        
        #A Prefix
        self.worksheet.write(0,0,"Prefix")
        #B Full Name
        self.worksheet.write(0,1,"Full Name")
        #C Specialization
        self.worksheet.write(0,2,"Specialization")
        #D Direct url to photo
        self.worksheet.write(0,3,"Direct url")
        #E Services (splitted with ;)
        self.worksheet.write(0,4,"Services")
        #F About me
        self.worksheet.write(0,5,"About me")
        #G Doctor indentity number
        self.worksheet.write(0,6,"indentity number")
        #H Number of calendars
        self.worksheet.write(0,7,"Number of calendars")
        #I Facility name
        self.worksheet.write(0,8,"Facility name")
        #J Street name
        self.worksheet.write(0,9,"Street name")
        #K City name
        self.worksheet.write(0,10,"City name")
        #L Post code
        self.worksheet.write(0,11,"Post code")
        #M Province name
        self.worksheet.write(0,12,"Province name")
        #N Phone number
        self.worksheet.write(0,13,"Phone number")
        #O Opinion
        self.worksheet.write(0,14,"Opinion")
        #P Opinion
        self.worksheet.write(0,15,"link")
        self.line_counter=1

    def __del__(self):
        self.workbook.close()

    def process_item(self, item, spider):

        def isfloat(value):
            try:
                float(value)
                return True
            except ValueError:
                return False
    


        self.worksheet.write(self.line_counter,15,item['link'])
        self.worksheet.write(self.line_counter,0,item['prof'])
        self.worksheet.write(self.line_counter,1,item['name'])
        self.worksheet.write(self.line_counter,2,item['specialization'])
        self.worksheet.write(self.line_counter,3,item['photo_link'])
        self.worksheet.write(self.line_counter,4,item['services'])
        self.worksheet.write(self.line_counter,5,item['about'])
        self.worksheet.write(self.line_counter,6,item['indentity_number'])
        self.worksheet.write(self.line_counter,7,item['calendar'])
        self.worksheet.write(self.line_counter,8,item['facility_name'])
        #Opinion
        self.worksheet.write(self.line_counter,14,' ')
        

    
        if '|' not in item['facility_direct']:
            street = item['facility_direct'].replace(item['facility_direct'].split('.')[-1],'') 
            self.worksheet.write(self.line_counter,9,street)
            postcode = re.sub("\D", "", item['facility_direct'].split('.')[-1]).strip()
            city =  item['facility_direct'].split('.')[-1].replace(postcode,'').strip()
            city = city.replace('Italia','').strip()
            self.worksheet.write(self.line_counter,10,city)
            self.worksheet.write(self.line_counter,11,postcode)
            self.worksheet.write(self.line_counter,12,'')
        else:
            street = item['facility_direct'].replace(item['facility_direct'].split(',')[-1],'') 
            city =  item['facility_direct'].split('|')[0].replace(street,'').strip()
            city = city.replace('Italia','').strip()
            postcode = re.sub("\D", "", item['facility_direct'].split('|')[-1]).strip()
            if isfloat(city):
                street = street+' '+city
                city = ''
            self.worksheet.write(self.line_counter,10,city)
            self.worksheet.write(self.line_counter,9,street)
            self.worksheet.write(self.line_counter,11,postcode)

            province = ((item['facility_direct'].split('|')[-1]).replace(postcode,'')).replace('-','').strip()
            province = province.replace('Italia','').strip()
            self.worksheet.write(self.line_counter,12,province)

        self.worksheet.write(self.line_counter,13,item['facility_phone'])    
        self.worksheet.write(self.line_counter,14,item['option'])
        self.worksheet.write(self.line_counter,15,item['link']) 
        self.worksheet.write(self.line_counter,16,item['facility_direct']) 
        self.worksheet.write(self.line_counter,17,item['spec']) 
        
        self.line_counter=self.line_counter+1
        return item


  