import os
import sys
import getopt
import zipfile
import rarfile
import shutil
import time

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from configparser import ConfigParser


def is_public_ip(ip_address):
    # 将IP地址拆分为四个整数
    octets = ip_address.split('.')
    first_octet = int(octets[0])

    # 判断非IP地址
    for ip in octets :
        if int(ip) > 255 :
            return False

    # 根据公网IP地址范围进行判断
    if first_octet == 10:
        return False  # 私有地址，不是公网IP
    elif first_octet == 172 and 16 <= int(octets[1]) <= 31:
        return False  # 私有地址，不是公网IP
    elif first_octet == 192 and int(octets[1]) == 168:
        return False  # 私有地址，不是公网IP
    elif first_octet == 127:
        return False  # 回环地址，不是公网IP
    elif first_octet == 169 and int(octets[1]) == 254:
        return False  # 链路本地地址，不是公网IP
    elif 224 <= first_octet <= 239:
        return False  # 多播地址，不是公网IP
    else:
        return True  # 其他情况为公网IP

def SearchFile(keyword,path):
    '''
    Search if keyword in the file, if yes return ture, else return false

    '''
    try:
        with open(path) as f:
            for index, line in enumerate(f.readlines()):
                if keyword in line:
                    li = [path,line]
                    return li
            
            return False
    except:
        pass
        # with open(path,"r", encoding='utf-8') as f:
        #     for index, line in enumerate(f.readlines()):
        #         if keyword in line:
        #             return True
            
        #     return False

def GetFiles(path):
    '''
    use GetMapFiles() to get all map
    use GetConfigFiles() to get all config
    use GetZipFiles() to get all achive files
    '''

    config = []
    txt = []
    zip = []
    rar = []
    xmap = []
    qmap = []
    #遍历目录中所有文件及子目录文件 
    for root,dirs,files in os.walk(path): 
        #for dir in dirs: 
        #    print(os.path.join(root,dir))
        for file in files: 
            #print(os.path.join(root,file))
            if file.endswith('.config') :
                Sresult = SearchFile('hostname',os.path.join(root,file))
                if Sresult:
                    config.append(Sresult)

            if file.endswith('.txt') :
                Cresult = SearchFile('hostname',os.path.join(root,file))
                if Cresult:
                    txt.append(Cresult)

            if file.endswith('.zip') :
                zlist = []
                try :
                    zlist = zipfile.ZipFile(os.path.join(root,file)).namelist()
                except :
                    pass
                for name in zlist:
                    if name.endswith('.xmap') or name.endswith('.qmap') :
                        zip.append(os.path.join(root,file))
                        break
                    elif name.endswith('.config') or name.endswith('.txt') :
                        with zipfile.ZipFile(os.path.join(root,file)) as zf :
                            with zf.open(name) as myfile :
                                for index, line in enumerate(myfile.readlines()):
                                    if b'hostname' in line :
                                        zip.append(os.path.join(root,file))
                                        break
                                    else :
                                        continue
                        break

            if file.endswith('.rar') :
                rlist = []
                try :
                    rlist = rarfile.RarFile(os.path.join(root,file)).namelist()
                except :
                    pass
                for name in rlist:
                    #if name.endswith('.config') or name.endswith('.xmap') or name.endswith('.qmap') :
                    if name.endswith('.xmap') or name.endswith('.qmap') :
                        rar.append(os.path.join(root,file))
                        break
                    elif name.endswith('.config') or name.endswith('.txt') :
                        with rarfile.RarFile(os.path.join(root,file)) as rf :
                            with rf.open(name) as myfile :
                                for index, line in enumerate(myfile.readlines()):
                                    if b'hostname' in line :
                                        rar.append(os.path.join(root,file))
                                        break
                                    else :
                                        continue
                        break


            if file.endswith('.xmap') :
                xmap.append(os.path.join(root,file))
            if file.endswith('.qmap') :
                qmap.append(os.path.join(root,file))

    return config,txt,zip,rar,xmap,qmap


#复制文件
def copyfile(srcfile,dstfile):
    if not os.path.isfile(srcfile):
        pass
    else:
        fpath,fname=os.path.split(srcfile)    #分离文件名和路径
        dir = dstfile
        #dir = dstfile + fpath.replace(':','') #构建目的路径，windows去除盘符后的冒号 Ex: D:\test --> D\test
        #if not os.path.exists(dir):
        #    os.makedirs(dir)                #创建路径
        shutil.copy(srcfile,dir + '\\' + fname)      #复制文件    
    #pass

