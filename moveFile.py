import os
import sys
import getopt
import shutil


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
    # try:
    #     opts,args=getopt.getopt(sys.argv[1:],"hs:d:",["help","source=","des_dir="]) #hs:d: 表示参数-h 不需要值，：表示需要值
    # except getopt.GetoptError as error:
    #     print(str(error))
    #     sys.exit(2)

    # for key,value in opts:
    #     if key == '-s':
    #         source = value
    #     if key == '-d':
    #         des_dir = value
    #     if key == '-h':
    #         print(" -s <source_dir> -d <des_dir_dir>")
    

    source = 'M:/QA Data'
    des_dir = 'Y:/'
    sourceL = source.split('\\')
    lognameT = ''
    for x in sourceL:
        if x.find(':') == 1:
            continue
        else:
            lognameT += x

 

    flist = open('Y:/FileList.txt','r')
    
    longfilename = open(des_dir + '\\LongFilename' + source[0] + lognameT + '.txt','w')
    
    errorlog = open(des_dir + '\\Errotlog' + source[0] + lognameT + '.txt','w')

    for y in flist.readlines():
        x = y.replace("\n",'')
        if len(x) > 240:    #文件路径超过255后，无法复制、移动
            longfilename.write(x + '\n')
        else:
            try:
                movefile(x,des_dir + '\\')
            except:
                errorlog.write(x + '\n')
    

    
    longfilename.close()
    errorlog.close()





if __name__ == '__main__':

    main()
    input('Please press any key to exit!')