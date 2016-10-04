# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import xlsxwriter


class RackspacePipeline(object):
    def __init__(self):
        self.workbook = xlsxwriter.Workbook('Rackspace.xlsx')
        self.worksheet = self.workbook.add_worksheet('Rackspace')
        
 
        self.worksheet.write(0,0,"Company name")
        self.worksheet.write(0,1,"Address")
        self.worksheet.write(0,2,"Website")
        self.worksheet.write(0,3,"Phone")
        self.worksheet.write(0,4,"Partner")
        self.worksheet.write(0,5,"Link")

        self.line_counter=1


    def __del__(self):
        self.workbook.close()

    def process_item(self, item, spider):
        
        self.worksheet.write(self.line_counter,0,item['company_name'])
        self.worksheet.write(self.line_counter,1,item['address'])
        self.worksheet.write(self.line_counter,2,item['website'])
        self.worksheet.write(self.line_counter,3,item['phone'])
        self.worksheet.write(self.line_counter,4,item['partner'])
        self.worksheet.write(self.line_counter,5,item['link'])
        self.line_counter=self.line_counter+1
        return item

