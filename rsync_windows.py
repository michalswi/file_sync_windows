#!/usr/bin/env python

import os
import hashlib

#without raw string error
dir_base = r'C:\Users\szp\Desktop\backup_files'
dir_usb = r'E:\backup_files'

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
	    #os.path.isdir()		
	    else:
		    dir_lst.append(dir_base + r'\{}'.format(i))
			
first_run()

print(file_dict.items())
print(dir_lst)			



