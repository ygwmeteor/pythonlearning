#! /usr/bin/env python

import os
import time
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
    
    return lists[-num : ]
    
def CheckProcess(name):
    
    proc = []
    p = os.popen('tasklist /FI "IMAGENAME eq %s"' % name)
    for x in p:
        proc.append(x)
    p.close()
    return proc
    
def MailContent(path,num):
    
    content = []
    
    dropbox = CheckProcess('dropbox.exe')
    carboniteservice = CheckProcess('carboniteservice.exe')
    
    if len(dropbox) < 2 or len(carboniteservice) < 2 :
        content.append("Dropbox or CarBonite doesn't run")
        s = '\n\t'.join(dropbox) + '\n\n' + '\n\t'.join(carboniteservice)
        content.append("Process Check Result:\n\t" + s)
        return content
    
    files = GetNewFiles(path,num)
    file_ctime = os.path.getctime(path + '\\' + files[0])
    now = time.time() - 86400
    
    if file_ctime > now :
        content.append("DB Backup Successfull")
        body = "\nThe Backup files are:\n\t" + '\n\t'.join(files)
        content.append(body)
        return content
    else :
        content.append("DB Backup Failed")
        body = "\nThe last backup sucessfull file is " + files[-1]
        content.append(body)
        return content
        

    
def main():
    
    #server = 'smtp.office365.com'
    #sender = 'online@netbraintech.com'
    #receiver = ['gavin.yuan@netbraintech.com' , 'feng.liu@netbraintech.com']
    #pwd = 'Netbrain12'
    
    
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
    path = config.get('os', 'path')
    receiver = config.get('email', 'receiver')
    server = config.get('email', 'server')
    sender = config.get('email', 'sender')
    pwd = config.get('email', 'pwd')
    
    content = MailContent(path,12)
    #content = MailContent("D:\\test",6)
    mail_content = content[1]
    
    msg = MIMEText(mail_content, "plain", "utf-8")
    msg["Subject"] = Header(content[0], "utf-8")
    msg["From"] = sender
    msg["To"] = Header(receiver)
    
    SendMail(server,sender,pwd,receiver.split(','),msg.as_string())

if __name__ == '__main__':
    main()
