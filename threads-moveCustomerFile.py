import os
import sys
import getopt
import zipfile
import rarfile
import shutil
import time
import threading
import queue




class ThreadCheckFile(threading.Thread):
    global file_list
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
    
    def run(self):
        while True:
            try:
                obj = self.queue.get(block=False)
            except Exception as e:
                #print('thread end')
                break
            self.result = CheckFile(obj[0], obj[1])
            if self.result:
                file_list.append(self.result)

            self.queue.task_done()


def SearchFile(keyword,path):
    '''
    Search if keyword in the file, if yes return true, else return false

    '''
    try:
        with open(path) as f:
            for index, line in enumerate(f.readlines()):
                if keyword in line:
                    #li = [path,line]
                    return True
            
            return False
    except:
        pass
        # with open(path,"r", encoding='utf-8') as f:
        #     for index, line in enumerate(f.readlines()):
        #         if keyword in line:
        #             return True
            
        #     return False
        
    
def CheckFile(file, path):
   
    if file.endswith('.config') :
        Sresult = SearchFile('hostname',path)
        if Sresult:
            return ('Config',path)

    if file.endswith('.txt') :
        Cresult = SearchFile('hostname',path)
        if Cresult:
            return ('Txt',path)

    if file.endswith('.zip') :
        zlist = []
        try :
            zlist = zipfile.ZipFile(path).namelist()
        except :
            pass
        for name in zlist:
            if name.endswith('.config') or name.endswith('.map') or name.endswith('.qmap') :
                return ('Zip',path)
                break
    if file.endswith('.rar') :
        rlist = []
        try :
            rlist = rarfile.RarFile(path).namelist()
        except :
            pass
        for name in rlist:
            if name.endswith('.config') or name.endswith('.map') or name.endswith('.qmap') :
                return ('Rar',path)
                break
    if file.endswith('.map') :
        return ('Map',path)
    if file.endswith('.qmap') :
        return ('Qmap',path)



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
    if not os.path.isfile(srcfile):
        pass
    else:
        fpath,fname=os.path.split(srcfile)    #分离文件名和路径
        dir = dstfile + fpath.replace(':','') #构建目的路径，windows去除盘符后的冒号 Ex: D:\test --> D\test
        if not os.path.exists(dir):
            os.makedirs(dir)                #创建路径
        shutil.move(srcfile,dir + '\\' + fname)      #移动文件
    #pass

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
    # des_dir = 'F:/11'
    sourceL = source.split('\\')
    lognameT = ''
    for x in sourceL:
        if x.find(':') == 1:
            continue
        else:
            lognameT += x

    log = open(des_dir + '\\time' + source[0] + lognameT + '.log', 'w')
    log.write("Program SearchFile started at : " + time.strftime("%Y-%m-%d %X",time.localtime()) + "\n")
    
    
    
    # l = GetFiles(source) 

    queue1 = queue.Queue()
    threads = []
    global file_list
    global lenth
    ignordir = ["QA Data" , "Support Case Data" , "TAC" , "User"]
    #遍历目录中所有文件及子目录文件 
    for root,dirs,files in os.walk(source,topdown=True): 
        #for dir in dirs: 
        #    print(os.path.join(root,dir))
        dirs[:] = [ d for d in dirs if d not in ignordir ]
        for file in files: 
            #print(os.path.join(root,file))
            queue1.put((file,os.path.join(root,file)), block=False)
    #print(queue1)
    log.write("OS walk finished at : " + time.strftime("%Y-%m-%d %X",time.localtime()) + "\n")
    for i in range(8):
        t = ThreadCheckFile(queue1)
        threads.append(t)
        t.start()
        

    for th in threads:
        th.join()




    log.write("Program SearchFile finished at : " + time.strftime("%Y-%m-%d %X",time.localtime()) + "\n")
 

    flist = open(des_dir + '\\FileLists' + source[0] + lognameT + '.txt','w')
    
    longfilename = open(des_dir + '\\LongFilename' + source[0] + lognameT + '.txt','w')
    
    errorlog = open(des_dir + '\\Errotlog' + source[0] + lognameT + '.txt','w')

    log.write("Program MoveFile started at : " + time.strftime("%Y-%m-%d %X",time.localtime()) + "\n")
    flist.write('==============================All files============================\n')

    #print(file_list)
    for x in file_list:
        flist.write(x[0] + "," + x[1] + '\n')
    flist.close()
    
    for x in file_list:
        if len(x[0]) > 240:    #文件路径超过255后，无法复制、移动
            longfilename.write(x[1] + '\n')
        else:
            try:
                movefile(x[1],des_dir + '\\')
            except:
                errorlog.write(x[1] + '\n')
    

    
    longfilename.close()
    log.write("Program MoveFile finished at : " + time.strftime("%Y-%m-%d %X",time.localtime()) + "\n")
    log.close()
    errorlog.close()





if __name__ == '__main__':
    
    file_list = []
    main()
    input('Please press any key to exit!')