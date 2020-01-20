#!/usr/bin/python3
import os, hashlib, binascii, time, json, datetime

def listFiles(dir):
    paths = []
    for root,dirs,files in os.walk(dir):
        for file in files:
            paths.append(os.path.join(root,file))
            
    return paths
    
def calcMD5(filePath, block_size=2**20):
    md5 = hashlib.md5()
    f = open(filePath, 'rb')
    while True:
        data = f.read(block_size)
        if not data:
            break
        md5.update(data)
    f.close()
    return md5.hexdigest()
        
files = listFiles('E:\Shared')

result = []

startTime = datetime.datetime.now()

for i in files:
    fileMD5 = calcMD5(i)
    result.append(fileMD5)

print(result)

endTime = datetime.datetime.now()
timeDiff = endTime - startTime
timeDiffSeconds = timeDiff.seconds
print('总费时{0}分钟{1}秒'.format(int(timeDiffSeconds/60), int(timeDiffSeconds%60)))
