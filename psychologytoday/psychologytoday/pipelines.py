# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import xlsxwriter

class PsychologytodayPipeline(object):
    def __init__(self):
        self.workbook = xlsxwriter.Workbook('Psychologytoday.xlsx')
        self.worksheet = self.workbook.add_worksheet('Psychologytoday')
        
        self.worksheet.write(0,0,"Name")
        self.worksheet.write(0,1,"Terapist type")
        self.worksheet.write(0,2,"Phone")

        # Address
        self.worksheet.write(0,3,"Full Address")
        self.worksheet.write(0,4,"City")
        self.worksheet.write(0,5,"Postal code")
        self.worksheet.write(0,6,"Street")

        self.worksheet.write(0,7,"Image link")
        self.worksheet.write(0,8,"Description")

        # Specialities
        self.worksheet.write(0,9,"Specialties")
        self.worksheet.write(0,10,"Issues")
        self.worksheet.write(0,11,"Mental health")
        self.worksheet.write(0,12,"Sexuality")
        
        # Qualification
        self.worksheet.write(0,13,"Qualifications Years in practice")
        self.worksheet.write(0,14,"Qualifications School")
        self.worksheet.write(0,15,"Qualifications Year graduated")
        self.worksheet.write(0,16,"Qualifications License and state")
        self.worksheet.write(0,17,"Qualifications Additional line")
        # Finances
        self.worksheet.write(0,18,"Finances Avg_cost")
        self.worksheet.write(0,19,"Finances Sliding scale")
        self.worksheet.write(0,20,"Finances Accepts insurence")
        self.worksheet.write(0,21,"Finances Accepted payment methods")
        self.worksheet.write(0,22,"Finances Accepted insurance plans")
        # Focus
        self.worksheet.write(0,23,"Focus Age")
        self.worksheet.write(0,24,"Focus Categories")
        self.worksheet.write(0,25,"Focus Ethnicity")
        self.worksheet.write(0,26,"Focus Religious orientation")

        # Treatment Approach
        self.worksheet.write(0,27,"Treatment orientation")
        self.worksheet.write(0,28,"Treatment momodality")

        self.worksheet.write(0,29,"URL link")

        self.line_counter=1

    def __del__(self):
        self.workbook.close()

    def process_item(self, item, spider):
        self.worksheet.write(self.line_counter,0,item['name'])
        self.worksheet.write(self.line_counter,1,item['terapist_type'])
        self.worksheet.write(self.line_counter,2,item['phone'])

        self.worksheet.write(self.line_counter,3,item['address'])
        self.worksheet.write(self.line_counter,4,item['city'])
        self.worksheet.write(self.line_counter,5,item['postal_code'])
        self.worksheet.write(self.line_counter,6,item['street_address'])

        self.worksheet.write(self.line_counter,7,item['image_link'])
        self.worksheet.write(self.line_counter,8,item['description'])

        self.worksheet.write(self.line_counter,9,item['specialties'])
        self.worksheet.write(self.line_counter,10,item['issues'])
        self.worksheet.write(self.line_counter,11,item['mental_health'])
        self.worksheet.write(self.line_counter,12,item['sexuality'])
        

        # Qualification
        self.worksheet.write(self.line_counter,13,item['qualifications_years_in_practice'])
        self.worksheet.write(self.line_counter,14,item['qualifications_school'])
        self.worksheet.write(self.line_counter,15,item['qualifications_year_graduated'])
        self.worksheet.write(self.line_counter,16,item['qualifications_license_and_state'])
        self.worksheet.write(self.line_counter,17,item['qualifications_other'])
        # Finances
        self.worksheet.write(self.line_counter,18,item['finances_avg_cost'])
        self.worksheet.write(self.line_counter,19,item['finances_sliding_scale'])
        self.worksheet.write(self.line_counter,20,item['finances_accepts_insurence'])
        self.worksheet.write(self.line_counter,21,item['finances_accepted_payment_methods'])
        self.worksheet.write(self.line_counter,22,item['finances_accepted_insurance_plans'])
        # Focus
        self.worksheet.write(self.line_counter,23,item['focus_age'])
        self.worksheet.write(self.line_counter,24,item['focus_categories'])
        self.worksheet.write(self.line_counter,25,item['focus_ethnicity'])
        self.worksheet.write(self.line_counter,26,item['focus_religious_orientation'])

        # Treatment Approach
        self.worksheet.write(self.line_counter,27,item['treatment_orientation'])
        self.worksheet.write(self.line_counter,28,item['treatment_momodality'])

        self.worksheet.write(self.line_counter,29,item['link'])
        self.line_counter=self.line_counter+1
        return item