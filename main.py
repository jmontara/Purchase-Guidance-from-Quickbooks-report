# filename:  purchaseG.py

### Purchase Guidance takes data from reports generated in
### QuickBooks and transforms data into information:

###	Data Input (QuickBooks reports):
###		Inventory Item Quick Report (iiqr.csv)
###		Inventory Status by Item (issbi.csv)
###		Purchases by Item Detail (pbid.csv)
 
### Data Output:
###   	Indented Bills of Materials
###		Sales history
###		Purchase Guidance

# standard library
import csv
import string 
import datetime

# classes 
import transaction

# functions
import readiiqr


transactions, itemStatsFromIiqr = readiiqr.readiiqr()


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
		
		
class Item(object):
	
	def __init__(self, itemName, itemDesc):
		self.itemName = itemName
		self.itemDesc = itemDesc
		
		self.xactions = []
		
		# itemStatsFromIiqr
		# from QB inventory item quick report 
		self.totOH = None
		self.totSO = None
		self.totPO = None
		
		# itemStatsFromIssbi
		# from QB inventory stock status by item
		self.roPoint = None
		
		# Item creating assemblies have a Transaction being of
		# type "Build Assembly" and a quantity being of
		# a positive value.  Transaction stored here  
		# is the most recent such transaction:
		self.itemCreatingTransaction = None 
		
		# Bill of Materials (bom) ...
		self.bom	= ''
		
		# Indented Bill of Materials (iBom) ...
		self.iBom 	= ''
		
		# Item Statistics (itemStats) ...
		self.itemStats = ''

		# from addItemPhantoms
		self.phantomSOqty = 0.0
		self.phantomOHqty = 0.0
		self.phantomROpoint = 0.0
		self.upperAssyNames = []
		
	def getTotSO(self):
		return self.totSO
	
	def getROpoint(self):
		return self.roPoint
			
	def getTotOH(self):
		return self.totOH

	def addPhantomSOqty(self, qty):
		""" 
		Assumes qty comes only from function addItemPhantoms.
			
		Inputs:
		self	- object, Item object
		qty		- float, a quantity required to fill
				       the sales order of a upper level item. 
		"""
		self.phantomSOqty += qty
		
	def addPhantomOHqty(self, qty):
		""" 
		Assumes qty comes only from function addItemPhantoms.
		
		Inputs:
		self	- object, Item object
		qty		- float, a quantity that exists 
					     in an upper level item 
		"""
		self.phantomOHqty += qty
		
	def addPhantomROpoint(self, qty):
		""" 
		Assumes qty comes only from function addItemPhantoms.
		
		Inputs:
		self	- object, Item object
		qty		- float, a quantity that exists 
					     in an upper level item 
		"""
		self.phantomROpoint += qty
		
	def addUpperAssy(self, itemName):
		""" 
		Assumes qty comes only from function addItemPhantoms.
		
		Inputs:
		self	- object, Item object
		itemName- str, an upper level itemName 
		"""
		self.upperAssyNames.append(itemName)	
	
	def getPhantomOHqty(self):
		return self.phantomOHqty
		
	def getPhantomSOqty(self):
		return self.phantomSOqty
		
	def getPhantomROpoint(self):
		return self.phantomROpoint
	
	def getUpperAssyNames(self):
		"""
		returns a list of upper assembly names
		"""
		return self.upperAssyNames
	
	def setItemStatsFromIiqr(self, value, qty):
		"""
		self 	- object, Item object
		value	- str, 	value is a subset of 
								["Tot On Hand"
								 , "Tot On Sales Order"
								 , "Tot On Purchase Order"]
		qty 	- str, examples "0", "5", "-5"
		
		"""		
		qty = float(qty)	
		if value == "Tot On Hand":
			self.totOH = qty
		if value == "Tot On Sales Order":
			self.totSO = qty
		if value == "Tot On Purchase Order":
			self.totPO = qty
			
		# for debug:
		# if value == "Tot On Sales Order"\
					# and self.itemName == "Cable-Power-China":
			# print "value", value, "qty", qty
			# print "self.totOH:", self.totOH
			# print "self.totSO:", self.totSO
			# print "self.totPO:", self.totPO
			# assert False 
			
	def setItemStatsFromIssbi(self, roPoint):
		"""
		self 	- object, Item object
		roPoint	- str, string representation of QB reorder point
					example:  "0"
					example:  "5"
		"""			
		roPoint = float(roPoint)
		self.roPoint = roPoint
		
	def setItemStats(self, itemStats):
		# assert type(itemStats) == ItemStats
		self.itemStats = itemStats
		
	def getItemStats(self):
		return self.itemStats
		
	def getItemName(self):
		return self.itemName
		
	def getItemDesc(self):
		return self.itemDesc
	
	def addXaction(self, transaction):
		"""
		Appends transaction to the item's transaction list.
		Also, sets self.itemCreatingTransaction 
		if transaction has has the following characteristics:
			type = "Build Assembly"
			qty  > 0
			most recent
		"""
		self.xactions.append(transaction)

		# a build assembly that creates this item
		if transaction.getType() == "Build Assembly"\
			and float(transaction.getQty()) > 0.0\
			and self.itemCreatingTransaction == None:
			self.itemCreatingTransaction = transaction
			return
			
		# a more recent build assembly	that creates this item
		if transaction.getType() == "Build Assembly"\
			and float(transaction.getQty()) > 0.0\
			and float(self.itemCreatingTransaction.getTnum())\
				< float(transaction.getTnum()):
			self.itemCreatingTransaction = transaction
			return			

	def getXactions(self):
		return self.xactions
		
	def getXactionsStr(self):
		ret = ""
		for xaction in self.xactions:
			ret += xaction.getShortStr()
		return ret
		
	def getItemCreatingTransaction(self):
		return self.itemCreatingTransaction
		
	def setBom(self, bom):
		# print "self.bom:", self.bom
		# print "bom:", bom
		# assert self.bom == None
		self.bom = bom
		
	def getBom(self):
		return self.bom
		
	def setIndentedBom(self, iBom):
		# assert self.iBom == None
		self.iBom = iBom
	
	def getIbom(self):
		""" 
		returns indented bill of materials
		"""
		return self.iBom

	def hasPhantomSale(self):
		""" 
		Returns True if the item has Phantom Sales.
		
		Used for diagnostic; every item should, after
		creating Transactions of type ""Phantom Sale",
		return True if it is on a indented Bill of Materials.
		
		Some critical items are, however, purchased but 
		not on any Bill of Materials.  These items include
		the processor, pal and others.  These items are held
		in reserve in case of "EOL", "NLA", end of life,
		no longer available, or other supply chain issue.
		"""
		if "Phantom Sale" in\
		self.getItemStats().getOutDict().keys():
			return True
		else:
			return False
			
	def isPurchased(self):
		"""
		Returns True if item's transactions include
		a transaction of type "Bill" or "Credit Card Charge"
		and the item is not an assembly.
		
		"""
		if len(self.getIbom().getItems()) > 1:
			return False
		for transaction in self.getXactions():
			if transaction.getType() == "Bill":
				return True
			if transaction.getType() == "Credit Card Charge":
				return True
		return False

	def onOpenPurchaseOrder(self):
		"""
		Returns the total of quantities on open purchase orders
		for this item.  
		"""
		raise notimplementederror
		
		
	def getPurchase1(self):
		"""
		Returns quantity required to fill Open
		Sales orders.

		If the return is a negative value, no
		purchase is required.
		
		If the return is a positive value,
		purchase of the returned quantity is required 
		
		"""
		# return a negative value for non-purchased items.
		if not self.isPurchased():
			return -1.0
		
		try:
			# item created by purchase order transaction
			return abs(self.getPhantomSOqty())\
				   - abs(self.getPhantomOHqty())\
				   - abs(self.totPO)
		except:
			# item not created by purchase order transaction
			return abs(self.getPhantomSOqty())\
				   - abs(self.getPhantomOHqty())			
		
	def getPurchase2(self):
		"""
		Returns quantity required to fill Open
		Sales Orders and maintain the reorder point.

		If the return is a negative value, no
		purchase is required.
		
		If the return is a positive value,
		purchase of the returned quantity is required 
		
		"""
		# return a negative value for non-purchased items.
		if not self.isPurchased():
			return -1.0
		
		try:
			# item is purchased using a PO
			return abs(self.getPhantomSOqty())\
				   - abs(self.getPhantomOHqty())\
				   + abs(self.getPhantomROpoint())\
				   - abs(self.totPO)
		except: 
			# print "\n\n\nwarningshould be an item not created by a purchase order:"
			# print item
			return abs(self.getPhantomSOqty())\
				   - abs(self.getPhantomOHqty())\
				   + abs(self.getPhantomROpoint())\
	
		
	def getTotPO(self):
		"""returns quantity on open PO """
		if self.totPO == None:
			return 0.0
		return self.totPO

	def __str__(self):
		ret = "\n\n<Item: " 
		ret += self.itemName  
		# ret += " (" + self.itemDesc + ")>\n"
		# ret += self.getIbom().__str__() 
		# ret += self.getXactionsStr()
		ret += self.itemStats.__str__()
		ret += "\nOn Hand: " + self.totOH.__str__()
		ret += "    On Sales Order: " + self.totSO.__str__()
		ret += "    On Purchase Order: " + self.totPO.__str__()
		ret += "    RO Point: "   + self.roPoint.__str__()
		ret += "\nWhere used: " + self.upperAssyNames.__str__()
		ret += "\nPhantom RO Point: "   + self.phantomROpoint.__str__()
		ret += "\nPhantom OH: " + self.phantomOHqty.__str__()
		ret += "\nPhantom SO: " + self.phantomSOqty.__str__()
		return ret
			
