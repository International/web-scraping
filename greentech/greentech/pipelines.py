# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import xlsxwriter

class GreentechPipeline(object):
    def __init__(self):
        self.workbook = xlsxwriter.Workbook('Greentech.xlsx')
        self.worksheet = self.workbook.add_worksheet('GreentechCompanies')
        
        self.worksheet.write(0,0,"Company name")
        self.worksheet.write(0,1,"Email")
        self.worksheet.write(0,2,"Website")
        self.worksheet.write(0,3,"Address")
        self.worksheet.write(0,4,"Link")

        self.line_counter=1

    def __del__(self):
        self.workbook.close()

    def process_item(self, item, spider):
        self.worksheet.write(self.line_counter,0,item['company_name'])
        self.worksheet.write(self.line_counter,1,item['email'])
        self.worksheet.write(self.line_counter,2,item['website'])
        self.worksheet.write(self.line_counter,3,item['address'])
        self.worksheet.write(self.line_counter,4,item['link'])

        self.line_counter=self.line_counter+1
        return item
