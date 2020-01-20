from urllib import request
from bs4 import BeautifulSoup
import time
url = 'http://www.bxwx3.org/txt/48595//169891//htm'
flag = 0
while 1:
    time.sleep(0.1)
    req = request.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                            Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063')
    str = request.urlopen(req).read().decode('gb2312')
    content = BeautifulSoup(str)
    with open('1.txt','ab+') as f:
        h = content.select('h1')
        #print(h[1].string)
        f.write(h[1].string.encode('utf-8') + '\n\n'.encode('utf-8'))
        s = content.find_all('p')
        for i in s:
           # print(i.string)
             f.write(i.string.encode('utf-8') + '\n'.encode('utf-8'))
    url = content.find(id = 'xiaye').get('href')
    if url == 'http://www.bxwx3.org/txt/48595/':
        break
        
