# -*- coding:utf-8 -*-
# @author: luning
# @create_on: Sep 29, 2018
# @file_name: data_clear.py

import datetime
import time
import csv
from src.class_files.constant import *

class DataClear(object):
    """
    Summary: 
        数据清洗

    Attributes:
        __data(dataframe): 数据
    """
    def __init__(self, data):
        self.__data = data

    def date_trans(self, data_time):
        """
            时间转换，全部转化时间戳
        -----------------------------------
        Args: 
            :param data_time(string): 需要转化的时间

        Returns:
            time_stamp 时间戳
        """
        # 转换成时间数组
        time_array = time.strptime(data_time, '%Y-%m-%d')
        time_stamp = time.mktime(time_array)
        return time_stamp

    def date_format(self, time_need_format, search_time):
        """
            时间转换，全部转化为yyyy-mm-dd格式
        -----------------------------------
        Args: 
            :param time_need_format(string): 需要转化的时间
            :param search_time(string): 爬取时间

        Returns:
            new_date_time 新时间
        """
        time_stamp = ''
        if time_need_format.find('年') >= 0:
            # 2018年7月11日
            new_time = time_need_format.replace('年', '-')
            new_time = new_time.replace('月', '-')
            new_time = new_time.replace('日', '')
            time_stamp = self.date_trans(new_time)

        elif time_need_format.find('月') >= 0:
            # 6月10日
            new_time = time_need_format.replace('月', '-')
            new_time = new_time.replace('日', '')
            new_time = '2018-' + new_time
            time_stamp = self.date_trans(new_time)
        
        elif time_need_format.find('-') >= 0:
            # 2018-7-11
            time_stamp = self.date_trans(time_need_format)

        else:
            # 今天、昨天...
            # 转换成时间戳
            search_time = search_time[:10]
            time_stamp = self.date_trans(search_time)
            time_stamp = time_stamp - constant['TIME_FORMAT'][time_need_format]
            
        # 转换成localtime
        time_local = time.localtime(time_stamp)
        # 转换成新的时间格式 (2016-05-05)
        new_date_time = time.strftime("%Y-%m-%d",time_local)
        return new_date_time
    
    def save_news(self, news):
        """
            将内容存储
        -----------------------------------
        Args: 
            :param news(dic): 写入的内容

        Returns:
            none
        """
        file_path = './src/data/news_format_not_contain_week.csv'
        file = open(file_path, 'a+')
        # 文件的头
        title_name = [
            'title',
            'publish_time',
            'content',
            'account',
            'account_name',
            'search_time'
        ]
        writer = csv.DictWriter(file, fieldnames = title_name)
        writer.writerow(news)

    def data_clear(self):
        """
            时间清洗函数
        -----------------------------------
        Args: 
            none

        Returns:
            none
        """
        for index, row in self.__data.iterrows():
            if row['publish_time'] != '一周前':
                row['publish_time'] = self.date_format(row['publish_time'], row['search_time'])
                data_push = {
                    'title': row['title'],
                    'publish_time': row['publish_time'],
                    'content': row['content'],
                    'account': row['account'],
                    'account_name': row['account_name'],
                    'search_time': row['search_time']
                }
                self.save_news(data_push)













