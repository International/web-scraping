# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import xlsxwriter

class AirVidPipeline(object):
    def __init__(self):
        self.workbook = xlsxwriter.Workbook('air_emails.xlsx')
        self.worksheet = self.workbook.add_worksheet('Emails')
        self.line_counter=0

    def __del__(self):
        self.workbook.close()

    def process_item(self, item, spider):
        self.worksheet.write(self.line_counter,0,item['email'])

        self.line_counter=self.line_counter+1
        return item
