# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class YellowpagesauPipeline(object):
    def __init__(self):
        self.workbook = xlsxwriter.Workbook('YellowpagesAU.xlsx')
        self.worksheet = self.workbook.add_worksheet('YellowpagesAU')
        
        self.worksheet.write(0,0,"Company link")
        self.worksheet.write(0,1,"Company name")
        self.worksheet.write(0,2,"Phone")
        self.worksheet.write(0,3,"Email")
        self.worksheet.write(0,4,"Website")
        self.worksheet.write(0,5,"Address")
        self.worksheet.write(0,6,"Page URL")


        self.line_counter=1

    def __del__(self):
        self.workbook.close()

    def process_item(self, item, spider):
        self.worksheet.write(self.line_counter,0,item['link'])
        self.worksheet.write(self.line_counter,1,item['name'])
        self.worksheet.write(self.line_counter,2,item['phone'])
        self.worksheet.write(self.line_counter,3,item['email'])
        self.worksheet.write(self.line_counter,4,item['address'])
        self.worksheet.write(self.line_counter,5,item['website'])
        self.worksheet.write(self.line_counter,6,item['address'])
        self.line_counter=self.line_counter+1
        return item