def itemsSortKey(item):
	return item.getItemName()
	
def buildItems(transactions = transactions,
			   itemStatsFromIiqr = itemStatsFromIiqr):
	"""
	Reads list of Transaction objects.
	Builds Item objects and returns a list of these,
	which is sorted in order of item name.  
	
	Inputs:
	transactions 		- list, list of Transaction objects
	itemStatsFromIiqr	- list, a list of tuples taking the form			
								(itemName, itemDesc, value, qty)
								 where value is a subset of 
								 ["Tot On Hand"
								 , "Tot On Sales Order"
								 , "Tot On Purchase Order"]
	
	Returns:
	items 			- list, list of Item objects, which is sorted in order of item name
	"""
	# print itemStatsFromIiqr
	# assert False 
	
	items = []

	itemNames =[]
	for t in transactions:
				
		# Create item and populate with first transaction. 
		if not t.getItemName() in itemNames:
			itemNames.append(t.getItemName())
			newItem = Item(t.getItemName(), t.getItemDesc())
			newItem.addXaction(t)
			items.append(newItem)

		# add transaction to existing Item
		else:
			for item in items:
				if item.getItemName() == t.getItemName():
					item.addXaction(t)
					break
					
	for itemStatFromIiqr in itemStatsFromIiqr:

		itemName = itemStatFromIiqr[0]
		itemDesc = itemStatFromIiqr[1]
		value = itemStatFromIiqr[2]
		qty = itemStatFromIiqr[3]
		
		# add itemStat to existing item
		for item in items:		
			if item.getItemName() == itemName\
			   and item.getItemDesc() == itemDesc:

				item.setItemStatsFromIiqr(value, qty)
				# break # leave this for loop
	
	# return a sorted list 
	ret = sorted(items, key=itemsSortKey) # new list
	
	return ret

items = buildItems()
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


def readissbi(filename = "issbi.csv", items = items):
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
	

		

readissbi()
# for item in items:
	# print item
# assert False
	
