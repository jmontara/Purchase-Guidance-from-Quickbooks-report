# launchMain.py

# Periodically checks for newly created input file.  
# Launches main when file is found.

import time
import os

import main # launch script on entry


def filetime(path): 	
	""" 
	returns time of file modification or creation

	inputs:
	path - string representation of path and filename 
	
	outputs:
	return - float, time of file modification or creation
	return - float, 0.0 if the file does not exist		 
	
	"""
	try: 
		return os.path.getmtime(path)
	except: 
		return 0.0


def check_repeat_report(path,
						sleepSeconds=2):
	""" 
	Check for newly created input file,  
	launch main.py when found, and repeat.	
	
	Inputs:
	path 			- string, representation of path and filename
	sleepSeconds 	- int, delay between checks 
	"""
	
	indent = ''
	fileTime = filetime(path) 
	while True:
		
		if indent == '.....':
			indent = ''
		else:
			indent += '.'
		print indent, 
		print " time.sleep(sleepSeconds) expired. ", 
		print "Press <cntl>-C to exit program."
		
		time.sleep(sleepSeconds)

		newFileTime = filetime(path)
		
		if newFileTime>fileTime:
			print newFileTime,">",fileTime, "new file to be parsed"
			fileTime = newFileTime
			reload(main)

if (__name__ == '__main__'):
	
	# to test uncomment this block
	print "To test this program, modify launchMainTest.foo"
	print "and examine output.\n\n"
	check_repeat_report(path='./launchMainTest.foo')
	
	
	
	