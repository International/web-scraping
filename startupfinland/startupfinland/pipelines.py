# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import xlsxwriter

class StartupfinlandPipeline(object):
    
    def __init__(self):
        self.workbook = xlsxwriter.Workbook('Startups.xlsx')
        self.worksheet = self.workbook.add_worksheet('Startups')
        
        self.worksheet.write(0,0,"Startup")
        self.worksheet.write(0,1,"Email")
        self.worksheet.write(0,2,"1st Team member")
        self.worksheet.write(0,3,"Role")
        self.worksheet.write(0,4,"Link")
        self.worksheet.write(0,5,"Validation")
        self.line_counter=1

    def __del__(self):
        self.workbook.close()

    def process_item(self, item, spider):
        self.worksheet.write(self.line_counter,0,item['name'])
        self.worksheet.write(self.line_counter,1,item['email'])
        self.worksheet.write(self.line_counter,2,item['team'])
        self.worksheet.write(self.line_counter,3,item['role'])
        self.worksheet.write(self.line_counter,4,item['link'])
        self.worksheet.write(self.line_counter,5,item['validation'])
        self.line_counter=self.line_counter+1
        return item
