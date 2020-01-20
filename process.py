import os, hashlib, time, datetime
import multiprocessing as mp

results = []

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

def collect_results(result):
    results.extend(result)

if __name__ == "__main__":
    p = mp.Pool(processes=2)
    files = listFiles('E:\shared')
    startTime = datetime.datetime.now()
    for f in files:
            p.apply_async(calcMD5, args=(f, ), callback=collect_results)
    p.close()
    p.join()
    print(results)
    
    endTime = datetime.datetime.now()
    timeDiff = endTime - startTime
    timeDiffSeconds = timeDiff.seconds
    print('总费时{0}分钟{1}秒'.format(int(timeDiffSeconds/60), int(timeDiffSeconds%60)))