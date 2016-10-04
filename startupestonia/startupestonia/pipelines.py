# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import xlsxwriter


class StartupestoniaPipeline(object):
    def __init__(self):
        self.workbook = xlsxwriter.Workbook('Startups.xlsx')
        self.worksheet = self.workbook.add_worksheet('Startups')
        
        self.worksheet.write(0,0,"Startup")
        self.worksheet.write(0,1,"Email")
        self.worksheet.write(0,2,"Email Validation")
        self.worksheet.write(0,3,"Team")
        self.worksheet.write(0,4,"Role")
        self.worksheet.write(0,5,"Link")
        
        self.line_counter=1


    def __del__(self):
        self.workbook.close()

    def process_item(self, item, spider):
        self.worksheet.write(self.line_counter,0,item['name'])
        self.worksheet.write(self.line_counter,1,item['email'])
        self.worksheet.write(self.line_counter,2,item['validation'])
        self.worksheet.write(self.line_counter,5,item['link'])
        if len(item['team'])>0:
            for team_element,role_element in zip(item['team'],item['role']):
                self.worksheet.write(self.line_counter,3,team_element)
                self.worksheet.write(self.line_counter,4,role_element)
                self.line_counter=self.line_counter+1
        else:
            self.line_counter=self.line_counter+1
        
        return item
