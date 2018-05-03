# filename:  functions.py

import csv
import datetime
import transaction

def readiiqr(filename = "iiqr.csv"):
	""" 
	Reads Inventory Item Quick Reports, a qb generated report. 
	Creates and returns a list of Transaction objects.

	Also, creates and returns a list of item statistics.

	
	Inputs:
	filename	- 	str, filname of quickbooks generated report, 
					 inventory item quick report


	Outputs:
	transactions 			- list, a list of transaction objects.	
	itemStatsFromIiqr		- list, a list of tuples taking the form			
								(itemName, itemDesc, value, qty)
								 where value is a subset of 
								 ["Tot on Hand"
								 , "Tot on Sales Order"
								 , "Tot on Purchase Order"]
	"""
	transactions = []
	itemStatsFromIiqr = []
	
	skipRows = 2 
	
	with open(filename, 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			
			# disregard top row(s)
			skipRows -= 1
			try:
				assert skipRows < 0
			except:
				continue
			
			# get itemName and description
			itemEnd = row[0].find("(")-1
			if itemEnd > -1:			
				itemName = row[0][:itemEnd]
				itemDesc = row[0][itemEnd+2:-1]
			
			# get other things that appear in row[0]
			if row[0][:11] == "Tot On Hand": 
				qty = row[7]
				itemStatsFromIiqr.append((itemName, itemDesc, "Tot On Hand", qty ))
				continue # to next row
				
			elif row[0][:len("Tot On Purchase Order")] == "Tot On Purchase Order":
				qty = row[7]
				itemStatsFromIiqr.append((itemName, itemDesc, "Tot On Purchase Order", qty ))
				continue # to next row
			
			elif row[0][:len("Tot On Sales Order")] == "Tot On Sales Order":
				qty = row[7]
				itemStatsFromIiqr.append((itemName, itemDesc, "Tot On Sales Order", qty ))
				continue # to next row
			
			# "Build Assembly", "Invoice", "Sales Orders", "Bills", etc, are caught here	
			if not row[2] == "":
				tran = row[1]
				type = row[2]
				dte = row[3]
				num = row[4]
				qty = row[7]
				so = row[9]			
			else:
				continue # to next row

			#convert dte to datetime
			mmddyy = dte.split("/")
			dte = datetime.date(int(mmddyy[2]),int(mmddyy[0]),int(mmddyy[1]))
			
			#create Transaction and append to transactions
			transactions.append(transaction.Transaction(itemName, itemDesc, tran, type, 
								 dte, num, qty, so))	
				
	return transactions, itemStatsFromIiqr

	
	