class Bom(object):
	""" Holds an item and items required to build that item"""
	def __init__(self, asy, desc, tNum = ''):
		"""
		Inputs:
		self	- object, BOM object
		asy		- str, item name
		asyDesc - str, description of item
		tNum 	- str, the transaction number upon which this	
					   BOM is built
		"""
		assert type(asy) == str
		self.asy = asy 
		self.desc = desc
		self.tNum = tNum
		self.items = []
		self.descs = []
		self.qtys = []
		self.levels = [] 
	def getAsyName(self):
		return self.asy
	def getAsyDesc(self):
		return self.desc
	def addItem(self, item, desc, qty, level):
		self.items.append(item)
		self.descs.append(desc)
		self.qtys.append(str(abs(float(qty))))
		self.levels.append(level)
		assert len(self.items) == len(self.descs)
		assert len(self.items) == len(self.qtys)
		assert len(self.items) == len(self.levels)
	def getSorted_tuples(self):
		""" returns a list of tuples sorted by item name
		"""
		bomItem_tuples =[] 
		for row in range(len(self.items)):
			bomItem_tuples.append((
						   self.qtys[row][:6],
						   self.levels[row],
						   self.items[row],
						   self.descs[row][:40]
						   ))
		sortedBomItem_tuples = sorted(bomItem_tuples,
							key=lambda item: item[2]) #sort by item	
		return sortedBomItem_tuples
	def __str__(self):
		ret = "-----------------------------------------------\n"
		# ret += "BOM for: "
		ret += self.asy + " (" + self.desc + ")\n" 
		ret += "\t\t\t\t\t(built from Transaction #" + self.tNum +")\n"
		ret += "Qty \t level item \t description\n"
		ret +="--------------------------------------------------"
		
		# 
		sortedBomItem_tuples = self.getSorted_tuples() 
		# for row in range(len(self.items)):
			# bomItem_tuples.append((
						   # self.qtys[row][:6],
						   # self.levels[row],
						   # self.items[row],
						   # self.descs[row][:40]
						   # ))
		# sortedBomItem_tuples = sorted(bomItem_tuples,
							# key=lambda item: item[2]) #sort by item	
		
		for row in range(len(self.items)):
			ret += "\n"
			ret += sortedBomItem_tuples[row][0] + " \t"
			ret += sortedBomItem_tuples[row][1] + " "
			ret += sortedBomItem_tuples[row][2] + " ("
			ret += sortedBomItem_tuples[row][3] + " ..."
		ret += "\n\n"
		return ret	
	
			 
def buildItemBoms(trans = transactions, items = items):
	""" 
	Reads list of transactions and items.  Updates items with
	a bill of materials.
	
	Inputs:
	trans		- list, list of Transaction objects
	items		- list, list of Item objects

	"""
	for item in items:
		
		itemCreatingTransaction = item.getItemCreatingTransaction()
		# skip item if not an assembly		
		if itemCreatingTransaction == None:
			continue

		
		itemName = itemCreatingTransaction.getItemName()
		transNum = itemCreatingTransaction.getTnum()
		transQty = itemCreatingTransaction.getQty()
		itemName = itemCreatingTransaction.getItemDesc()
		bom = Bom(itemName, itemName, transNum)		
		level = "."
		for t in trans:
			# disregard unless a build
			if not t.getType() == "Build Assembly":
				continue
			# disregard unless lower asy 
			if not float(t.getQty()) < 0:
				continue				
			if t.getTnum() == transNum:
				itemQty = float(t.getQty())/float(transQty)
				itemQty = str(itemQty)[:5]
				bom.addItem(t.getItemName(), t.getItemDesc(), 
							itemQty, level)	
		item.setBom(bom)

buildItemBoms()
count = 0
for item in items:
	if not item.getBom() == None:
		# print item.getBom()
		count += 1
print "buildItemBoms yields", count, "bills of materials"		
# assert False

class IndentedBom(object):
	def __init__(self):
		"""
		Inputs:
		self	-	object, IndentedBom object
		"""
		self.items =[]
		
	def addItem(self,T):
		"""
		Inputs:
		T		- tuple, item's variables
				  
		example: 
		T = (itemQty, itemLevel, itemName, itemDesc)
		"""
		self.items.append(T)
		
	def getItems(self):
		return self.items
	
	def __str__(self):
		ret = "-----------------------------------------------\n"
		ret += "Indented Bill of Materials: \n"
		ret += "qty 	level	item	(description  snipped \n"
		ret +="--------------------------------------------------"
		for item in self.items:
			ret += "\n"
			ret += item[0] + " \t"
			ret += item[1] + " "
			ret += item[2] + " ("
			ret += item[3] + " ..."
		ret += "\n\n"
		return ret			


