#!/usr/bin/env python

import os
import hashlib
import sys
from multiprocessing import Process, Queue
import time
from shutil import copy2
import re

#windows: without raw string -> error
dir_base = r'C:\Users\szp\Desktop\backup_files'
dir_usb = r'E:\backup_files'

to_be_changed = {}

def f_base(q):
    """ add local files (as a key) and their checksum (as a value) to dict """
    base_dict = {}
    count = 0
    for path, dirs, files in os.walk(dir_base):
        for f in files:
            if os.path.isfile(path + r'\{}'.format(f)):
                count += 1
                with open(path + r'\{}'.format(f), 'rb') as of:
                    fc = of.read()
                    base_dict[path + r'\{}'.format(f)]=( hashlib.md5(fc).hexdigest() )
    print("base dict:", len(base_dict.items()))
    print("base:", count)
    q.put(base_dict)

def f_usb(q2):
    """ add usb files (as a key) and their checksum (as a value) to dict """
    usb_dict = {}
    count = 0
    for path, dirs, files in os.walk(dir_usb):
        for f in files:
            if os.path.isfile(path + r'\{}'.format(f)):
                count += 1
                with open(path + r'\{}'.format(f), 'rb') as of:
                    fc = of.read()
                    usb_dict[path + r'\{}'.format(f)]=( hashlib.md5(fc).hexdigest() )
    print("usb dict:", len(usb_dict.items()))
    print("usb:", count)
    q2.put(usb_dict) 

def compare_dicts():
    """ compare both dictionaries and find updated/new files from source """
    print("=== start checking ===")
    for key, value in a_usb_dict.items():
        if value not in a_base_dict.values():
            print(key, value)
            to_be_changed[key] = value
    print("=== checked ===")
    if to_be_changed:
        return 1
    else:
        return 0

def update_files():
    """ base on data from compare_dicts() it will update files """
    print("=== updating ===")
    for key, value in to_be_changed.items():
        print("src:", key)
        #stupid windows, problem with \ vs \\
        #key_src = re.sub(r'{}'.format(dir_usb) ,'', r'{}'.format(key), count=1)
        key_src = key.replace(dir_usb, '')
        key_base = os.path.join(dir_base + key_src)
        print("dest:", key_base)
        if not os.path.exists('\\'.join(key_base.split('\\')[:-1])):
            print '\\'.join(key_base.split('\\')[:-1])
            os.makedirs('\\'.join(key_base.split('\\')[:-1]))
        copy2(key, key_base)
    print("=== updated ===")

def fire():
    """ run... """
    global a_base_dict, a_usb_dict
    if os.path.exists(dir_base) and os.path.exists(dir_usb):
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
        
        # 'if' statement is needed to not run 'update_files()' if there are no files to be updated
        if compare_dicts():
            update_files()
        else:
            print("=== completed ===")
    else:
        sys.exit("Missing directories")
        
if __name__=='__main__':
    fire()
  
    

