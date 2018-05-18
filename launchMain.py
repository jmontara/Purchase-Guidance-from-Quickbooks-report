# launchMain.py

# Periodically checks for newly created input file.  
# Launches main when file is found.

import time
import os



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
		ret = os.path.getmtime(path)
	except: 
		ret = 0.0
	return ret

def check_repeat_report(path='./launchMainTest.foo',
						sleepSeconds=2):
	""" 
	Check for newly created input file, report check, launch
	main.py when found, and repeat.	
	
	Inputs:
	path 			- string, representation of path and filename
	sleepSeconds 	- int, delay between checks 
	"""
	
	indent = ''
	fileTime = 0.0 
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
			print "newFileTime>fileTime; new file to be parsed"
			fileTime = newFileTime

if (__name__ == '__main__'):
	# execute as standalone using >python launchMain.py
	
	print filetime(path='./launchMainTest.foo')
	check_repeat_report()
	

	
	
	
