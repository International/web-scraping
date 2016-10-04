# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import xlsxwriter

class IdoctorsPipeline(object):
    def __init__(self):
        self.workbook = xlsxwriter.Workbook('Doctors.xlsx')
        self.worksheet = self.workbook.add_worksheet('idoctors')
        
        self.worksheet.write(0,0,"Prof")
        self.worksheet.write(0,1,"Name")
        self.worksheet.write(0,2,"Specialization")
        self.worksheet.write(0,3,"Photo")
        self.worksheet.write(0,4,"Calendar")
        self.worksheet.write(0,5,"Link")
        self.line_counter=1

    def __del__(self):
        self.workbook.close()

    def process_item(self, item, spider):
        self.worksheet.write(self.line_counter,0,item['prof'])
        self.worksheet.write(self.line_counter,1,item['name'])
        self.worksheet.write(self.line_counter,2,item['specialization'])
        self.worksheet.write(self.line_counter,3,item['photo_link'])
        self.worksheet.write(self.line_counter,4,item['calendar'])
        self.worksheet.write(self.line_counter,5,item['link'])
        self.line_counter=self.line_counter+1
        return item
