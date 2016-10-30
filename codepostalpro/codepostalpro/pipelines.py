# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import xlsxwriter
class xlsxPipeline(object):

    def open_spider(self):
        self.workbook = xlsxwriter.Workbook('Codepostalpro.xlsx')
        self.worksheet = self.workbook.add_worksheet('Codepostalpro')

        self.worksheet.write(0,0,"Region")
        self.worksheet.write(0,1,"City")
        self.worksheet.write(0,2,"Area")
        self.worksheet.write(0,3,"Post code")
        self.worksheet.write(0,4,"Latitude")
        self.worksheet.write(0,5,"Longitude")
        self.worksheet.write(0,6,"Latitude_decoded")
        self.worksheet.write(0,7,"Longitude_decoded")
        self.worksheet.write(0,8,"URL")
        self.worksheet.write(0,9,"latitude_url")
        self.worksheet.write(0,10,"longitude_url")

        self.line_counter=1

    def close_spider(self):
        self.workbook.close()

    def process_item(self, item, spider):
        self.worksheet.write(self.line_counter,0,item['region'])
        self.worksheet.write(self.line_counter,1,item['city'])
        self.worksheet.write(self.line_counter,2,item['area'])
        self.worksheet.write(self.line_counter,3,item['post_code'])
        self.worksheet.write(self.line_counter,4,item['latitude'])
        self.worksheet.write(self.line_counter,5,item['longitude'])
        self.worksheet.write(self.line_counter,6,item['latitude_decoded'])
        self.worksheet.write(self.line_counter,7,item['longitude_decoded'])
        self.worksheet.write(self.line_counter,8,item['URL'])
        self.worksheet.write(self.line_counter,9,item['latitude_url'])
        self.worksheet.write(self.line_counter,10,item['longitude_url'])
        self.line_counter=self.line_counter+1

        return item