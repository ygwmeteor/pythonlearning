
# -*- coding:UTF-8 -*-

# Pyhon 文本网络爬虫 Selenium + PhatomJS
'''
https://www.cnblogs.com/Albert-Lee/p/6238866.html
PhatomJS:http://phantomjs.org/
Selenium:pip install selenium
'''

# 导入http请求库
import requests
import lxml
import os
import re
import time

from bs4 import BeautifulSoup

#URL = 'https://www.booktxt.net/0_362/'
URL = 'http://www.catalog.update.microsoft.com/DownloadDialog.aspx'

# itchat: https://itchat.readthedocs.io/zh/latest/


def requestsTest():
    # get
    # 给请求指定一个请求头来模拟chrome浏览器
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
    rep = requests.get(URL, headers=headers)
    rep = requests.post(URL)


def BeautifulSoupTest():
    soup = BeautifulSoup('htmltext', 'html.parser')
    print(soup.prettify())
    # find title
    title = soup.title


def getTotalPage(url):
    # 给请求指定一个请求头来模拟chrome浏览器
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
    req = requests.get(url, headers=headers)
    #req.encoding = 'gb2312'
    # req = requests.get(url)
    soup = BeautifulSoup(req.text, 'lxml')
    return soup


def getAllIndexes(soup):
    list_div = soup.find_all('a')
    lis = []
    # print(list_div.children)
    # for child in list_div.children:
    #     res = child.find_all('a')
    #     for dd in res:
    #         lis.append(dd.attrs['href'])
    for a_tag in list_div:
        lis.append(a_tag.attrs['href'])

    return lis


def main():
    print("Python 网络爬虫")
    soup = getTotalPage(URL)
    print(soup.prettify())
    lis = getAllIndexes(soup)
    dir = os.getcwd()
    for file in lis:
        filename = file.split("/")[-1]
        r = requests.get(file)
        with open(dir+"\\" + filename, "wb") as f:
            f.write(r.content)
            
    print("ALL DONE !!!")

if __name__ == '__main__':
    main()
