# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import xlsxwriter


class IoofPipeline(object):
    def __init__(self):
        self.workbook = xlsxwriter.Workbook('ioof.xlsx')
        self.worksheet = self.workbook.add_worksheet('ioof')
        
        self.worksheet.write(0,0,"Name")
        self.worksheet.write(0,1,"Email")
        self.worksheet.write(0,2,"Phone")
        self.worksheet.write(0,3,"Website")
        self.worksheet.write(0,4,"url")


        self.line_counter=1


    def __del__(self):
        self.workbook.close()

    def process_item(self, item, spider):
        self.worksheet.write(self.line_counter,0,item['secretary'])
        self.worksheet.write(self.line_counter,1,item['email'])
        self.worksheet.write(self.line_counter,2,item['phone'])
        self.worksheet.write(self.line_counter,3,item['webpage'])
        self.worksheet.write(self.line_counter,4,item['page_url'])
        self.line_counter=self.line_counter+1
        return item