def buildItemIndentedBom(asyName='BP-2000-MP-4', asyQty='1', 
				   items=items, level=''):
	"""
	Gives a indented lists of BOMs, which display the 
	assembly and every part and quantity of each lower
	level of assembly.

	Inputs:
	asyName	- str, name of assembly 
	asyQty	- str, quantity of assembly for which to construct BOM
	boms	- list, list of all BOM objects
	level 	- str, indicates level of indentation of asyName
	
	Outputs:
	all		- list, list of (qty, level, item, description)
			  including quantity, level, itemName , and itemDesc 
			  of the item and every item in the asy.
			
	"""
	
	def getIbom(asyName='BP-2000-MP-4', asyQty='1', 
				   items=items, level=''):
		"""
		helper function.
		
		iBom	- list, list of (qty, level, item, description)
		  including each quantity, level, item, and description
		  of every item in the asyName. 
		"""		   
		global allInIndentedBom 

		for item in items:
			if item.getItemName() == asyName:
				asyDesc = item.getItemDesc()
				break
		
		allInIndentedBom += [(asyQty, level, asyName, asyDesc)]
		
		# base case of recursive calls
		# return when asyName does not match an item that is an assembly
		asyDesc = None
		for item in items:
			itemCreatingTransaction = item.getItemCreatingTransaction()
			if itemCreatingTransaction == None:
				continue
			itemName = itemCreatingTransaction.getItemName()
			itemDesc = itemCreatingTransaction.getItemDesc()
			if asyName == itemName:
				asyDesc = itemDesc
				thisBomContent = item.getBom().getSorted_tuples()
				break
		if asyDesc == None:
			asyDesc = "item description goes here" 
			L = [(asyQty, level, asyName, asyDesc)]
			return L
			
		else: 
			T =(asyQty, level, asyName, asyDesc)
			level += "."
			# for each item 
			for item in thisBomContent:
				itemQty = str(float(item[0]) * float(asyQty))
				itemName = item[2]
				itemDesc = item[3]
				# recursively call to find the base case		
				L = getIbom(itemName, itemQty, 
									  items, level)
				# if the base case is not found
				if L == None:
					print "error: found no base case in buildItemIndentedBom"
					assert False
				else:
					# print "\nreturn from base case with L:	 ", L
					L = [T] + L
					
				# after reaching the base case and prepending any tuples
			return L

	# print "\n\nentering function:", asyName, asyQty, items, level
	global allInIndentedBom
	allInIndentedBom =[]
	getIbom(asyName, asyQty, items, level)
	# copy of global
	ret = allInIndentedBom[:]
	# print "\n\nret:", ret
	
	indentedBom = IndentedBom()
	for item in items:
		if item.getItemName() == asyName:
			for indentedItem in ret:
				indentedBom.addItem(indentedItem)
			item.setIndentedBom(indentedBom)
	return ret

# asyName='BP-2000-MP-4'	
# print "\nbuildItemIndentedBom(*,*,*,..):"
# buildItemIndentedBom(asyName='BP-2000-MP-4', asyQty='2', 
					# items=items, level='')				   
# for item in items:
	# if item.getItemName() == asyName:
		# print item.getIbom()
		
	
def buildItemIndentedBoms(items = items):
	"""
	builds Indented bills of materials for each item 
	in items list, and updates the item accordingly.
	"""
	for item in items:
		itemName = item.getItemName()
		buildItemIndentedBom(asyName=itemName,
							 asyQty='1',
							 items=items,
							 level ="")

buildItemIndentedBoms()

# for item in items:
	# print item.getIbom()
# assert False

def writeItemFiles(items = items, outDir = 'itemFiles'):		
	"""
	Export item indented boms to csv files 	
	Export item.__str__() to file
	
	Inputs:
	items - list, list of item objects
	outDir - str, directory where output files are written
			 assumes this is directory is already created
	
	Outputs:
	files showing indented boms having the name similar to item.getItemName()
	files showing item.__str__()
	
	"""
 
	allowedFileNameChars ="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
	
	for item in items:
		
		#if char in outFileName is not allowed, 
		# replace it with _
		# outFileName = ''
		outFileName = '.\itemFiles\\'
		# outFileName = '.\' + outDir + '\\'
		for char in item.getItemName():
			if char in allowedFileNameChars:
				outFileName += char
			else:
				outFileName += '_'
		# outFileName += '.csv'
		outFileName = outFileName + '-ibom.csv'
		
		with open(outFileName, 'wb') as f:
			csv_writer = csv.writer(f)
			# header row
			qty = "qty"
			level = "level"
			itemName = "itemName"
			itemDesc = "itemDesc"
			csv_writer.writerow([qty, level, itemName, itemDesc]) 
			for indentedItem in item.getIbom().getItems():
				qty = indentedItem[0]
				level = indentedItem[1]
				itemName = indentedItem[2]
				itemDesc = indentedItem[3]				
				csv_writer.writerow([qty, level, itemName, itemDesc]) 
		# assert False
		#if char in outFileName is not allowed, 
		# replace it with _
		# outFileName = ''
		outFileName = '.\itemFiles\\'
		# outFileName = '.\' + outDir + '\\'
		for char in item.getItemName():
			if char in allowedFileNameChars:
				outFileName += char
			else:
				outFileName += '_'
		# outFileName += '.csv'
		outFileName = outFileName + '-summary.txt'
		
		with open(outFileName, "w") as text_file:
			text_file.write(item.__str__())
		# assert False

# writeItemFiles()
# assert False



def setTransactionSaleDate(transactions = transactions):
	"""
	Updates Transaction objects that are of type "Invoice" 
	with the date of the sales order associated with the invoice.
	
	Returns a list of these updated Transaction objects.
	
	Inputs:
	transactions	- list, list of Transaction objects
	
	Outputs:
	invoiceTransactions = list, list of updated Transaction objects
	"""
		
	salesOrders = {}
	ret = []

	for transaction in transactions:
		if transaction.getType() == "Sales Order":
			salesOrders[transaction.getNum()] = transaction.getDate()

	for transaction in transactions:
		if transaction.getType() == "Invoice":
			try:
				transaction.setInvoiceSaleDate(salesOrders[transaction.getSoNum()])
				ret.append(transaction)
			except:
				print "\nwarning, this invoice transaction has no sales order number in available data"
				print "warning, substituting invoice date as an approximation for sale date"
				print "warning, Doing this puts some sales into a different calendar year. "
				transaction.setInvoiceSaleDate(transaction.getDate())
				print transaction
				ret.append(transaction)
				
	return ret
	
invoiceTransactions = setTransactionSaleDate()
# limit = 500
# for t in invoiceTransactions:
	# print "invoice transaction with sale date:", t
	# limit -= 1
	# if limit < 0:
		# break
# assert False
		
