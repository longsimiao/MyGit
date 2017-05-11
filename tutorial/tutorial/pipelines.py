# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from openpyxl import Workbook


class TutorialPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['PhoneID'] in self.ids_seen:
            print("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['PhoneID'])
            return item

