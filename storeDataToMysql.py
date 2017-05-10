#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 4/21/17 12:25 AM
# @Author  : Ferras
# @Email   : mxlmiao@sina.cn
# @File    : test_next_url.py
# @Software: PyCharm
import re
import pymysql
from crawlDataFromJD import getPhoneDataFromJd


def judge_table_exist(table_name, database_name):
    """
    判断表是否已存在
    :param table_name:
    :param database_name:
    :return:
    """
    conn = pymysql.connect(host='localhost', user='root',
                           passwd='root', db=database_name,
                           charset='utf8')
    cur = conn.cursor()
    try:
        show_table_sql = "SHOW TABLES;"
        cur.execute(show_table_sql)
        tables = [cur.fetchall()]
        table_list = re.findall('(\'.*?\')', str(tables))
        table_list = [re.sub("'", '', each) for each in table_list]
        if table_name in table_list:
            print('Table', table_name, 'already exists')
            return 1
        else:
            print('Table', table_name, 'not exists')
            return 0
    except Exception as e:
        print("<--出现异常-->" + str(e))
    finally:
        cur.close()
        conn.close()


def create_table(table_name, database_name):
    """
    输入要创建的表名和要使用的数据库名称
    :param table_name: 要创建的表名称
    :param database_name: 所使用的数据库名称
    :return:
    """
    conn = pymysql.connect(host='localhost', user='root',
                           passwd='root', db=database_name,
                           charset='utf8')
    cur = conn.cursor()
    try:

        create_table_sql = """
            CREATE TABLE %s(
            id BIGINT(7) NOT NULL AUTO_INCREMENT,
            store VARCHAR(200),
            brief VARCHAR(200),
            SKU VARCHAR(200),
            price VARCHAR(200),
            total_comment VARCHAR(200),
            good_comment VARCHAR(200),
            after_comment VARCHAR(200),
            general_comment VARCHAR(200),
            poor_comment VARCHAR(200),
            good_comment_rate VARCHAR(200),
            poor_comment_rate VARCHAR(200),
            general_comment_rate VARCHAR(200),
            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY(id)
            )CHARACTER SET=utf8;
            """ % table_name

        cur.execute(create_table_sql)
    except Exception as e:
        print("<--出现异常-->" + str(e))
    finally:
        cur.close()
        conn.close()


def store_data(table_name, database_name, start_url):
    """
    将爬取到的数据存储到mysql中
    :param table_name: 使用的表名称
    :param database_name: 使用的数据库名称
    :param start_url: 起始url
    :return:
    """
    # 判断数据要存储的表是否存在
    if judge_table_exist(table_name, database_name) == 0:
        create_table(table_name, database_name)

    # 连接数据库，准备存储数据
    conn = pymysql.connect(host='localhost', user='root',
                           passwd='root', db=database_name, charset='utf8')
    cur = conn.cursor()
    try:

        # get_phone_data_from_jd()获取一页数据
        sql_data = getPhoneDataFromJd(start_url)
        print(len(sql_data))
        for data in sql_data:
            # 存储爬取数据
            store_data_sql = u"""
            INSERT INTO %s (store, brief, SKU, price, total_comment,
            good_comment, after_comment, general_comment, poor_comment,
            good_comment_rate, poor_comment_rate, general_comment_rate)
            VALUES(\"%s", \"%s", \"%s", \"%s" ,\"%s", \"%s",
            \"%s", \"%s", \"%s", \"%s", \"%s", \"%s")
            """ % (table_name, data[0], data[1], data[2],
                   data[3], data[4], data[5], data[6],
                   data[7], data[8], data[9], data[10],
                   data[11])

            cur.execute(store_data_sql)
            cur.connection.commit()
    except Exception as e:
        print("<--出现异常-->" + str(e))
    finally:
        cur.close()
        conn.close()

begin_url = "https://list.jd.com/list.html?cat=9987,653,655"
store_data("jd_dat", "mytest", begin_url)