def addItemPhantoms(items = items):			
	"""
	Looks at every item's transactions and, if a transaction 
	is of type "Invoice", adds a Transaction of type 
	"Phantom Sale" to each item in the item's indented bill of materials.	
	
	Looks at every item's self.totSO and, if not None and non-zero, adds
	a relevant quantity to the phantomSOqty of each item 
	in the item's indented bill of materials.	
	
	Looks at every item's self.totOH and, if not None and non-zero, adds
	a relevant quantity to the phantomOHqty of each item 
	in the item's indented bill of materials.
	
	Looks at every item's self.roPoint and, if not None and non-zero, adds
	a relevant quantity to the phantomROpoint of each item 
	in the item's indented bill of materials. 
		
	Outputs:
	phantomSales - list, list of Transactions of type "Phantom Sale"
	"""
	
	phantomSales = []
	
	#Item name to object lookup dictionary
	itemName2Object = {}
	for item in items:
		itemName2Object[item.getItemName()] = item
	

	for item in items:
	
		# item's transactions 
		itemTransactions = item.getXactions()
		for itemTransaction in itemTransactions:
			if itemTransaction.getType() == "Invoice":
			

				itemQty = itemTransaction.getQty()
				itemTnum = itemTransaction.getTnum()
				itemType = "Phantom Sale"
				itemDate = itemTransaction.getDate()
				itemNum = itemTransaction.getNum()
				itemQty = itemTransaction.getQty()
				itemSO	= itemTransaction.getSoNum()
				itemInvoiceSaleDate = itemTransaction.getInvoiceSaleDate()	
				
				# Items in iBom include the item and, if the item is an
				# assembly, all items required to build the item.
				itemsInIbom = item.getIbom().getItems()
				for itemInIbom in itemsInIbom:
					
					phantomQty = str(float(itemQty) * float(itemInIbom[0]))[:4]
					phantomItemName = itemInIbom[2]
					phantomDesc = itemInIbom[3]
					phantomSale = transaction.Transaction(phantomItemName, phantomDesc, 
											  itemTnum, itemType, itemDate,
											  itemNum,	phantomQty, itemSO, 
											  itemInvoiceSaleDate)	
						
					itemName2Object[phantomItemName].addXaction(phantomSale)
					phantomSales.append(phantomSale)
					
					
	# item's totSO
	for item in items:				
		
		# skip item if it has no open Sales Orders
		if item.getTotSO() == None:
			continue 
		epsilon = 0.01
		if 0.0 + epsilon > abs(float(item.getTotSO())):
			continue
		
		itemsInIbom = item.getIbom().getItems()		
		for itemInIbom in itemsInIbom:
			phantomItemName = itemInIbom[2]
			phantomSOqty = item.getTotSO() * float(itemInIbom[0])
			itemName2Object[phantomItemName].addPhantomSOqty(phantomSOqty)
		
			# print "\n", item.getItemName(),
			# print item.getTotSO()
			# print phantomItemName,
			# print itemInIbom[0]
			# print "mult:", item.getTotSO() * float(itemInIbom[0])

	# item's totOH
	for item in items:				
		
		# skip item if it has no OH inventory
		if item.getTotOH() == None:
			continue 
		epsilon = 0.01
		if 0.0 + epsilon > abs(float(item.getTotOH())):
			continue
			
		# otherwise, add value of the top assembly
		# to each item in the top assembly's indented bill of materials					
		itemsInIbom = item.getIbom().getItems()		
		for itemInIbom in itemsInIbom:
			phantomItemName = itemInIbom[2]
			phantomOHqty = item.getTotOH() * float(itemInIbom[0])
			itemName2Object[phantomItemName].addPhantomOHqty(phantomOHqty)
	
	# item's roPoint
	for item in items:				
		
		# skip item if it has no or zero RO point
		if item.getROpoint() == None:
			continue 
		epsilon = 0.01
		if 0.0 + epsilon > abs(float(item.getROpoint())):
			continue
		
		# otherwise, add value of the top assembly
		# to each item in the top assembly's indented bill of materials
		itemsInIbom = item.getIbom().getItems()		
		for itemInIbom in itemsInIbom:
			phantomItemName = itemInIbom[2]
			phantomROpoint = item.getROpoint() * float(itemInIbom[0])
			itemName2Object[phantomItemName].addPhantomROpoint(phantomROpoint)
	
	# item's upper level assy's
	for item in items:
		
		# Skip item if it's indented bill of materials contains
		# only one entry.
		if len(item.getIbom().getItems()) < 2:
			continue
			
		# otherwise, add name of the top assembly
		# to each item in the top assembly's indented bill of materials.
		itemsInIbom = item.getIbom().getItems()
		for itemInIbom in itemsInIbom:
			phantomItemName = itemInIbom[2]
			itemName2Object[phantomItemName].addUpperAssy(item.getItemName())
			
			# print "\n", phantomItemName
			# print item.getItemName()
		# print item.getIbom()
		# print item.getUpperAssyNames()
		# print itemName2Object['BP-Elastic-M-1/4-Balloons'].getUpperAssyNames()
		# assert False
	
				
	return phantomSales	

phantomSales = addItemPhantoms()
# print "itemHistories:", itemHistories

print "phantomSales() yields", len(phantomSales), "transactions"
# limit = 1000
# for transaction in phantomSales:
	# print "phantomSales", transaction
	# limit -=1
	# if limit < 0:
		# break
# assert False
	

def total(transactions, dateStart, dateEnd):
	"""
	returns the sum of quantities in transactions that 
	occur on dateStart, on dateEnd, and between 
	dateStart and dateEnd.

	Inputs:
	transactions	- list, list of transaction objects
	dateStart		- datetime.date object
	dateEnd			- datetime.date object
	
	Outputs:
	ret				- str, string representation of total
	
	"""
	ret = 0.0
	for transaction in transactions:
		# skip if not between start and end date
		if not dateStart <= transaction.getDate() <= dateEnd:
			continue
		try:
			ret += float(transaction.getQty())
		except:
			# skip transactions that have "" in the qty column
			if not transaction.getQty() == "":
				print transaction
				print "\n\nError, garbage in transaction.getQty()"
				print "converting transaction qty to float"
				assert False			
	return str(ret)

