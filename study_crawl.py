import requests
import re
import random
import datetime
from bs4 import BeautifulSoup
from urllib.request import urlopen
import json

random.seed(datetime.datetime.now())
url = "https://list.jd.com/list.html?cat=9987,653,655"
headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep - alive',
            'Host': 'github.com',
            'Referer': 'https://github.com/racaljk/hosts',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/55.0.2883.9 Safari/537.36'
            }
# 请求页面,内存对象
req_content = urlopen(url)

# 获取页面内容，并解析
html_content = BeautifulSoup(req_content.read(), "html.parser")  # lxml

# get phone lists
phone_lists = html_content.findAll("li", {"class": "gl-item"})

# get shop
shop_lists = html_content.findAll("div", {"class": "p-shop"})
i = 0

# shop["data-shop_name"] = shop_name
for shop in shop_lists:
    i += 1
    print(shop)
    # print(i, "-", shop["data-shop_name"])
    break

# get sku lists
sku_lists = html_content.findAll("div", {"class": "j-sku-item"})
# sku_num["data-sku"] = sku
for sku_num in sku_lists:
    i += 1
    sku = sku_num["data-sku"]

    # requests url for json price
    json_price_url = 'https://p.3.cn/prices/mgets?skuIds=J_' + sku
    # get json price data
    json_price = requests.get(json_price_url, headers).text
    # get the first price dict
    price_data = json.loads(json_price)[0]
    # price
    phone_price = price_data["op"]

    # requests url for json comments
    comments_url = 'https://club.jd.com/comment/productCommentSummaries.action?referenceIds=' + sku
    # get json comments data
    comments_json_data = requests.get(comments_url, headers).text
    # Get comments dict. CommentsCount for key and a list for value.
    comments_data = json.loads(comments_json_data)
    comments_list = comments_data.get("CommentsCount")[0]

    comment_count = comments_list.get("CommentCountStr")
    good_comment_count = comments_list.get("GoodCountStr")
    after_comment_count = comments_list.get("AfterCountStr")
    general_comment_count = comments_list.get("GeneralCountStr")
    poor_comment_count = comments_list.get("PoorCountStr")
    good_comment_rate = comments_list.get("GoodRate")
    poor_comment_rate = comments_list.get("PoorRate")
    general_comment_rate = comments_list.get("GeneralRate")

    shop_url = "https://item.jd.com/%s.html" % sku
    print(shop_url)
    # shop_json_data = requests.get(shop_json_url, headers).text
    # shop_data = json.loads(shop_json_data)
    # print(shop_data)

    break





