import os
import re

file = open("E:\\desktop\\aaa.txt" , "w" , encoding='utf-8')
with open("E:\\desktop\\ng_audit.log" , "r" , encoding='utf-8') as da:
    for line in da:
        username = re.findall(r'( [a-z]{1,20} <.*>)',line)
        ip_list = re.findall(r'(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)',line)
        if len(ip_list) != 0:
            ip = ip_list[0]
            res = "".join(username) + ',' + ".".join(ip)
            file.write(res+"\n")
        
file.close()
        