# readperformancecycles2.py

# standard library
import csv

def readperformancecycles2():
	""" 
	Reads performancecycles2.csv, 
	
	This file must be located as follows
	    'C:\Users\john\Documents\GitHub\Purchase-Guidance-from-Quickbooks-report\performanceCycles2.csv'

	This file is manually generated and contains 
	the following columns:
		itemName, successorName
	
	Where one item must be purchased prior to purchase of another
	item, the one item is referred to herein as a successor item.
		

	Outputs:
	a dictionary, itemName: successorName
	"""
	
	filename = 'C:\Users\john\Documents\GitHub\Purchase-Guidance-from-Quickbooks-report\performanceCycle2.csv'

	
	ret = {}
	
	skipRows = 1 
	
	with open(filename, 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			
			# disregard top row(s)
			skipRows -= 1
			try:
				assert skipRows < 0
			except:
				continue
			
			# get itemName and successorName
			itemName = row[0]
			itemSuccessor = row[1]
		
			ret[itemName] = itemSuccessor 
				
	return ret

if __name__ == "__main__":
	listOfTuples = readperformancecycles2()
	print listOfTuples
	