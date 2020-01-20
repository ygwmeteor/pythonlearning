import os
import sys
import getopt
import zipfile
import rarfile
import shutil
import time



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
    map = []
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
                    if name.endswith('.config') or name.endswith('.map') or name.endswith('.qmap') :
                        zip.append(os.path.join(root,file))
                        break
            if file.endswith('.rar') :
                rlist = []
                try :
                    rlist = rarfile.RarFile(os.path.join(root,file)).namelist()
                except :
                    pass
                for name in rlist:
                    if name.endswith('.config') or name.endswith('.map') or name.endswith('.qmap') :
                        rar.append(os.path.join(root,file))
                        break
            if file.endswith('.map') :
                map.append(os.path.join(root,file))
            if file.endswith('.qmap') :
                qmap.append(os.path.join(root,file))

    return config,txt,zip,rar,map,qmap


#复制文件
def copyfile(srcfile,dstfile):
    if not os.path.isfile(srcfile):
        pass
    else:
        fpath,fname=os.path.split(srcfile)    #分离文件名和路径
        dir = dstfile + fpath.replace(':','') #构建目的路径，windows去除盘符后的冒号 Ex: D:\test --> D\test
        if not os.path.exists(dir):
            os.makedirs(dir)                #创建路径
        shutil.copy(srcfile,dir + '\\' + fname)      #复制文件    
    #pass

#移动文件
def movefile(srcfile,dstfile):
    # if not os.path.isfile(srcfile):
        # pass
    # else:
        # fpath,fname=os.path.split(srcfile)    #分离文件名和路径
        # dir = dstfile + fpath.replace(':','') #构建目的路径，windows去除盘符后的冒号 Ex: D:\test --> D\test
        # if not os.path.exists(dir):
            # os.makedirs(dir)                #创建路径
        # shutil.move(srcfile,dir + '\\' + fname)      #移动文件
    pass

def main():
    
    #获取执行程序后的参数
    try:
        opts,args=getopt.getopt(sys.argv[1:],"hs:d:",["help","source=","destination="]) #hs:d: 表示参数-h 不需要值，：表示需要值
    except getopt.GetoptError as error:
        print(str(error))
        sys.exit(2)

    for key,value in opts:
        if key == '-s':
            source = value
        if key == '-d':
            destination = value
        if key == '-h':
            print(" -s <source_dir> -d <destination_dir>")
    

    # source = 'D:/test'
    # destination = 'F:/aa'
    sourceL = source.split('\\')
    lognameT = ''
    for x in sourceL:
        if x.find(':') == 1:
            continue
        else:
            lognameT += x

    log = open(destination + '\\time' + source[0] + lognameT + '.log', 'w')
    log.write("Program SearchFile started at : " + time.strftime("%Y-%m-%d %X",time.localtime()) + "\n")
    c,t,z,r,m,q= GetFiles(source) 
    log.write("Program SearchFile finished at : " + time.strftime("%Y-%m-%d %X",time.localtime()) + "\n")

    flist = open(destination + '\\FileLists' + source[0] + lognameT + '.txt','w')
    
    longfilename = open(destination + '\\LongFilename' + source[0] + lognameT + '.txt','w')


    log.write("Program MoveFile started at : " + time.strftime("%Y-%m-%d %X",time.localtime()) + "\n")
    flist.write('==============================All Config files============================\n')
    for x in c:
        if len(x) > 240:    #文件路径超过255后，无法复制、移动
            longfilename.write(x[0] + '\n')
        else:
            flist.write(x[0] + "              Content:" + x[1] )
            movefile(x[0],destination + '\\')
    flist.write('==============================All TXT files============================\n')
    for x in t:
        if len(x) > 240:
            longfilename.write(x[0] + '\n')
        else:
            flist.write(x[0] + "              Content:" + x[1] )
            movefile(x[0],destination + '\\')
    flist.write('==============================All ZIP/RAR files============================\n')
    for x in z:
        if len(x) > 240:
            longfilename.write(x + '\n')
        else:
            flist.write(x + '\n')
            movefile(x,destination + '\\')
    for x in r:
        if len(x) > 240:
            longfilename.write(x + '\n')
        else:
            flist.write(x + '\n')
            movefile(x,destination + '\\')
    flist.write('==============================All Map files============================\n')
    for x in m:
        if len(x) > 240:
            longfilename.write(x + '\n')
        else:
            flist.write(x + '\n')
            movefile(x,destination + '\\')
    flist.write('==============================All Qmap files============================\n')
    for x in q:
        if len(x) > 240:
            longfilename.write(x + '\n')
        else:
            flist.write(x + '\n')
            movefile(x,destination + '\\')

    flist.close()
    longfilename.close()
    log.write("Program MoveFile finished at : " + time.strftime("%Y-%m-%d %X",time.localtime()) + "\n")
    log.close()





if __name__ == '__main__':
    
    main()
    input('Please press any key to exit!')