#移动文件
def movefile(srcfile,dstfile):
    #if not os.path.isfile(srcfile):
    #    pass
    #else:
    #    fpath,fname=os.path.split(srcfile)    #分离文件名和路径
    #    dir = dstfile + fpath.replace(':','') #构建目的路径，windows去除盘符后的冒号 Ex: D:\test --> D\test
    #    if not os.path.exists(dir):
    #        os.makedirs(dir)                #创建路径
    #    shutil.move(srcfile,dir + '\\' + fname)      #移动文件
    pass



def main():
    
    #获取执行程序后的参数
    try:
        opts,args=getopt.getopt(sys.argv[1:],"hs:d:",["help","source=","des_dir="]) #hs:d: 表示参数-h 不需要值，：表示需要值
    except getopt.GetoptError as error:
        print(str(error))
        sys.exit(2)

    for key,value in opts:
        if key == '-s':
            source = value
        if key == '-d':
            des_dir = value
        if key == '-h':
            print(" -s <source_dir> -d <des_dir_dir>")
    

    # source = 'D:/test'
    # des_dir = 'F:/aa'
    sourceL = source.split('\\')
    lognameT = ''
    for x in sourceL:
        if x.find(':') == 1:
            continue
        else:
            lognameT += x

    log = open(des_dir + '\\time' + source[0] + lognameT + '.log', 'w')
    log.write("Program SearchFile started at : " + time.strftime("%Y-%m-%d %X",time.localtime()) + "\n")
    c,t,z,r,m,q= GetFiles(source) 
    log.write("Program SearchFile finished at : " + time.strftime("%Y-%m-%d %X",time.localtime()) + "\n")

    flist = open(des_dir + '\\FileLists' + source[0] + lognameT + '.txt','w')
    
    longfilename = open(des_dir + '\\LongFilename' + source[0] + lognameT + '.txt','w')


    log.write("Program MoveFile started at : " + time.strftime("%Y-%m-%d %X",time.localtime()) + "\n")
    flist.write('==============================All Config files============================\n')
    for x in c:
        if len(x) > 240:    #文件路径超过255后，无法复制、移动
            longfilename.write(x[0] + '\n')
        else:
            flist.write(x[0] + "              Content:" + x[1] )
            #copyfile(x[0],des_dir + '\\config\\')
    flist.write('==============================All TXT files============================\n')
    for x in t:
        if len(x) > 240:
            longfilename.write(x[0] + '\n')
        else:
            flist.write(x[0] + "              Content:" + x[1] )
           # copyfile(x[0],des_dir + '\\txt\\')
    flist.write('==============================All ZIP/RAR files============================\n')
    for x in z:
        if len(x) > 240:
            longfilename.write(x + '\n')
        else:
            flist.write(x + '\n')
            #copyfile(x,des_dir + '\\zip\\')
    for x in r:
        if len(x) > 240:
            longfilename.write(x + '\n')
        else:
            flist.write(x + '\n')
            #copyfile(x,des_dir + '\\rar\\')
    flist.write('==============================All Map files============================\n')
    for x in m:
        if len(x) > 240:
            longfilename.write(x + '\n')
        else:
            flist.write(x + '\n')
            #copyfile(x,des_dir + '\\xmap\\')
    flist.write('==============================All Qmap files============================\n')
    for x in q:
        if len(x) > 240:
            longfilename.write(x + '\n')
        else:
            flist.write(x + '\n')
            #copyfile(x,des_dir + '\\')

    flist.close()
    longfilename.close()
    log.write("Program MoveFile finished at : " + time.strftime("%Y-%m-%d %X",time.localtime()) + "\n")
    log.close()

    # send email notification 

    config = ConfigParser()
    config.read_file(open('config.ini'))
    #path = config.get('os', 'path')
    receiver = config.get('email', 'receiver')
    server = config.get('email', 'server')
    sender = config.get('email', 'sender')
    pwd = config.get('email', 'pwd')
    port = 587

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = "Customer data found in files.com"
    body = "Hi Team,\n\nThere are customer data found in files.com. For detail, please see the attachment.\n\n\nThanks\n"

    msg.attach(MIMEText(body, 'plain'))

    attachment = open(des_dir + '\\FileLists' + source[0] + lognameT + '.txt','rb')

    mime_base = MIMEBase('application', 'octet-stream')
    mime_base.set_payload((attachment).read())
    encoders.encode_base64(mime_base)
    mime_base.add_header('Content-Disposition', 'attachment', filename='CheckResult.txt')

    msg.attach(mime_base)

    try:
        server = smtplib.SMTP(server, port)
        server.starttls()
        server.login(sender, pwd)
        server.send_message(msg)
        server.quit()
        print('Email sent successfully!')
    except Exception as e:
        print('Error: unable to send email.')
        print(e)




if __name__ == '__main__':
    
    main()
#    input('Please press any key to exit!')