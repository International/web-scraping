# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import xlsxwriter


class UsineDegitalePipeline(object):
    def __init__(self):
        self.workbook = xlsxwriter.Workbook('Startups.xlsx')
        self.worksheet = self.workbook.add_worksheet('usine-digitale.fr')
        
   
        self.line_counter=1

    def __del__(self):
        self.workbook.close()

    def process_item(self, item, spider):
        
        self.worksheet.write(self.line_counter,0,item['name'])
        self.worksheet.write(self.line_counter,1,item['ceo'])
        self.worksheet.write(self.line_counter,2,item['city'])
        self.worksheet.write(self.line_counter,3,item['phone'])
        self.worksheet.write(self.line_counter,4,item['website'])
        self.worksheet.write(self.line_counter,5,item['email'])
        self.worksheet.write(self.line_counter,6,item['link'])

        
           
        self.line_counter=self.line_counter+1
        return item

