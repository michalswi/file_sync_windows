#!/usr/bin/env python

import os
import hashlib
import sys
from multiprocessing import Process, Queue
import time
from shutil import copy2
import re
import logging

logging.basicConfig(filename='syncLinux.log')
logger = logging.getLogger("SyncFilesLinux")
logger.setLevel(logging.INFO)

DIR_BASE = r'{}'.format(sys.argv[1])
DIR_USB = r'{}'.format(sys.argv[2])

TO_BE_CHANGED = {}

def f_base(q):
    """ add local files (as a key) and their checksum (as a value) to dict """
    base_dict = {}
    #count should be equal to the number of items in base_dict.
    count = 0
    #https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python
    #https://www.tutorialspoint.com/python/os_walk.htm
    for path, dirs, files in os.walk(DIR_BASE):
        for f in files:
            if os.path.isfile(path + r'/{}'.format(f)):
                count += 1
                with open(path + r'/{}'.format(f), 'rb') as of:
                    fc = of.read()
                    base_dict[path + r'/{}'.format(f)]=( hashlib.md5(fc).hexdigest() )
    b_d_len = len(base_dict.items())                    
    logger.info('\nBase dict length: {} \nBase count: {}'.format(b_d_len, count))
    q.put(base_dict)

def f_usb(q2):
    """ add usb files (as a key) and their checksum (as a value) to dict """
    usb_dict = {}
    #count should be equal to the number of items in base_dict.
    count = 0
    for path, dirs, files in os.walk(DIR_USB):
        for f in files:
            if os.path.isfile(path + r'/{}'.format(f)):
                count += 1
                with open(path + r'/{}'.format(f), 'rb') as of:
                    fc = of.read()
                    usb_dict[path + r'/{}'.format(f)]=( hashlib.md5(fc).hexdigest() )
    u_d_len = len(usb_dict.items())
    logger.info('\nUSB dict length: {} \nUSB count: {}'.format(u_d_len, count))
    q2.put(usb_dict) 

def compare_dicts():
    """ compare both dictionaries and find updated/new files from source """
    logger.info('\n=== comparing dictionaries.. ===')
    print('=== comparing dictionaries.. ===')
    for key, value in a_usb_dict.items():
        if value not in a_base_dict.values():
            print(key, value)
            TO_BE_CHANGED[key] = value
    logger.info("\n{} \n=== compared ===".format(TO_BE_CHANGED))
    print('=== compared ===')    
    
    if TO_BE_CHANGED:
        return 1
    else:
        return 0

def update_files():
    """ base on data from compare_dicts() it will update files """
    logger.info('\n=== updating files.. ===')
    print('=== updating files.. ===')
    #https://stackoverflow.com/questions/123198/how-do-i-copy-a-file-in-python
    for key, value in TO_BE_CHANGED.items():
        print('src:', key)
        key_src = re.sub('{}'.format(DIR_USB) ,'', '{}'.format(key), count=1)
        key_base = os.path.join(DIR_BASE + key_src)
        print('dest:', key_base)
        # split.. : if you have '/dir1/dir2/file' it will remove 'file' and create '/dir1/dir2'
        if not os.path.exists("/".join(key_base.split('/')[:-1])):
            os.makedirs("/".join(key_base.split('/')[:-1]))
        copy2(key, key_base)
    logger.info('\n=== updated ===')
    print('=== updated ===')

def fire():
    """ run... """
    global a_base_dict, a_usb_dict

    #https://stackoverflow.com/questions/17927173/collecting-result-from-different-process-in-python
    if os.path.exists(DIR_BASE) and os.path.exists(DIR_USB):
        q = Queue()
        q2 = Queue()
        
        p1 = Process(target=f_base, args=(q,))
        p1.start()
        p2 = Process(target=f_usb, args=(q2,))
        p2.start()    
        
        a_base_dict = q.get()
        a_usb_dict = q2.get()
        
        p1.join()
        p2.join()
        
        #print(len(a_base_dict))
        #print(len(a_usb_dict))

        #time.sleep(10)
        
        # 'if' statement is needed to not run 'update_files()' if there are no files to be updated
        if compare_dicts():
            update_files()
        else:
            print("=== completed ===")
    else:
        sys.exit("Missing directories")

if __name__=='__main__':
    fire()