def testTotal():
	""" 
	creates transactions
	sends to the function total
	returns value of total
	"""
	transactions = []

	for day in range(18):
		if day < 10:
			continue
		item = "item" + str(day)
		desc = "desc" + str(day)
		tNum = "tnum" + str(day)
		type = "type" + str(day)
		dte =  datetime.date.fromordinal(day+1)
		num = "num" + str(day)
		qty = str(1)
		soNum = "soNum" + str(day)
		transactions.append(Transaction(item, desc, tNum, type, dte,
							num, qty, soNum, soDte=None))
	
	dayStart = datetime.date.fromordinal(10)
	dayEnd = datetime.date.fromordinal(20)
							
	return total(transactions, dayStart, dayEnd)
	
# print testTotal()
# assert False
	
	
def getStatFunctionsString(statFunction, dateStart, dateEnd, desc, slice="year"):
	""" 
	returns a list of tuples used within ItemStat object
	
	Inputs:
	statFunction 	- function name, statFunction
	dateStart 		- object, datetime.date 
	dateEnd			- object, dateTime.date
	desc			- str, description
	slice			= str, description of the slices of dates for each tuple in list to be output	
	Outputs:
	L				= list of tuples having the form used within statFunctions
					  
					  if slice == "year" and statFunction == total	
					  example [(total, dateStart1, dateEnd1, "Y0", "total"),
							   (total, dateStart2, dateEnd2, "Y1", "total"),
							   ...
							   (total, dateStart3, dateEnd3, "Yn", "total")]
							   
					  if slice == "month" and statFunction == total	
					  example [(total, dateStart1, dateEnd1, "Y0M1", "total"),
							   (total, dateStart2, dateEnd2, "Y0M2", "total"),
							   ...
							   (total, dateStart12, dateEnd12, "Y0M12", "total"),]

   				      if slice == "year" and and statFunction == maxMonth
					  example [(max, dateStart1, dateEnd1, "MMY0", "max month total"),
							   (max, dateStart2, dateEnd2, "MMY1", "max month total"),
							   ...
							   (max, dateStartn, dateEndn, "MMYn", desc), "max month total"]
							   
   				      if slice == "year" and and statFunction == max30day
					  example [(max, dateStart1, dateEnd1, "M30Y0", "max 30 day total"),
							   (max, dateStart2, dateEnd2, "M30Y1", "max 30 day total"),
							   ...
							   (max, dateStartn, dateEndn, "M30Yn", desc), "max 30 day total"]

   				      if slice == "year" and and statFunction == max10day
					  example [(max, dateStart1, dateEnd1, "M10Y0", "max 10 day total"),
							   (max, dateStart2, dateEnd2, "M10Y1", "max 10 day total"),
							   ...
							   (max, dateStartn, dateEndn, "M10Yn", desc), "max 10 day total"]
							   
	"""
	L = []
	limit = 12 # columns limited to print nicely
	
	if slice == "year" and statFunction == total:
		yearsStart = dateStart.__getattribute__("year")
		yearsEnd = dateEnd.__getattribute__("year") 
		year = yearsStart
		while year <= yearsEnd:
			dateStartSlice = datetime.date(year, 1, 1)
			year += 1
			
			dateEndSlicePlus1day = datetime.date(year, 1, 1)
			dateEndSliceOrdinal = dateEndSlicePlus1day.toordinal() - 1
			dateEndSlice = datetime.date.fromordinal(dateEndSliceOrdinal)
			
			descShort = "Y" + str(year - yearsStart -1)

			T = (statFunction, 
				 dateStartSlice,
				 dateEndSlice,
				 descShort,
				 desc)
			L += [T]
			
		return L[:limit]		
	
	if slice == "month" and statFunction == total:
		yearsStart = dateStart.__getattribute__("year")
		yearsEnd = dateEnd.__getattribute__("year") 
		year = yearsStart - 1
		while year <= yearsEnd:
			year += 1
			month = 0
			while month < 12:
				month += 1
				dateStartSlice = datetime.date(year, month, 1)
				try: 
					dateEndSlicePlus1day = datetime.date(year, month + 1, 1)
				except: # the 13th month
					dateEndSlicePlus1day = datetime.date(year+1, 1, 1)
				dateEndSliceOrdinal = dateEndSlicePlus1day.toordinal() - 1
				dateEndSlice = datetime.date.fromordinal(dateEndSliceOrdinal)			
			
				descShort = "Y" + str(year - yearsStart)	
				descShort += "M" + str(month)
			
				T = (statFunction, 
					 dateStartSlice,
					 dateEndSlice,
					 descShort,
					 desc)
				L += [T]
				
		return L[:limit]

	if slice == "year" and statFunction == maxmonth:
		yearsStart = dateStart.__getattribute__("year")
		yearsEnd = dateEnd.__getattribute__("year") 
		year = yearsStart - 1
		while year < yearsEnd:
			year += 1
			dateStartSlice = datetime.date(year, 1, 1)
			dateEndSlicePlus1day = datetime.date(year +1, 1, 1)
			dateEndSliceOrdinal = dateEndSlicePlus1day.toordinal() - 1
			dateEndSlice = datetime.date.fromordinal(dateEndSliceOrdinal)			

			descShort = "MM"		
			descShort += "Y" + str(year - yearsStart)	
		
			T = (statFunction, 
				 dateStartSlice,
				 dateEndSlice,
				 descShort,
				 desc)
			L += [T]
				
		return L[:limit]
		
	if slice == "year" and statFunction == max30day:
		yearsStart = dateStart.__getattribute__("year")
		yearsEnd = dateEnd.__getattribute__("year") 
		year = yearsStart - 1
		while year < yearsEnd:
			year += 1
			dateStartSlice = datetime.date(year, 1, 1)
			dateEndSlicePlus1day = datetime.date(year +1, 1, 1)
			dateEndSliceOrdinal = dateEndSlicePlus1day.toordinal() - 1
			dateEndSlice = datetime.date.fromordinal(dateEndSliceOrdinal)			

			descShort = "M30"		
			descShort += "Y" + str(year - yearsStart)	
		
			T = (statFunction, 
				 dateStartSlice,
				 dateEndSlice,
				 descShort,
				 desc)
			L += [T]
				
		return L[:limit]

	if slice == "year" and statFunction == max10day:
		yearsStart = dateStart.__getattribute__("year")
		yearsEnd = dateEnd.__getattribute__("year") 
		year = yearsStart - 1
		while year < yearsEnd:
			year += 1
			dateStartSlice = datetime.date(year, 1, 1)
			dateEndSlicePlus1day = datetime.date(year +1, 1, 1)
			dateEndSliceOrdinal = dateEndSlicePlus1day.toordinal() - 1
			dateEndSlice = datetime.date.fromordinal(dateEndSliceOrdinal)			

			descShort = "M10"		
			descShort += "Y" + str(year - yearsStart)	
		
			T = (statFunction, 
				 dateStartSlice,
				 dateEndSlice,
				 descShort,
				 desc)
			L += [T]
				
		return L[:limit]
		

