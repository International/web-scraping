# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import xlsxwriter


class ShowcasePipeline(object):
    def __init__(self):
        self.workbook = xlsxwriter.Workbook('Brockers.xlsx')
        self.worksheet = self.workbook.add_worksheet('showcase.com Brockers')
        
   
        self.line_counter=1

    def __del__(self):
        self.workbook.close()

    def process_item(self, item, spider):
	    self.worksheet.write(self.line_counter,10,item['link'])
	    self.worksheet.write(self.line_counter,0,item['brokers_name'])
	    self.worksheet.write(self.line_counter,1,item['company_name'])
	    self.worksheet.write(self.line_counter,2,item['street_address1'])
	    self.worksheet.write(self.line_counter,3,item['street_address2'])
	    self.worksheet.write(self.line_counter,4,item['city'])
	    self.worksheet.write(self.line_counter,5,item['state'])
	    self.worksheet.write(self.line_counter,6,item['zip_code'])
	    self.worksheet.write(self.line_counter,7,item['phone_number'])
	    self.worksheet.write(self.line_counter,8,item['email_address'])
	    self.worksheet.write(self.line_counter,9,item['website_address'])

	       
	    self.line_counter=self.line_counter+1
	    return item


  