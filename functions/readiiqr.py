# readiiqr.py

# standard library
import csv
import datetime

import classes.transaction


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
			transactions.append(classes.transaction.Transaction(itemName, itemDesc, tran, type, 
								 dte, num, qty, so))	
				
	return transactions, itemStatsFromIiqr


## Multiple iiqr files may be read, due to QuickBooks
# output csv file #  size limitation.  This is required
# read all transactions.  A single file has been seen capable
# of storing greater than 15,000 transactions, which
# equates to more than 3 years of transactions for some
# companies.

# transaction slices from less than 3,080 KB csv file size.
# transactions, itemStatsFromIiqr = readiiqr("iiqr2004-01-01-to-2007-12-31.CSV")
# transactionsSlice1, itemStatsFromIiqr = readiiqr("iiqr2008-01-01-to-2010-12-31.CSV")
# transactions = transactions + transactionsSlice1
# transactionsSlice2, itemStatsFromIiqr = readiiqr("iiqr2011-01-01through2014-12-31.CSV")
# transactions = transactions + transactionsSlice2
# transactionsSlice3, itemStatsFromIiqr = readiiqr("iiqr2015-01-01-to-2018-01-31.CSV")
# transactions = transactions + transactionsSlice3


# print '\nshowing iiqrItemStats:'
# for item in itemStatsFromIiqr:
	# print item
	
# limit = 2
# soNums = []
# print "\nshowing", limit , 'Transactions of type "Invoice"'
# for t in transactions:
	# if t.type == "Invoice":
		# print t
		# soNums.append(t.getInvoiceSoNum())
		# limit -= 1
		# if limit <= 0:
			# break
# limit = 2
# print "\nshowing Transactions related to those listed above"
# for t in transactions:
	# if (t.type == "Sales Order" and t.getNum() in soNums):
		# print t
		# limit -= 1
		# if limit <= 0:
			# break
# print "readiiqr() yields", len(transactions), "transactions"
# assert False