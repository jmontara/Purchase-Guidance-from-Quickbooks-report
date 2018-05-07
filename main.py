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
import classes.indentedBom

# functions
import functions.readiiqr
import functions.readissbi
import functions.buildItems
import functions.buildItemBoms



transactions, itemStatsFromIiqr = functions.readiiqr.readiiqr()	
		

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

functions.readissbi.readissbi(filename = "issbi.csv", 
							  items = items)
# for item in items:
	# print item
# assert False
	
			 


functions.buildItemBoms.buildItemBoms(trans = transactions, 
									  items = items)
count = 0
for item in items:
	if not item.getBom() == None:
		# print item.getBom()
		count += 1
print "buildItemBoms yields", count, "bills of materials"		
# assert False


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
	
	indentedBom = classes.indentedBom.IndentedBom()
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
					phantomSale = classes.transaction.Transaction(phantomItemName, phantomDesc, 
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
		transactions.append(classes.transaction.Transaction(item, desc, tNum, type, dte,
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

		assert type(item) == classes.item.Item

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
			
	