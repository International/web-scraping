# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import xlsxwriter
class AdvanceautopartsPipeline(object):

    def open_spider(self):
        self.workbook = xlsxwriter.Workbook('Advanceautoparts.xlsx')
        self.worksheet = self.workbook.add_worksheet('Advanceautoparts')

        self.worksheet.write(0,0,"Name")
        self.worksheet.write(0,1,"Store Number")
        self.worksheet.write(0,2,"Street")
        self.worksheet.write(0,3,"City")
        self.worksheet.write(0,4,"Region")
        self.worksheet.write(0,5,"Postal Code")
        self.worksheet.write(0,6,"Country")
        self.worksheet.write(0,7,"telephone")
        self.worksheet.write(0,8,"Store Link")
        self.line_counter=1

    def close_spider(self):
        self.workbook.close()

    def process_item(self, item, spider):
        self.worksheet.write(self.line_counter,0,item['shopName'])
        self.worksheet.write(self.line_counter,1,item['shopNumber'])
        self.worksheet.write(self.line_counter,2,item['streetAddress'])
        self.worksheet.write(self.line_counter,3,item['addressLocality'])
        self.worksheet.write(self.line_counter,4,item['addressRegion'])
        self.worksheet.write(self.line_counter,5,item['postalCode'])
        self.worksheet.write(self.line_counter,6,item['addressCountry'])
        self.worksheet.write(self.line_counter,7,item['telephone'])
        self.worksheet.write(self.line_counter,8,item['storeLink'])
        self.line_counter=self.line_counter+1

        return item