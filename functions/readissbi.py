# readissbi in functions

import csv

def readissbi(filename, items):
	""" 
	Reads a qb generated report. 

	Updates item objects with item reorder point.
	
	Inputs:
	filename	- str, filename of quickbooks generated report, 
					 inventory stock status by item
	items	 	- list, a list of item objects to be updated.	
	"""
	
	with open(filename, 'rb') as f:
		reader = csv.reader(f)
		for row in reader:

			# itemName and description in 1st column 
			itemEnd = row[0].find("(")-1	
			itemName = row[0][:itemEnd]		
			itemDesc = row[0][itemEnd+2:-1]

			# roPoint in 3rd column
			roPoint = row[2]
		
			# select relevant Item object and set RO point
			for item in items:
				if item.getItemName() == itemName:
					try:
						item.setItemStatsFromIssbi(roPoint)
					except:
						pass
						# print "\nin readissbi()",itemName, itemDesc, roPoint

			
	# for index in range(len(itemNames)):
		# print "\n\n", index, "  ",  itemNames[index]
		# print itemDescs[index]
		# print roPoints[index]
	
	# assert False