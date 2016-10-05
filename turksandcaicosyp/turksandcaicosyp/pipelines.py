# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3

class TurksandcaicosypPipeline(object):

    def __init__(self):
        self.conn = sqlite3.connect('Turksandcaicosyp.sqlite')
        self.cursor = self.conn.cursor()

        # Create teble
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Turksandcaicosyp_table
                    (name text, phone text, area text)''')

    def __del__(self):
        # Save (commit) the changes
        self.conn.commit()

        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        self.conn.close()

    def process_item(self, item, spider):
        try:
            self.cursor.executemany('INSERT INTO Turksandcaicosyp_table VALUES (?,?,?)',[(item['name'], item['phone'], item['area'])])
        except:
            print('Failed to insert item')
        return item


