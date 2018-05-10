# checkTotOH.py

import classes.item

def checkTotOH(items):
	"""
	checks each item in items to see that it has a 
	    a total on hand value
	
	Inputs:
	items	- 	list, list of item objects
	
	Outputs:
			- printed list of item names for which	
			  total on hand value is none
	"""
	print "\n\nprinting items that have total value on hand None"
	count = 0
	for item in items:
		if item.getTotOH() == None:
			print item
			count += 1
			
	print "there are", count, "items having total value on hand None"

# checkTotOH(items)	