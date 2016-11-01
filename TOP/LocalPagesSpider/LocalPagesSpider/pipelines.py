# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import xlsxwriter

class cleanerPipeline(object):

    def process_item(self, item, spider):
        item['company_name'] = item['company_name'].strip() if item['company_name'] else None
        item['phone'] = item['phone'].strip() if item['phone'] else None
        item['address'] = ' '.join([elem.strip() for elem in item['address'] if elem.strip()]) if item['address'] else None
        return item

class xlsxPipeline(object):
    def open_spider(self, spider):
        self.workbook = xlsxwriter.Workbook('Data.xlsx')
        self.worksheet = self.workbook.add_worksheet('Data')
        
        self.worksheet.write(0,0,"Company name")
        self.worksheet.write(0,1,"Phone")
        self.worksheet.write(0,2,"Address")
        self.line_counter=1

    def close_spider(self, spider):
        self.workbook.close()

    def process_item(self, item, spider):
        self.worksheet.write(self.line_counter,0,item['company_name'])
        self.worksheet.write(self.line_counter,1,item['phone'])
        self.worksheet.write(self.line_counter,2,item['address'])
        self.line_counter=self.line_counter+1
        return item
