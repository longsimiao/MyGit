# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdspiderItem(scrapy.Item):

    sku = scrapy.Field()
    # shop_name
    store = scrapy.Field()
    price = scrapy.Field()
    # 总评论
    CommentsAll = scrapy.Field()
    # 好评
    CommentsGood = scrapy.Field()
    # 追评
    CommentsAfter = scrapy.Field()
    # 中评
    CommentsGeneral = scrapy.Field()
    # 差评
    CommentsPoor = scrapy.Field()
    # 好评率
    GoodRate = scrapy.Field()
    # 中评率
    GeneralRate = scrapy.Field()
    # 差评率
    PoorRate = scrapy.Field()

