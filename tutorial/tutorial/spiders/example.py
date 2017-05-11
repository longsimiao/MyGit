# -*- coding: utf-8 -*-
"""
debug: scrapy shell "https://list.jd.com/list.html?cat=9987,653,655"
save results as CSV: scrapy crawl spider_name -o data.csv
save results as JSON: scrapy crawl spider_name -o data.json
"""
import requests
import re
import json
import random
import time
from scrapy.spiders import Spider
from tutorial.items import JdspiderItem
from scrapy.selector import Selector
from scrapy.http import Request


class JdSpider(Spider):
    name = "Spider"
    allowed_domains = ["jd.com"]
    redis_key = "JDSpider:start_urls"
    start_urls = ["https://list.jd.com/list.html?cat=9987,653,655"]

    def parse(self, response):
        item = JdspiderItem()
        phones = Selector(response).xpath('//*[@id="plist"]/ul/li')
        for each in phones:
            phoneStore = each.xpath('div/div[7]/@data-shop_name').extract()
            # 获取skuId
            temp_href = each.xpath('div/div[1]/a/@href').extract()
            phoneSku = re.search('[0-9]\d*', str(temp_href)).group(0)
            # 从json中获取价格信息
            guessNumA = random.randrange(1000000, 9999999)
            json_url = 'https://p.3.cn/prices/mgets?pduid=' + str(guessNumA) \
                       + '&skuIds=J_' + phoneSku
            ju = requests.get(json_url).text
            data1 = json.loads(ju)[0]
            phonePrice = data1.get('op')
            # 从json中获取评论信息
            guessNumB = random.randrange(10000000, 99999999)
            commentsUrl = 'https://club.jd.com/comment/productComment \
                            Summaries.action?referenceIds=' \
                          + phoneSku + '&_=' + str(guessNumA)
            cu = requests.get(commentsUrl).text
            data2 = json.loads(cu).get('CommentsCount')[0]
            commentsAll = data2.get('CommentCountStr')
            commentsGood = data2.get('GoodCountStr')
            commentsAfter = data2.get('AfterCountStr')
            commentsGeneral = data2.get('GeneralCountStr')
            commentsPoor = data2.get('PoorCountStr')
            goodRate = data2.get('GoodRate')
            generalRate = data2.get('PoorRate')
            poorRate = data2.get('PoorRate')
            # item实例属性
            item['sku'] = phoneSku
            item['store'] = phoneStore
            item['price'] = phonePrice
            item['CommentsAll'] = commentsAll
            item['CommentsGood'] = commentsGood
            item['CommentsAfter'] = commentsAfter
            item['CommentsGeneral'] = commentsGeneral
            item['CommentsPoor'] = commentsPoor
            item['GoodRate'] = goodRate
            item['GeneralRate'] = generalRate
            item['PoorRate'] = poorRate
            yield item

        next_link = response.xpath('//*[@id="J_bottomPage"]/span[1]/a[10]/@href').extract()
        if next_link:
            next_link = 'https://list.jd.com' + next_link[0] + '#J_main'
            print(next_link)
            time.sleep(1)
            yield Request(next_link, callback=self.parse)


# from scrapy.spiders import CrawlSpider
# class JdSpider(CrawlSpider):
#     name = "Spider"
#     allowed_domains = ["jd.com"]
#     redis_key = "JDSpider:start_urls"
#     start_urls = ["https://list.jd.com/list.html?cat=9987,653,655"]
#
#     def parse(self, response):
#         item = JdspiderItem()
#         phones = Selector(response).xpath('//*[@id="plist"]/ul/li')
#         for each in phones:
#             phoneStore = each.xpath('div/div[7]/@data-shop_name').extract()
#             # 获取skuId
#             temp_href = each.xpath('div/div[1]/a/@href').extract()
#             phoneSku = re.search('[0-9]\d*', str(temp_href)).group(0)
#             # 从json中获取价格信息
#             guessNumA = random.randrange(1000000, 9999999)
#             json_url = 'https://p.3.cn/prices/mgets?pduid=' + str(guessNumA) \
#                        + '&skuIds=J_' + phoneSku
#             ju = requests.get(json_url).text
#             data1 = json.loads(ju)[0]
#             phonePrice = data1.get('op')
#             # 从json中获取评论信息
#             guessNumB = random.randrange(10000000, 99999999)
#             commentsUrl = 'https://club.jd.com/comment/productComment \
#                             Summaries.action?referenceIds=' \
#                           + phoneSku + '&_=' + str(guessNumA)
#             cu = requests.get(commentsUrl).text
#             data2 = json.loads(cu).get('CommentsCount')[0]
#             commentsAll = data2.get('CommentCountStr')
#             commentsGood = data2.get('GoodCountStr')
#             commentsAfter = data2.get('AfterCountStr')
#             commentsGeneral = data2.get('GeneralCountStr')
#             commentsPoor = data2.get('PoorCountStr')
#             goodRate = data2.get('GoodRate')
#             generalRate = data2.get('PoorRate')
#             poorRate = data2.get('PoorRate')
#             # item实例属性
#             item['sku'] = phoneSku
#             item['store'] = phoneStore
#             item['price'] = phonePrice
#             item['CommentsAll'] = commentsAll
#             item['CommentsGood'] = commentsGood
#             item['CommentsAfter'] = commentsAfter
#             item['CommentsGeneral'] = commentsGeneral
#             item['CommentsPoor'] = commentsPoor
#             item['GoodRate'] = goodRate
#             item['GeneralRate'] = generalRate
#             item['PoorRate'] = poorRate
#             yield item
#
#         next_link = response.xpath('//*[@id="J_bottomPage"]/span[1]/a[10]/@href').extract()
#         if next_link:
#             next_link = 'https://list.jd.com' + next_link[0] + '#J_main'
#             print(next_link)
#             time.sleep(1)
#             yield Request(next_link, callback=self.parse)