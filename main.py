# filename:  purchaseG.py

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


transactions, itemStatsFromIiqr = functions.readiiqr.readiiqr()	
		

items = functions.buildItems.buildItems(
							transactions = transactions,
							itemStatsFromIiqr = itemStatsFromIiqr)

# print "buildItems() yields", len(items), "items"
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

functions.readissbi.readissbi(filename = "issbi.csv", 
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


print "\nPurchases required to fill Sales Orders and Maintain RO point:"
countItemsToPurchase = 0
for item in items:
	if item.getPurchase2() > -0.0:
		purchQty = item.getPurchase2()
		print "  Purchase qty ", purchQty, " of ", item.getItemName(),
		print " ", item.getItemDesc()
		countItemsToPurchase += 1
print "Purchase of ", countItemsToPurchase, "item(s) required to fill Sales Orders and Maintain RO point"

print "\nPurchase required to fill Sales Orders:"
countItemsToPurchase = 0
for item in items:
	if item.getPurchase1() > -0.0:
		purchQty = item.getPurchase1()
		print "  Purchase qty ", purchQty, " of ", item.getItemName(),
		print " ", item.getItemDesc()
		countItemsToPurchase += 1
print "purchase of ", countItemsToPurchase, "item(s) is required to build open SOs"


print "\nOpen purchase orders exist for the following items:"
countItemsPurchased = 0
for item in items:
	if item.getTotPO() > 0.01:
		purchQty = item.getTotPO()
		print "  Purchased qty ", purchQty, " of ", item.getItemName(),
		print " ", item.getItemDesc()
		countItemsPurchased += 1
print "receipt of", countItemsPurchased, " item(s) is expected; these items have been purchased"

print "\nThe following items have negative quantities:"
countItemsToBuild = 0
for item in items:
	if item.getTotOH() <=-.01:
		buildQty = item.getTotOH()
		print "  Build qty ", buildQty, " of ", item.getItemName() + " (" + item.getItemDesc() + ")"
		countItemsToBuild += 1
print "QB inventory adjust or logical build could correct negative counts of:", countItemsToBuild, "item(s)."		

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
										outDir = 'itemFiles')		
		
# if __name__ == main:
	# print "hey"
	
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
			
	