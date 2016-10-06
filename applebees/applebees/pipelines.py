# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import xlsxwriter

class ApplebeesPipeline(object):
    def __init__(self):
        self.workbook = xlsxwriter.Workbook('ApplebeesData.xlsx')
        self.worksheet = self.workbook.add_worksheet('Applebees')
        
        self.worksheet.write(0,0,"State")
        self.worksheet.write(0,1,"Location name")
        self.worksheet.write(0,2,"Region")
        self.worksheet.write(0,3,"City")
        self.worksheet.write(0,4,"Street")
        self.worksheet.write(0,5,"Postal code")
        self.worksheet.write(0,6,"Phone")
        self.worksheet.write(0,7,"Link")

        self.line_counter=1

    def __del__(self):
        self.workbook.close()

    def process_item(self, item, spider):
        self.worksheet.write(self.line_counter,0,item['state'])
        self.worksheet.write(self.line_counter,1,item['restaurant_name'])
        self.worksheet.write(self.line_counter,2,item['region'])
        self.worksheet.write(self.line_counter,3,item['city'])
        self.worksheet.write(self.line_counter,4,item['street'])
        self.worksheet.write(self.line_counter,5,item['postal'])
        self.worksheet.write(self.line_counter,6,item['phone'])
        self.worksheet.write(self.line_counter,7,item['link'])
        self.line_counter=self.line_counter+1
        return item