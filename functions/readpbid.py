# readpbid.py

# standard library
import csv
import datetime

# import classes.transaction


# def readpbid(items = items, filename = "pbid.csv"):
def readpbid(filename, items):
	""" 
	Reads purchases by item detail, a qb generated report. 
	Updates the item object associated with each item
	in the list of Item objects.
	
	Inputs:
	items 		-   list of Item objects
	
	filename	- 	str, filname of quickbooks generated report, 
					 purchases by item detail


	"""
	
	# itemPbidRows = []
	
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

			# disregard rows that start with "Total"
			if row[0][:len("Total")] == "Total":
				continue
				
			# print "row:", row	
			
			# get itemName and description in 1st column
			itemEnd = row[0].find("(")-1
			if itemEnd > -1:			
				itemName = row[0][:itemEnd]
				itemDesc = row[0][itemEnd+2:-1]

			# print "\n  itemName, itemDesc:", itemName,", ", itemDesc
			
		
			# # get other things that appear in row[0]
			# if row[0][:len("Total")] == "Total": #  + itemName +  (" + itemDesc + ")": 
				# qty = row[6]
				# itemStatsFromPbid.append((itemName, itemDesc, "Qty", qty ))
				# print "itemName, itemDesc, qty", itemName, itemDesc, qty
				# continue # to next row
				
			# elif row[0][:len("Tot On Purchase Order")] == "Tot On Purchase Order":
				# qty = row[7]
				# itemStatsFromPbid.append((itemName, itemDesc, "Tot On Purchase Order", qty ))
				# continue # to next row
			
			# elif row[0][:len("Tot On Sales Order")] == "Tot On Sales Order":
				# qty = row[7]
				# itemStatsFromPbid.append((itemName, itemDesc, "Tot On Sales Order", qty ))
				# continue # to next row
			
			# "Bill", "Credit Car", and etc, are caught here	
			if not row[2] == "":
				type = row[1]
				dte = row[2]
				num = row[3]
				memo = row[4]
				source = row[5]
				qty = row[6]
				um = row[7]
				costPrice = row[8]
				amount = row[9] 

				print "\nitemName:", itemName, "row[x]:", costPrice #, type(costPrice)	
				for item in row:
					
					print "  ", item,
			
			else:
				continue # to next row

			# select relevant Item object and set value
			for item in items:
				if item.getItemName() == itemName:
					try:
						print "\nitemName:", itemName, "costPrice:", costPrice
						# print "type(item):", type(item)
						item.setItemStatsFromPbid(costPrice)
						print "item.getunitcost()", item.getunitcost()
					except:
						print "fail to setItemStatsFromPbid"
						assert False
						pass	
						
			#convert dte to datetime
			# mmddyy = dte.split("/")
			# dte = datetime.date(int(mmddyy[2]),int(mmddyy[0]),int(mmddyy[1]))
			
			# print "\t\ttype, dte, num, costPrice", type, dte, num, costPrice
			#create Transaction and append to transactions
			# transactions.append(classes.transaction.Transaction(itemName, itemDesc, tran, type, 
								 # dte, num, qty, so, name, memo))	
				
	# return transactions, itemStatsFromPbid


if __name__ == "__main__":		
	print "In readpbid.py"
	# import transaction
	pbidLocation= 'C:\Users\john\Dropbox (Visitech)\Company Forms\Inventory\Purchase Guidance\pbid.csv'
	ret = readpbid(pbidLocation)
	# print "ret:", ret
	
	## Multiple iiqr files may be read, due to QuickBooks
	# output csv file #  size limitation.  This is required to
	# read all transactions.  A single file has been seen capable
	# of storing greater than 15,000 transactions, which
	# equates to more than 3 years of transactions for some
	# companies.

	# transaction slices from less than 3,080 KB csv file size.
	# transactions, itemStatsFromPbid = readiiqr("iiqr2004-01-01-to-2007-12-31.CSV")
	# transactionsSlice1, itemStatsFromPbid = readiiqr("iiqr2008-01-01-to-2010-12-31.CSV")
	# transactions = transactions + transactionsSlice1
	# transactionsSlice2, itemStatsFromPbid = readiiqr("iiqr2011-01-01through2014-12-31.CSV")
	# transactions = transactions + transactionsSlice2
	# transactionsSlice3, itemStatsFromPbid = readiiqr("iiqr2015-01-01-to-2018-01-31.CSV")
	# transactions = transactions + transactionsSlice3


	# print '\nshowing iiqrItemStats:'
	# for item in itemStatsFromPbid:
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