# filename:  main.py

### Purchase Guidance takes data from reports generated in
### QuickBooks and transforms data into information:

###	Data Input (QuickBooks reports):
###		Inventory Item Quick Report (iiqr.csv)
###		Inventory Status by Item (issbi.csv)
###		Purchases by Item Detail (pbid.csv)

### comment/uncomment file location to run on different machines
### locations for input files on laptop:
iiqrLocation ='C:\Users\Moore\Dropbox (Visitech)\Company Forms\Inventory\Purchase Guidance\iiqr.csv'
issbiLocation ='C:\Users\Moore\Dropbox (Visitech)\Company Forms\Inventory\Purchase Guidance\issbi.csv'
### location for input files on desktop
iiqrLocation = 'C:\Users\john\Dropbox (Visitech)\Company Forms\Inventory\Purchase Guidance\iiqr.csv'
issbiLocation= 'C:\Users\john\Dropbox (Visitech)\Company Forms\Inventory\Purchase Guidance\issbi.csv'
 
### Data Output (flat files and/or print to console):
###   	Indented Bills of Materials
###		Sales history
###		Purchase Guidance
### locations for output files on laptop:
purchaseguidanceLocation ='C:\Users\Moore\Dropbox (Visitech)\Company Forms\Inventory\Purchase Guidance\purchaseguidance.txt'
itemFilesOutDir = 'C:\Users\Moore\Dropbox (Visitech)\Company Forms\Inventory\Purchase Guidance\item files showing history of builds & demand from sales\\'
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
# import functions.writepurchasetriggerfile





transactions, itemStatsFromIiqr = functions.readiiqr.readiiqr(iiqrLocation)	
		

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


### 
###  Write file summarizing purchasing guidance
### 

str = "\nPurchases required to fill Sales Orders and Maintain RO point:"

print "\nPurchases required to fill Sales Orders and Maintain RO point:"
countItemsToPurchase = 0
for item in items:
	if item.getPurchase2() > -0.0:
		purchQty = item.getPurchase2().__repr__()
		str += '\n'
		str += "  Purchase qty " + purchQty + " of " + item.getItemName()
		str += item.getItemDesc()
		print "  Purchase qty ", purchQty, " of ", item.getItemName(),
		print " ", item.getItemDesc()
		countItemsToPurchase += 1

str += "\n"
str += "Purchase of " + countItemsToPurchase.__repr__() + "item(s) required to fill Sales Orders and Maintain RO point"
print "Purchase of ", countItemsToPurchase, "item(s) required to fill Sales Orders and Maintain RO point"

str += "\n\nExpedite of item(s) on Purchase Orders required to build Sales Orders:"
print "\nExpedite of item(s) on Purchase Orders required to build Sales Orders:"
countItemsToExpedite = 0
for item in items:
	if item.getExpediteQty() > -0.0:
		expediteQty = item.getExpediteQty().__repr__()
		str +="\n  expedite qty " + expediteQty + " of " + item.getItemName() + item.getItemDesc()
		print "  expedite qty ", expediteQty, " of ", item.getItemName(),
		print " ", item.getItemDesc()
		countItemsToExpedite += 1
str += "\nExpedite of " + countItemsToExpedite.__repr__() + "item(s) is required;  These items are on Purchase orders and the quantity listed above must be received prior to build of Sales Orders." 
print "Expedite of ", countItemsToExpedite, "item(s) is required;  These items are on Purchase orders and the quantity listed above must be received prior to build of Sales Orders."

str +=" \n\n Purchase of items(s) required to fill Sales Orders:" 
print "\nPurchase of item(s) required to fill Sales Orders:"
countItemsToPurchase = 0
for item in items:
	if item.getPurchase1() > -0.0:
		purchQty = item.getPurchase1().__repr__()
		print "\n Purchase qty ", purchQty, " of ", item.getItemName(),
		print " ", item.getItemDesc()
		str += "/n Purchase qty " + purchQty + " of " 
		str += item.getItemName() + " " + item.getItemDesc()
		countItemsToPurchase += 1
print "Purchase of ", countItemsToPurchase, "item(s) is required to build open Sales Orders.  "
str += "Purchase of " + countItemsToPurchase.__repr__() + " item(s) is required to build open sales Orders."

print "\nOpen purchase orders exist for the following items:"
str += "\n\nOpen purchase orders exist for the following items:"
countItemsPurchased = 0
for item in items:
	if item.getTotPO() > 0.01:
		purchQty = item.getTotPO().__repr__()
		print "  Purchased qty ", purchQty, " of ", item.getItemName(),
		print " ", item.getItemDesc()
		str += "\n  Purchased qty " + purchQty + " of "
		str += item.getItemName() + " "
		str += item.getItemDesc()
		countItemsPurchased += 1
print "Receipt of", countItemsPurchased, " item(s) is expected; these items have been purchased"
str += "\nReceipt of " + countItemsPurchased.__repr__() + " item(s) is expected"
str += " these items have been purchased."

print "\nThe following items have negative quantities:"
str += "\n\n The following items have negative quantities:"
countItemsToBuild = 0
for item in items:
	if item.getTotOH() <=-.01:
		buildQty = item.getTotOH().__repr__()
		print "  Build qty ", buildQty, " of ", item.getItemName() + " (" + item.getItemDesc() + ")"
		str += "\n  Build qty" + buildQty + " of "
		str += item.getItemName() + " ("
		str += item.getItemDesc() + ")."
		countItemsToBuild += 1
print "QB inventory adjust or logical build could correct negative counts of:", countItemsToBuild, "item(s)."
str += "\nQB inventory adjust or logical build could correct"
str += " negative counts of " + countItemsToBuild.__repr__() + " item(s)\n"		

with open(purchaseguidanceLocation, "w") as text_file:
	text_file.write(str)


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