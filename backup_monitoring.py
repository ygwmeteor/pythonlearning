#! /usr/bin/env python

import os
import time
import datetime
import smtplib

from email.mime.text import MIMEText
from email.header import Header

from configparser import ConfigParser


def SendMail(server,sender,pwd,receiver,msg):
    
    email = smtplib.SMTP(server,587)
    email.starttls()
    email.ehlo(server)
    email.login(sender,pwd)
    email.sendmail(sender,receiver,msg)
    email.quit()
    
    
def GetNewFiles(path,num):
    
    lists = os.listdir(path)
    lists.sort(key=lambda fn:os.path.getctime(path+'\\'+fn))

    result = []

    for file in lists[-num :] :
        full_path = os.path.join(path, file)
        #print(full_path)
        #print(file)
        mtime = os.stat(full_path).st_mtime
        ftime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
        result.append(file + " " + ftime)
    
    return result
    
def CheckBackup(list):
    
    CheckResult = False
    today = datetime.date.today().strftime("%Y-%m-%d")
    for file in list:
        if today in file:
            CheckResult = True
            break
    
    return CheckResult
    
def MailContent(pathL,num):
    
    content = []
    subject = "All backup sucessfull!"
    body = ""
    spilt = "\n-------------------------------------------------------------------\n\n"
    
    for key,value in pathL:
        fileList = GetNewFiles(value,num)
        files = ""
        
        if key == "EsafeNet" and datetime.date.today().strftime("%w") != "3":
            continue
        if key == "SVN" and datetime.date.today().strftime("%w") != "5":
            continue

        if not CheckBackup(fileList):
            subject = key + " backup failed"

        for file in fileList:
            files +=  file + "\n\n"
        body = body + key + " backup files:\n\n" + files + spilt
    content.append(subject)
    content.append(body)

    return content



    
def main():
    
    # server = 'smtp.office365.com'
    # sender = 'beijingit4@netbraintech.com'
    # receiver = 'gavin.yuan@netbraintech.com'
    # pwd = 'flxcnjzwjfqhrhnp'

    #config.ini file content:
    #
    #[os]
    #path=D:\test
    #
    #[email]
    #server=smtp.office365.com
    #sender=online@netbraintech.com
    #pwd=Netbrain12
    #receiver=gaowei.yuan@netbraintech.com,Feng.Liu@netbraintech.com
    
    config = ConfigParser()
    config.read_file(open('config.ini'))
    #path = config.get('os', 'path')
    receiver = config.get('email', 'receiver')
    server = config.get('email', 'server')
    sender = config.get('email', 'sender')
    pwd = config.get('email', 'pwd')
    
    
    path = [("AD",r"\\10.10.10.12\AD-001-bak2019"), \
            ("Exchange",r"\\10.10.10.19\exchange"), \
            ("GitHub",r"\\10.10.36.1\githubbak"), \
            ("Jira",r"\\10.10.14.253\Jira_Backup\Jira"), \
            ("Confluence",r"\\10.10.14.253\Jira_Backup\Confluence"), \
            ("EsafeNet",r"\\10.10.10.19\backup\10-70"), \
            ("SVN",r"\\10.10.14.253\bak\10.10sys")]

    content = MailContent(path,5)

    #content = MailContent(path,12)
    #content = MailContent("D:\\test",6)
    mail_content = content[1]

    
    msg = MIMEText(mail_content, "plain", "utf-8")
    msg["Subject"] = Header(content[0], "utf-8")
    msg["From"] = sender
    msg["To"] = Header(receiver)
    
    SendMail(server,sender,pwd,receiver.split(','),msg.as_string())






if __name__ == '__main__':
    main()
