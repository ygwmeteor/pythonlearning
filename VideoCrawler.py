
# 参考资料
# '''
# https://www.cnblogs.com/fatlyz/p/4293669.html
# https://blog.csdn.net/c406495762/article/details/78123502
# https://cuijiahua.com/blog/spider/
# https://www.cnblogs.com/xuchunlin/p/8668069.html
# '''

# 导入http请求库
import requests
import lxml
import os
import re
import time
import sys
from bs4 import BeautifulSoup

# 一级网址
UrlBase = "http://www.79yy.cn"
# 视频列表页
URL = "http://www.79yy.cn/type/1/1.html"
# 视频介绍页
URL2 = "http://www.79yy.cn/show/32276.html"
# 视频播放页
URL3 = "http://www.79yy.cn/play/32276/0/0.html"
# 视频真实播放地址
URLX = "http://api.yyxzpc.cn/mdparse/m3u8.php?id=https://cn2.zuidadianying.com/20181216/IdYeq4aP/index.m3u8"


def getPage(url):
    # 给请求指定一个请求头来模拟chrome浏览器
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
    req = requests.get(url, headers=headers)
    # req.encoding = 'gb2312'
    # req.encoding = 'gbk'
    # req = requests.get(url)
    soup = BeautifulSoup(req.text, 'lxml')
    return soup


def createHtmls(playUrls):
    if playUrls is None:
        return None
    hrefTemplate = '<div><a href="{}">{}</a></div>'
    result = ''
    for li in playUrls:
        result = result+'\n'+hrefTemplate.format(li[1], li[0])
    return result


def createIndexHtml(urls):
    divTemplate = '<div style="width:100%;height:100%">\n{}\n</iframe>\n</div>'
    divStr = divTemplate.format(urls)
    htmlTemplate = '''
    <!DOCTYPE html>
    <html lang="zh-cn" manifest="" xmlns="" dir="auto">\n<html>\n
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta http-equiv="X-UA-Compatible" content="ie=edge">
            <title>电影大全</title>
        </head>
        <body>
            <h1>无广告电影</h1>
        {}
        </body>
    </html>
    '''
    return htmlTemplate.format(divStr)


def saveHtmlToFile(html, fileName):
    if not html is None:
        fp = open(fileName, 'x', 1024, 'utf-8')
        fp.write(html)
        fp.flush()
        fp.close()
        return 0
    return 1


def findPlayUrl(url):
    soup = getPage(url)
    div = soup.find('div', attrs={'class': 'online-button'})
    if not div is None:
        # ,string="^\s+立即播放\s+$"
        a = div.find('a', attrs={'class': 'btn btn-success btn-block'})
        if not a is None:
            return a.attrs['href']
    return None


def findRealPlayUrl(url):
    # <iframe border="0" frameborder="0" height="460" id="player_swf" marginheight="0" marginwidth="0" scrolling="no" allowfullscreen="ture" src="http://api.yyxzpc.cn/mdparse/m3u8.php?id=https://sohu.zuida-163sina.com/20190110/xq7CpZ80/index.m3u8" width="100%"></iframe>
    soup = getPage(url)
    frame = soup.find('iframe', id='player_swf')
    if not frame is None:
        return frame.attrs['src']
    return None


def main():
    lis = []
    playUrls = []
    realUrls = []
    soup = getPage(URL)
    divs = soup.find_all(
        'div', attrs={'class': 'col-md-1-5 col-sm-4 col-xs-6'})
    k = 0
    if not divs is None:
        for div in divs:
            k = k + 1
            a = div.find('a')
            if not a is None:
                lis.append((a.attrs['title'], UrlBase+a.attrs['href']))
    for dd in lis:
        time.sleep(2.7)
        print(" Name:{},URL:{}".format(dd[0], dd[1]))
        p0 = findPlayUrl(dd[1])
        if not p0 is None:
            playUrls.append((dd[0], UrlBase+p0))
    for dd in playUrls:
        time.sleep(2.0)
        p0 = findRealPlayUrl(dd[1])
        if not p0 is None:
            print(" Name:{},RealURL:{}".format(dd[0], p0))
            realUrls.append((dd[0], p0))
    result2 = createHtmls(realUrls)
    result = createIndexHtml(result2)
    if not result is None:
        dir= 'Python\\Crawlers\\'
        if os.path.isdir(dir):
            htmlFile = dir + time.strftime('%Y%m%d%H%M', time.localtime(time.time()))+"_Movie.html"
        else:
            htmlFile = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))+"_Movie.html"
        if os.path.isfile(htmlFile):
            os.remove(htmlFile)
        saveHtmlToFile(result, htmlFile)

def main2():
    dir= 'Python\\Crawlers2\\'
    if os.path.isdir(dir):
        print("exists")
    else:
        print("not exists")

if __name__ == '__main__':
    print("Video Crawler Start!")
    main2()
    print("Video Crawler Done!")
