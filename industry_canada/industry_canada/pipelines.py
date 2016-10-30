# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import string
import xlsxwriter


class IndustryCanadaPipeline(object):

    def process_item(self, item, spider):
        item['company_name'] = item['company_name'].strip() if item['company_name'] else None
        try:
            address = [elem.strip() for elem in item['address'] if elem.strip()] if item['address'] else None
            item['address'] = ' '.join([elem.strip() for elem in ' '.join(address).split() if elem.strip()])
        except:
            item['address'] = None
        try:
            item['postal_code'] = address.pop()
        except:
            item['postal_code'] = None
        try:
            city_province = address.pop()
            item['city'] = city_province.split(',')[0].strip()
            item['province'] = city_province.split(',')[-1].strip()
        except:
            item['city'] = None
            item['province'] = None
        try:   
            item['street'] = ' '.join(address)
        except:
            item['street'] = None
        item['company_phone'] = ', '.join(elem.strip() for elem in item['company_phone'] if elem.strip()) if item['company_phone'] else None
        item['company_website'] = item['company_website'].strip() if item['company_website'] else None
        item['company_email'] = item['company_email'].strip().replace('mailto:','') if item['company_email'] else None

        item['description'] = item['description'].strip() if item['description'] else None
        item['year_established'] = item['year_established'].strip() if item['year_established'] else None
        item['primary_industry'] = item['primary_industry'].strip() if item['primary_industry'] else None
        item['employee'] = item['employee'].strip() if item['employee'] else None
        try:
            item['contact_name'] = ' '.join(elem.strip() for elem in (' '.join([elem.strip() for elem in item['contact_name'] if elem.strip()])).split())
        except:
            item['contact_name'] = None
        try:
            item['contact_title'] = ', '.join([elem.strip() for elem in item['contact_title'] if elem.strip()])
        except:
            item['contact_title'] = None
        try:
            item['contact_email'] = ', '.join([elem.strip() for elem in item['contact_email'] if elem.strip()])
        except:
            item['contact_email'] = None
        try:
            item['contact_phone'] = ', '.join([elem.strip() for elem in item['contact_phone'] if elem.strip()])
        except:
            item['contact_phone'] = None   
        return item


class xlsxPipeline(object):

    def open_spider(self, spider):
        self.workbook = xlsxwriter.Workbook('Data.xlsx')
        self.worksheet = self.workbook.add_worksheet('Data')
        self.worksheet.write(0,0,"Company name")
        self.worksheet.write(0,1,"Full Address")
        self.worksheet.write(0,2,"Address")
        self.worksheet.write(0,3,"City")
        self.worksheet.write(0,4,"Province")
        self.worksheet.write(0,5,"Postal Code")
        self.worksheet.write(0,6,"Phone")
        self.worksheet.write(0,7,"Website")
        self.worksheet.write(0,8,"Description")
        self.worksheet.write(0,9,"Year Established")
        self.worksheet.write(0,10,"Primary Industry (NAICS)")
        self.worksheet.write(0,11,"Number of Employees")
        self.worksheet.write(0,12,"Contact Name")
        self.worksheet.write(0,13,"Title")
        self.worksheet.write(0,14,"Email")
        self.worksheet.write(0,15,"Phone")
        self.worksheet.write(0,16,"Industry Canada URL")
        self.line_counter=1

    def close_spider(self, spider):
        self.workbook.close()

    def process_item(self, item, spider):
        self.worksheet.write(self.line_counter,0,item['company_name'])
        self.worksheet.write(self.line_counter,1,item['address'])
        self.worksheet.write(self.line_counter,2,item['street'])
        self.worksheet.write(self.line_counter,3,item['city'])
        self.worksheet.write(self.line_counter,4,item['province'])
        self.worksheet.write(self.line_counter,5,item['postal_code'])
        self.worksheet.write(self.line_counter,6,item['company_phone'])
        self.worksheet.write(self.line_counter,7,item['company_website'])
        self.worksheet.write(self.line_counter,8,item['description'])
        self.worksheet.write(self.line_counter,9,item['year_established'])
        self.worksheet.write(self.line_counter,10,item['primary_industry'])
        self.worksheet.write(self.line_counter,11,item['employee'])
        self.worksheet.write(self.line_counter,12,item['contact_name'])
        self.worksheet.write(self.line_counter,13,item['contact_title'])
        self.worksheet.write(self.line_counter,14,item['contact_email'])
        self.worksheet.write(self.line_counter,15,item['contact_phone'])
        self.worksheet.write(self.line_counter,16,item['URL'])
        self.line_counter=self.line_counter+1
        return item