# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import xlsxwriter


class MantaPipeline(object):
    def __init__(self):
        self.workbook = xlsxwriter.Workbook('MantaCompanies.xlsx')
        self.worksheet = self.workbook.add_worksheet('MantaCompanies')
        
        self.worksheet.write(0,0,"Company name")
        self.worksheet.write(0,1,"Phone")
        self.worksheet.write(0,2,"Address")
        self.line_counter=1


    def __del__(self):
        self.workbook.close()

    def process_item(self, item, spider):
        self.worksheet.write(self.line_counter,0,item['company_name'])
        self.worksheet.write(self.line_counter,1,item['phone'])
        self.worksheet.write(self.line_counter,2,item['address'])
        self.line_counter=self.line_counter+1
        return item