def maxmonth(transactions, dateStart, dateEnd):
	""" 
	assumes dateStart - dateEnd is a period of one year.
	returns the maximum of totals of quantities that fall within a one month period
	"""
	maxMonthTotal = 0.0

	thisYear = dateStart.__getattribute__('year')
	for month in range(1,13,1):
		monthTotal = 0.0
		periodStart = datetime.date(thisYear,month,1)
		try:
			periodEndPlus1Ordinal = datetime.date(thisYear, month +1, 1 ).toordinal()
		except:
			periodEndPlus1Ordinal = datetime.date(thisYear+1, 1,1).toordinal()
		periodEndOrdinal = periodEndPlus1Ordinal -1
		periodEnd = datetime.date.fromordinal(periodEndOrdinal)
		for transaction in transactions:
			if periodStart <= transaction.getDate() <= periodEnd:
				monthTotal += float(transaction.getQty())
				if abs(monthTotal) > abs(maxMonthTotal):
					maxMonthTotal = monthTotal
	
	return str(maxMonthTotal)[:6]

def max30day(transactions, dateStart, dateEnd):
	""" 
	assumes dateStart - dateEnd is a period of one year
	returns the maximum of totals of quantities that fall within a 30 day period
	
	"""
	maxPeriodTotal = 0.0
	
	periodDays = 30

	thisYear = dateStart.__getattribute__('year')
	periodStartOrdinal = datetime.date(thisYear, 1, 1).toordinal()
	periodEndOrdinal = periodStartOrdinal + periodDays
	
	while datetime.date.fromordinal(periodEndOrdinal) <= dateEnd:
		periodTotal = 0.0
		for transaction in transactions:
			if periodStartOrdinal <= transaction.getDate().toordinal() <= periodEndOrdinal:
				periodTotal += float(transaction.getQty())
		if abs(periodTotal) > abs(maxPeriodTotal):
			maxPeriodTotal = periodTotal
		
		periodStartOrdinal += 1
		periodEndOrdinal += 1

	# print "\n\n"	
	# print "dateStart.toordinal()", dateStart.toordinal(), "dateStart:", dateStart.__str__()
	# print "dateEnd.toordinal()", dateEnd.toordinal(), "dateEnd:", dateEnd.__str__()
	# print "periodStartOrdinal", periodStartOrdinal, "periodStart:", datetime.date.fromordinal(periodStartOrdinal).__str__()
	# print "periodEndOrdinal", periodEndOrdinal, "periodEnd:", datetime.date.fromordinal(periodEndOrdinal).__str__()
	# assert False
	
	return str(maxPeriodTotal)[:6]	


def max10day(transactions, dateStart, dateEnd):
	""" 
	assumes dateStart - dateEnd is a period of one year
	returns the maximum of totals of quantities that fall within a 10 day period
	
	"""
	maxPeriodTotal = 0.0
	
	periodDays = 10

	thisYear = dateStart.__getattribute__('year')
	periodStartOrdinal = datetime.date(thisYear, 1, 1).toordinal()
	periodEndOrdinal = periodStartOrdinal + periodDays
	
	while datetime.date.fromordinal(periodEndOrdinal) <= dateEnd:
		periodTotal = 0.0
		for transaction in transactions:
			if periodStartOrdinal <= transaction.getDate().toordinal() <= periodEndOrdinal:
				periodTotal += float(transaction.getQty())
		if abs(periodTotal) > abs(maxPeriodTotal):
			maxPeriodTotal = periodTotal
		
		periodStartOrdinal += 1
		periodEndOrdinal += 1

	# print "\n\n"	
	# print "dateStart.toordinal()", dateStart.toordinal(), "dateStart:", dateStart.__str__()
	# print "dateEnd.toordinal()", dateEnd.toordinal(), "dateEnd:", dateEnd.__str__()
	# print "periodStartOrdinal", periodStartOrdinal, "periodStart:", datetime.date.fromordinal(periodStartOrdinal).__str__()
	# print "periodEndOrdinal", periodEndOrdinal, "periodEnd:", datetime.date.fromordinal(periodEndOrdinal).__str__()
	# assert False
	
	return str(maxPeriodTotal)[:6]	
	
		
