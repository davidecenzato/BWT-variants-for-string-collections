#!/usr/bin/env python

# script for replacing a character in a text

import sys, os, tempfile

def replace_char(path,current,new):
	tmp=tempfile.mkstemp()
	newLine = chr(10)
	zeroChar = chr(0)
	with open(path) as fd1, open(tmp[1],'w') as fd2:
		for line in fd1:
			if(current == "newline"):
				line = line.replace(newLine,new)
			elif(current == "zero"):
				line = line.replace(zeroChar,new)
			else:
				line = line.replace(current,new)
			fd2.write(line)

	os.rename(tmp[1],path)