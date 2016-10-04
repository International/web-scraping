# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import xlsxwriter


class SimplifyemPipeline(object):
    def __init__(self):
        self.workbook = xlsxwriter.Workbook('simplifyemMajorCitiesData.xlsx')
        self.worksheet = self.workbook.add_worksheet('MajorCitiesCompanies')
        
        self.worksheet.write(0,0,"Company link")
        self.worksheet.write(0,1,"Company name")
        self.worksheet.write(0,2,"State")
        self.worksheet.write(0,3,"City")
        self.worksheet.write(0,4,"Address")
        self.worksheet.write(0,5,"Zip code")
        self.worksheet.write(0,6,"Descryption")

        self.line_counter=1


    def __del__(self):
        self.workbook.close()

    def process_item(self, item, spider):
        self.worksheet.write(self.line_counter,0,item['link'])
        self.worksheet.write(self.line_counter,1,item['company_name'])
        self.worksheet.write(self.line_counter,2,item['state'])
        self.worksheet.write(self.line_counter,3,item['city'])
        self.worksheet.write(self.line_counter,4,item['address'])
        self.worksheet.write(self.line_counter,5,item['zip_code'])
        self.worksheet.write(self.line_counter,6,item['description'])
        self.line_counter=self.line_counter+1
        return item