class ItemStats(object):
	def __init__(self, item, transactions):

		assert type(item) == Item

		# Make this object callable from the Item object & self
		item.setItemStats(self) 
		self.item = item
		
		# Make inDict with key being Transaction.getType()
		#    value being the transaction.
		#    example: {"pseudoSale": [transaction1, transaction2, ...] ;
		#			   "Build Assembly": [transaction6, transaction4, ...];
		#			   "Invoice": [transaction20, transaction30, ...];
		#			   "Sales Order": [transaction20, transaction30, ...];
		#			   "Bill": [transaction20, transaction30, ...]}				
		inDict = {}
		for xaction in item.getXactions():
			if xaction.getType() in inDict.keys():
				existingValue = inDict[xaction.getType()]
				inDict[xaction.getType()] = existingValue + [xaction]
			else:
				inDict[xaction.getType()] = [xaction]

		# Determine start and end dates in transactions.
		# Using proleptic Gregorian ordinal of the date, 
		# where January 1 of year 1 has ordinal 1
		transactionsStartDay = 836499 # many days into the future
		transactionsEndDay = 1		  # January 1 of year 1
		for transaction in transactions:
			if transaction.getDate().toordinal() < transactionsStartDay:
				transactionsStartDay\
				   = transaction.getDate().toordinal()
			if transaction.getDate().toordinal() > transactionsEndDay:
				transactionsEndDay\
				   = transaction.getDate().toordinal()
		dateStart = datetime.date.fromordinal(transactionsStartDay)
		dateEnd = datetime.date.fromordinal(transactionsEndDay)
		
		
		# Make outDict with key being Transaction.getType()
		#    and value being paired lists statDesc and statValue.
		#    example:  {"PseudoSale": ["total"], [105]}
		# Parse inDict for stats and load these into outDict.
		#    example:  {"PseudoSale": ["total", "2017"], [105, 33]}
		#    example:  {"PseudoSale": ["total", "2017", "2016"], [105, 33, 28]}
		# Continue to parse and load for each key in inDict.		
		#    example:  {"PseudoSale": ["total"], [105]}
		#    example:  {"PseudoSale": ["total", "2017"], [105, 33]}
		#    example:  {"PseudoSale": ["total", "2017", "2016"], [105, 33, 28]}
		#    example:  {"Build Assembly": ["total", "2017"], [105, 33]}
		#    example:  {"Build Assembly": ["total", "2017"], [105, 33]}
		#    example:  {"Build Assembly": ["total", "2017", "2016"], [105, 33, 28]}
		self.outDict = {}
		
		
		# self.statFunctions contain the following:
		#  statFunction - function located in __main__
		#  dateStart	- function parameter, object, datetime.date  
		#  dateEnd		- function parameter, object, datetime.date
		#  descShort	- str, description of statFunction
		#  desc			- str, description of statFunction
		
		self.statFunctions = []
		self.statFunctions +=\
		 [(total, dateStart, dateEnd, "total", "total for all days")]
		self.statFunctions +=\
		 getStatFunctionsString(total, dateStart, dateEnd, "total for year", "year" )
		# self.statFunctions +=\
		 # getStatFunctionsString(total, dateStart, dateEnd, "total for month", "month" )
		# self.statFunctions +=\
		 # getStatFunctionsString(maxmonth, dateStart, dateEnd, "Maximum total for month in year", "year" )
		self.statFunctions +=\
		 getStatFunctionsString(max30day, dateStart, dateEnd, "Maximum total for 30 days in year", "year" )
		self.statFunctions +=\
		 getStatFunctionsString(max10day, dateStart, dateEnd, "Maximum total for 10 days in year", "year" )
		

		
		for key in inDict.keys():
			xactions = inDict[key]
			self.outDict[key] = []
			if key == None:
				print "key:", key 
				print "error key should not be none"
				assert False
			for statFunctionRow in self.statFunctions:
				
				statFunction = statFunctionRow[0]
				dateStart = statFunctionRow[1]
				dateEnd = statFunctionRow[2]
				self.outDict[key] = self.outDict[key]\
									+ [statFunction(xactions,
													dateStart,
													dateEnd)] 
				
	def getOutDict(self):
		return self.outDict
		
	# def getOutDictPhantomSalesStr(self):
		# ret = ""
		# for key in self.outDict.keys()
			# if key == "Phantom Sales":
				# print key, self.outDict[key]
	
		
	def __str__(self):
		""" example output
		#    Summary stats for item V0052 (Some description)
		#    Columns Key:
		#    Column Name, column description (statFunction)
		#    
		#	 buildType 		Total 	2017	2016	...
		#    pseudoSale 	105		33		28		...
		#    build assembly	105		33		28		...	
		#	 ...	  		... 	...		...		...					
		"""
		ret = "==================================================\n"
		ret += "Summary stats for " + self.item.getItemName() +"\n"
		ret += "                 (" + self.item.getItemDesc() + ")\n"
		ret += "Columns Key:\n"
		for statFunctionRow in self.statFunctions:
			ret += " " + statFunctionRow[3] 
			ret += " - " + statFunctionRow[4] 
			ret += " (" + statFunctionRow[1].__str__()
			ret += " through " + statFunctionRow[2].__str__()
			ret += ")\n"
		ret += "-------------------------------------------------\n"
		# first row
		ret += "              "
		for statFunctionRow in self.statFunctions:
			padLength = 7 - len(statFunctionRow[3])
			pad =""
			for padCount in range(padLength):
				pad += " "
			ret += statFunctionRow[3] + pad
		ret += "\n"	
		# other rows 
		for key in sorted(self.outDict.keys()):
			# first column truncate and pad to fit, ie "Build Assembly" becomes "Build Assemb  "
			padLength = 14 - len(key[:12])
			pad = ""
			for padCount in range(padLength):
				pad += " "
			ret += key[:12] + pad

			# other columns
			for stat in self.outDict[key]:
				# other columns are padded to fit.  ie "0.0" becomes "0.0    "
				padLength = 7 - len(stat)
				pad = ""
				for padCount in range(padLength):
					pad += " "
				ret += stat + pad 
			ret += "\n"	
		return ret	
				
				
			
# itemName = 'BP-2000-MP-6-220V'		
# for item in items:
	# if item.getItemName() == itemName:
		# itemStats = ItemStats(item, transactions)
		# break
# for item in items:
	# if item.getItemName() == itemName:
		# print item

def setItemsStats(items = items):
	print "\nsetting items stats"
	for item in items:
		itemStats = ItemStats(item, transactions)
		
setItemsStats()
		
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


writeItemFiles()		
		
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
			
	