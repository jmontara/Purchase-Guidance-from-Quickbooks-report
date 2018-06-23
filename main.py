# filename:  main.py

### Purchase Guidance takes data from reports generated in
### QuickBooks and transforms data into information:

###	Data Input (QuickBooks reports):
###		Inventory Item Quick Report (iiqr.csv)
###		Inventory Status by Item (issbi.csv)
###		Purchases by Item Detail (pbid.csv)

### Data Output (flat files and/or print to console):
###   	Indented Bills of Materials
###		Sales history
###		Purchase Guidance


### comment/uncomment file location to run on different machines


### locations for input files on laptop:
iiqrLocation ='C:\Users\Moore\Dropbox (Visitech)\Company Forms\Inventory\Purchase Guidance\iiqr.csv'
issbiLocation ='C:\Users\Moore\Dropbox (Visitech)\Company Forms\Inventory\Purchase Guidance\issbi.csv'
### locations for output files on laptop:
purchaseguidanceLocation ='C:\Users\Moore\Dropbox (Visitech)\Company Forms\Inventory\Purchase Guidance\purchaseguidance.txt'
itemFilesOutDir = 'C:\Users\Moore\Dropbox (Visitech)\Company Forms\Inventory\Purchase Guidance\item files showing history of builds & demand from sales\\'

### location for input files on desktop
iiqrLocation = 'C:\Users\john\Dropbox (Visitech)\Company Forms\Inventory\Purchase Guidance\iiqr.csv'
issbiLocation= 'C:\Users\john\Dropbox (Visitech)\Company Forms\Inventory\Purchase Guidance\issbi.csv'
### location for output files on desktop
purchaseguidanceLocation ='C:\Users\john\Dropbox (Visitech)\Company Forms\Inventory\Purchase Guidance\purchaseguidance.txt'
itemFilesOutDir = 'C:\Users\john\Dropbox (Visitech)\Company Forms\Inventory\Purchase Guidance\item files showing history of builds & demand from sales\\'


# standard library
import csv
import string 
import datetime

# classes 
import classes.transaction
# import classes.itemStats 

# functions
import functions.readiiqr
import functions.readissbi
import functions.buildItems
import functions.buildItemBoms
import functions.buildItemIndentedBoms
import functions.writeItemFiles
import functions.setTransactionSaleDate
import functions.addItemPhantoms
import functions.itemStatsFxns
import functions.checkTotOH
import functions.writepurchaseguidance
# import functions.writepurchasetriggerfile





transactions, itemStatsFromIiqr = functions.readiiqr.readiiqr(iiqrLocation)	
		

items = functions.buildItems.buildItems(
							transactions = transactions,
							itemStatsFromIiqr = itemStatsFromIiqr)

print "buildItems() yields", len(items), "items"
# limit = 10
# for item in items:
	# print "item name & desc:", item.getItemName(), item.getItemDesc()
	# print item.getXactionsStr()
	# print "creating transaction:", item.getItemCreatingTransaction()
	# print item
	# limit -=1
	# if limit < 0:
		# break
# print "buildItems() yields", len(items), "items"
# assert False

functions.readissbi.readissbi(filename = issbiLocation, 
							  items = items)
# for item in items:
	# print item
# assert False
	

functions.buildItemBoms.buildItemBoms(trans = transactions, 
									  items = items)
# count = 0
# for item in items:
	# if not item.getBom() == None:
		# print item.getBom()
		# count += 1
# print "buildItemBoms yields", count, "bills of materials"		
# assert False


functions.buildItemIndentedBoms.buildItemIndentedBoms(items = items)
# for item in items:
	# print item.getIbom()
# assert False


invoiceTransactions = functions.\
					  setTransactionSaleDate.\
					  setTransactionSaleDate(transactions = transactions)
# limit = 500
# for t in invoiceTransactions:
	# print "invoice transaction with sale date:", t
	# limit -= 1
	# if limit < 0:
		# break
# assert False
		

phantomSales = functions.\
			   addItemPhantoms.\
			   addItemPhantoms(items = items)
# print "itemHistories:", itemHistories
# print "phantomSales() yields", len(phantomSales), "transactions"
# limit = 1000
# for transaction in phantomSales:
	# print "phantomSales", transaction
	# limit -=1
	# if limit < 0:
		# break
# assert False
	
print "functions.itemStatsFxns.setItemsStats,", type(functions.itemStatsFxns.setItemsStats)		
functions.itemStatsFxns.setItemsStats(items=items, transactions=transactions)
		
# itemNames = ['BP-2000-MP-6-220V', 'BP2-AB-6-Assy', 
			 # 'V0086', 'BP2-AB-6-Board-Empty']		
# for item in items:
	# if item.getItemName() in itemNames:
		# print item.getItemStats().__str__()

for item in items:
	print item

for item in items:
	if item.getItemName() == "BP-2000-CU-220V":
		print item

count = 0	
print "\n\n\n\n\npurchased items:"	
for item in items:
	if item.isPurchased():
		print item
		count += 1
print "\nThere are ", count, "inventory items."

# print "type(functions.writepurchaseguidance):", type(functions.writepurchaseguidance)
functions.writepurchaseguidance.writepurchaseguidance(items, purchaseguidanceLocation)


def writeItemSales(outFileName = "itemsales.csv", item = items):		
	"""
	# Export item phantom sale transactions into a csv	
	# that can be read into excel to graph history
	# of sales of an item.
	
	"""
	
	with open(outFileName, 'wb') as f:
		csv_writer = csv.writer(f)
		# header row
		itemName = "itemName"
		itemDesc = "itemDesc"
		saleDate = "saleDate"
		saleYear = "saleYear"
		saleMonth = "saleMonth"
		saleQty = "saleQty"
		csv_writer.writerow([itemName, itemDesc, saleDate, saleYear, saleMonth, saleQty]) 
		for item in items:
			for xaction in item.getXactions():
				if xaction.getType() == "Phantom Sale":
					itemName = item.getItemName()
					itemDesc = item.getItemDesc()
					saleDate = xaction.getDate().__str__()
					saleYear = xaction.getDate().year
					saleMonth = xaction.getDate().month
					saleQty = xaction.getQty()
					csv_writer.writerow([itemName, itemDesc, saleDate, saleYear, saleMonth, saleQty]) 
	

writeItemSales()
# for item in items:
	# print item.getItemStats().__str__()
		
# for item in items:
	# if item.getItemName() == "v0091":
		# print item.getXactionsStr()


functions.writeItemFiles.writeItemFiles(
										items = items, 
										outDir = itemFilesOutDir)		

functions.checkTotOH.checkTotOH(items = items)	
			
		
# if __name__ == main:
	# print "hey"	