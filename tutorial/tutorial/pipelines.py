# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class TutorialPipeline(object):
    """
    CREATE TABLE scrapy_spider (
    id BIGINT(7) NOT NULL AUTO_INCREMENT,
    'sku' varchar(500),
    'store' varchar(500),
    'price' varchar(500),
    'CommentsAll' varchar(500),
    'CommentsGood' varchar(500),
    'CommentsAfter' varchar(500),
    'CommentsGeneral' varchar(500),
    'CommentsPoor' varchar(500),
    'GoodRate' varchar(500),
    'GeneralRate' varchar(500),
    'PoorRate' varchar(500)
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(id)
    )CHARACTER SET=utf8;
    """
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', user='root',
                                    passwd='root', db="mytest", charset='utf8')

    def process_item(self, item, spider):
        if item['PhoneID'] in self.ids_seen:
            print("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['PhoneID'])
            return item

