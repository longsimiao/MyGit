#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.request import urlopen, build_opener
from bs4 import BeautifulSoup
import random
import datetime
import requests
import json
import csv


random.seed(datetime.datetime.now())


def get_url_lists(start_url, crawl_url_lists=[]):
    """
    获取待爬取 url 列表
    :param start_url: Start url.
    :param crawl_url_lists: A list to store being crawled url list.
    :return: To be crawled url list.
    """
    # 判断url是否已在待爬取池中
    if start_url not in crawl_url_lists:
        crawl_url_lists.append(start_url)

    headers = ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/55.0.2883.9 Safari/537.36')
    build_opener().addheaders = [headers]
    req_content = build_opener().open(start_url)
    bs_obj = BeautifulSoup(req_content.read(), 'html.parser')
    next_page_url_obj = bs_obj.findAll("a", {"class": "pn-next"})
    hostname = "https://list.jd.com"
    # '#J_main'需保留，否则无法抓取全部url
    next_page_url = hostname + next_page_url_obj[0]["href"] + '#J_main'

    if next_page_url not in crawl_url_lists:
        crawl_url_lists.append(next_page_url)
        # callback get_url_lists()
        get_url_lists(next_page_url, crawl_url_lists)

    return crawl_url_lists


def get_phone_data_from_jd(start_url):
    """
    爬取内容
    :param start_url: Start url.
    :return: Data to be stored.
    """
    headers = ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/55.0.2883.9 Safari/537.36')
    build_opener().addheaders = [headers]
    req_content = build_opener().open(start_url)
    bs_obj = BeautifulSoup(req_content.read(), 'html.parser')

    phone_lists = bs_obj.findAll("li", {"class": "gl-item"})
    # print(phone_lists[0])
    phone_row = []
    for phone_obj in phone_lists:
        temp_phone_row = []
        # 店铺名称 store_name
        store_obj = phone_obj.findAll("div", {"class": "p-shop"})
        store_name = store_obj[0]["data-shop_name"]

        # 手机简介
        phone_brief_obj = phone_obj.findAll("em")
        phone_brief = phone_brief_obj[-1].string

        # SKU
        phone_sku_obj = phone_obj.findAll("div", {"class": "j-sku-item"})
        phone_sku = phone_sku_obj[0]["data-sku"]

        # 价格 phone_price
        # json_price_url = 'https://p.3.cn/prices/mgets?skuIds=J_' + phone_sku
        guess_num_1 = random.randrange(10000000, 99999999)
        json_price_url = 'https://p.3.cn/prices/mgets?pduid=14926716573134' \
                         + str(guess_num_1) + '&skuIds=J_' + phone_sku
        json_price = requests.get(json_price_url, headers).text
        price_data = json.loads(json_price)[0]
        phone_price = price_data["op"]

        # comments_url = 'https://club.jd.com/comment/product' \
        #                'CommentSummaries.action?referenceIds=' + phone_sku
        guess_num_2 = random.randrange(10000000, 99999999)
        comments_url = 'https://club.jd.com/comment/productComment' \
                       'Summaries.action?referenceIds=' + phone_sku \
                       + '&_=14927' + str(guess_num_2)
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

        temp_phone_row.append(store_name)
        temp_phone_row.append(phone_brief)
        temp_phone_row.append(phone_sku)
        temp_phone_row.append(phone_price)
        temp_phone_row.append(comment_count)
        temp_phone_row.append(good_comment_count)
        temp_phone_row.append(after_comment_count)
        temp_phone_row.append(general_comment_count)
        temp_phone_row.append(poor_comment_count)
        temp_phone_row.append(good_comment_rate)
        temp_phone_row.append(poor_comment_rate)
        temp_phone_row.append(general_comment_rate)

        print(temp_phone_row)

        phone_row.append(temp_phone_row)

    return phone_row


def main_control(start_url):
    """
    每一页存为一个CSV文件
    :param start_url: Start url.
    :return: None.
    """
    crawl_url_line = get_url_lists(start_url)
    i = 0

    for url in crawl_url_line:
        csv_data = get_phone_data_from_jd(url)
        i += 1
        csv_file_name = "res" + str(i)
        with open(csv_file_name + ".csv", "w") as f:
            header = ["店铺", "简介", "SKU", "价格", "总评", "好评",
                      "追评", "中评", "差评", "好评率", "差评率", "中评率"]
            f_csv = csv.writer(f)
            f_csv.writerow(header)
            f_csv.writerows(csv_data)


def main_control_res(start_url):
    """
    所有结果存为一个CSV文件
    :param start_url: Start url.
    :return: None.
    """
    crawl_url_line = get_url_lists(start_url)
    res_csv = []
    for url in crawl_url_line:
        csv_data = get_phone_data_from_jd(url)
        res_csv += csv_data
    return res_csv


# begin_url = "https://list.jd.com/list.html?cat=9987,653,655"
#
# csv_data_res = main_control_res(begin_url)
# csv_name = "res"
# with open(csv_name + ".csv", "w") as f:
#     headers = ["店铺", "简介", "SKU", "价格", "总评", "好评", "追评",
#                "中评", "差评","好评率", "差评率", "中评率"]
#     f_csv = csv.writer(f)
#     f_csv.writerow(headers)
#     f_csv.writerows(csv_data_res)
#
# main_control_res(begin_url)

# get_phone_data_from_jd(begin_url)
