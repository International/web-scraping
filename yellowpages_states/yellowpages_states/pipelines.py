# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class YellowpagesStatesPipeline(object):
    def process_item(self, item, spider):
        with open('US_CITIES.txt','a',encoding='utf-8') as links:
            links.write('[{},{},{}]\n'.format(item['state'],item['state_name'],item['city']))
            return item
