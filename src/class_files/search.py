# -*- coding:utf-8 -*-
# @author: luning
# @create_on: Sep 26, 2018
# @file_name: search.py

import re
import urllib.parse
import urllib.request
import urllib.error
import time
import datetime
import csv
from bs4 import BeautifulSoup as BS
from src.class_files.driver_common import *
from src.class_files.constant import *

class Search(object):
    """
    Summary: 
        爬虫主要程序

    Attributes:
        __key_words(string): 搜索的关键词
        __base_url(string): 网站的网址(不含Query的)
        __driver(object): 驱动
    """
    def __init__(self, key_words, base_url):
        self.__key_words = key_words
        self.__base_url = base_url

    def create_website_address(self, page):
        """
            创建访问的URL
        -----------------------------------
        Args: 
            :param page(number): 要访问的页数

        Returns:
            url: 访问的URL
        """
        query = {
            'query': '',
            'type': 2,
            'page': page
        }
        # UTF-8编码 错误处理方式是直接报错
        key_words = self.__key_words.encode(encoding='UTF-8',errors='strict')
        query['query'] = key_words
        querys = urllib.parse.urlencode(query)
        url = self.__base_url + '?' + querys
        return url

    def open_pages(self, url, type):
        """
            打开链接并返回HTML页面用于分析
        -----------------------------------
        Args: 
            :param url(string): 要爬的URL
            :param type(num): 是爬文章还是爬列表

        Returns:
            soup: BeautifulSoup返回的页面对象
        # """
        # soup = None
        # if type == constant['LIST_TYPE']:
        #     response = urllib.request.urlopen(url)  
        #     data = response.read()
        #     data = data.decode('UTF-8')
        #     soup = BS(data, 'html.parser')
        # else:
        self.__driver = DriverCommon()
        news_driver = self.__driver # 生成一个driver对象
        # news_driver.driver.get(url) 写两遍是因为要加cookie
        # 浏览器确保这个cookie用于这个网站才会给加载
        # 不写两遍会出错
        if type == constant['LIST_TYPE']:
            news_driver.driver.get(url)
            time.sleep(2)
            for cookie in constant['COOKIE_LIST']:
                news_driver.driver.add_cookie(cookie)
        news_driver.driver.get(url)
        soup = BS(news_driver.driver.page_source, 'html.parser')
        return soup

    def get_news_links(self, url):
        """
            获取搜狗访问页面的新闻块链接
        -----------------------------------
        Args: 
            :param url(string): 要爬的URL

        Returns:
            results: 本页面中所有的新闻链接
        """
        soup = self.open_pages(url, constant['LIST_TYPE'])
        print(url)
        news = soup.findAll(class_= 'txt-box')
        results = []
        for new in news:
            new = new.find('h3')
            news_url = ''
            # URL 正则
            urlRE = re.compile(r'href="([^"]*)"')
            urls = re.search(urlRE, str(new))
            # 找URL
            if urls:
                for url in urls.groups():
                    news_url = url.split('amp;')
                    news_url = ''.join(news_url)
            if (news_url != ''):
                results.append(news_url)
        return results

    def get_news_content(self, url):
        """
            获取单个文章内容
        -----------------------------------
        Args: 
            :param url(string): 要爬的URL

        Returns:
            news_content: 本页面中所有的新闻链接
        """
        news_content = None
        try:
            print(url)
            soup = self.open_pages(url, constant['ARTICLE_TYPE'])
            title = soup.find(class_= 'rich_media_title').get_text().strip()
            date = soup.find('em', id='publish_time').get_text().strip()
            content = soup.find(class_= 'rich_media_content').get_text().strip()
            account = soup.find(class_= 'profile_meta_value').get_text().strip()
            account_name = soup.find(class_= 'profile_nickname').get_text().strip()
            now = datetime.datetime.now()
            news_content = {
                'title': title,
                'publish_time': date,
                'content': content,
                'account': account,
                'account_name': account_name,
                'search_time': str(now)
            }
        except:
            print('error in search article')
        return news_content

    def save_news(self, news):
        """
            将内容存储
        -----------------------------------
        Args: 
            :param news(dic): 写入的内容

        Returns:
            none
        """
        file_path = './src/data/news.csv'
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

    def search_news(self):
        news_urls = []
        for num in range(1, constant['PAGE_NUM']+1):
            url = self.create_website_address(num)
            news_urls += self.get_news_links(url)
            self.__driver.driver.quit()
            print(len(news_urls))
            time.sleep(10)
            for url in news_urls:
                news = self.get_news_content(url)
                if news:
                    self.save_news(news)
                self.__driver.driver.quit()
                time.sleep(5)
            news_urls = []
        

