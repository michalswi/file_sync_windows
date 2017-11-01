#!/usr/bin/env python

import os
import hashlib
#maybe
#https://bitbucket.org/vds2212/rsync.py/src/7349f4e532ff9f6d9db37e8b36566327141d9964/rsync.py?at=default&fileviewer=file-view-default

#without raw string error
dir_base = r'C:\Users\szp\Desktop\backup_files'
dir_usb = r'E:\backup_files'

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
#https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python
#11254
count = 0
num = 0
file_dict = {}
lst = []
for path, dirs, files in os.walk(dir_base):
  #print path
  for f in files:
	#print path+f
	#count should be equal to the number of items in file_dict.
	count += 1
	with open(path + r'\{}'.format(f)) as of:
		fc = of.read()
		num += 1
		file_dict[hashlib.md5(fc).hexdigest()]=( path + r'\{}'.format(f) )
			
print(len(file_dict.items()))
print(count)
print(num)

