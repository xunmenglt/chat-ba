import os
import time
from filelock import FileLock
import random
from concurrent.futures import ThreadPoolExecutor
lock_path="data.txt.lock"
file_path="data.txt"
def write_text_to_file(content):
    lock=FileLock(lock_path)
    print("加载锁",content)
    with lock:
        with open(file_path,'r',encoding="utf8") as fp:
            n=fp.readline()
            if not n:
                n=0
            n=int(n)
            n+=1
        with open(file_path,'w',encoding="utf8") as fp:
            fp.write(str(n))
            fp.write("\n")
        # time.sleep(random.randint(1,5))
    print("释放锁",content)

with ThreadPoolExecutor(max_workers=10) as pool:
    pool.map(write_text_to_file,[f"thread-${i}" for i in range(50)])
        
        
