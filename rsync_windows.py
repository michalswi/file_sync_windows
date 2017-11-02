#!/usr/bin/env python

import os
import hashlib
import sys
from multiprocessing import Process, Queue
import time

#windows: without raw string -> error
#dir_base = r'C:\Users\szp\Desktop\backup_files'
#dir_base = r'C:\Users\szp\Desktop\New_folder'
dir_usb = r'E:\backup_files'

dir_base = r'{}'.format(sys.argv[1])
dir_usb = r'{}'.format(sys.argv[2])

"""
#main directory and files
file_dict = {}
dir_lst = []

def first_run():
	
	for i in os.listdir(dir_base):
		#print(i)
		# distinguish between files and directories
		# for file
		if os.path.isfile(dir_base + r'\{}'.format(i)):
			with open(dir_base + r'\{}'.format(i)) as file:
				fc = file.read()
				#checksum:full_path_to_file_and_filename
				file_dict[hashlib.md5(fc).hexdigest()]=(dir_base + r'\{}'.format(i))
		# for directory
		elif os.path.isdir(dir_base + r'\{}'.format(i)):		
			dir_lst.append(dir_base + r'\{}'.format(i))
			
		else:
			print("dupa")
			
first_run()

print(file_dict.items())
print(dir_lst)			
"""
#os.walk()
#https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python

def f_base(q):
    """ add local files (as a key) and their checksum (as a value) to dict """
    base_dict = {}
    
	#count should be equal to the number of items in base_dict.
    count = 0
    for path, dirs, files in os.walk(dir_base):
        for f in files:
            #if os.path.isfile(path + r'\{}'.format(f)):        # windows \
            if os.path.isfile(path + r'/{}'.format(f)):         # linux /
                count += 1
                #with open(path + r'\{}'.format(f), 'rb') as of:
                with open(path + r'/{}'.format(f), 'rb') as of:
                    fc = of.read()
                    #base_dict[path + r'\{}'.format(f)]=( hashlib.md5(fc).hexdigest() )
                    base_dict[path + r'/{}'.format(f)]=( hashlib.md5(fc).hexdigest() )
                    
    print("base dict:", len(base_dict.items()))
    print("base:", count)
    q.put(base_dict)
    

def f_usb(q2):
    """ add usb files (as a key) and their checksum (as a value) to dict """

    usb_dict = {}
    
    #count should be equal to the number of items in base_dict.
    count = 0
    for path, dirs, files in os.walk(dir_usb):
        for f in files:
            if os.path.isfile(path + r'/{}'.format(f)):
                count += 1
                with open(path + r'/{}'.format(f), 'rb') as of:
                    fc = of.read()
                    usb_dict[path + r'/{}'.format(f)]=( hashlib.md5(fc).hexdigest() )
                    
    print("usb dict:", len(usb_dict.items()))
    print("usb:", count)
    q2.put(usb_dict) 


def compare_dicts():
    """ compare both dictionaries and find updated/missing files"""
    
    print("=== start checking ===")
    
    for key, value in usb_dict.items():
        if value not in base_dict.values():
            print key, value

#https://stackoverflow.com/questions/17927173/collecting-result-from-different-process-in-python
if __name__=='__main__':
    q = Queue()
    q2 = Queue()
    
    p1 = Process(target=f_base, args=(q,))
    p1.start()
    p2 = Process(target=f_usb, args=(q2,))
    p2.start()    
    
    base_dict = q.get()
    usb_dict = q2.get()
    
    
    p1.join()
    p2.join()
    
    print(len(base_dict))
    print(len(usb_dict))

    time.sleep(10)
    compare_dicts()
  
    
