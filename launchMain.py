# launchMain.py

# Periodically checks for newly created input file.  
# Launches main when file is found.


import time
import os

sleepSeconds = 2

indent = ''
path = './launchMainTest.foo'
fileTime = 0.0


def filetime(path=path): 	
	""" returns time of file """
	# print "in filetime"
	# print "os.path.getmtime(path):", os.path.getmtime(path)
	ret = os.path.getmtime(path)
	print "       type(ret):", type(ret)
	print "       ret:", ret
	return ret

while True:
	
	if indent == '.....':
		indent = ''
	else:
		indent += '.'
	print indent, 
	print " time.sleep(sleepSeconds) expired. ", 
	print "Press <cntl>-C to exit program."
	
	time.sleep(sleepSeconds)

	newFileTime = filetime()
	
	if newFileTime>fileTime:
		print "newFileTime>fileTime; new file to be parsed"
		fileTime = newFileTime
	

	

	
	
	
