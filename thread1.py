#!/usr/bin/python3
import os, hashlib, binascii, time, json, datetime, threading, queue

def listFiles(dir):
    paths = []
    for root,dirs,files in os.walk(dir):
        for file in files:
            paths.append(os.path.join(root,file))
            
    return paths
    
        
class threadMD5(threading.Thread):
    global result
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
    
    def run(self):
        while True:
            try:
                filePath = self.queue.get(block=False)
            except Exception as e:
                print('thread end')
                break
            fileMD5 = calcMD5(filePath)
            result.append(fileMD5)
            self.queue.task_done()

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
    
startTime = datetime.datetime.now()
files = listFiles('E:\Shared')

result = []

#多线程
queue = queue.Queue()
for i in files:
    queue.put(i, block=False)

threads = []

for i in range(4):
    t = threadMD5(queue)
    t.setDaemon(True)
    t.start()
    threads.append(t)

for i in threads:
    i.join()

print(result)

endTime = datetime.datetime.now()
timeDiff = endTime - startTime
timeDiffSeconds = timeDiff.seconds
print('总费时{0}分钟{1}秒'.format(int(timeDiffSeconds/60), int(timeDiffSeconds%60)))