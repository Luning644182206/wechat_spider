# -*- coding:utf-8 -*-
# @author: luning
# @create_on: Sep 26, 2018
# @file_name: main.py

from src.class_files.search import Search
from src.class_files.constant import *
import pandas as pd
import os,sys
sys.path.append('./src/class_files')

if __name__ == '__main__':
    key_words = ['共产党', '特朗普', '中美贸易','中美贸易战']
    for key_word in key_words:
        base_url = constant['URL']['WECHAT']
        search_news = Search(key_word, base_url)
        search_news.search_news()

    # 数据统计
    path = './src/data/news.csv'
    news = pd.read_csv(path, sep=',')
    print(news)
    account_num = news.groupby(['account'])['account'].nunique()
    print(df_new_1)

