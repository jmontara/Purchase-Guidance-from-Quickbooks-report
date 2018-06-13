# addItemPhantoms.py

import classes.transaction

def addItemPhantoms(items):			
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
											  "", "",
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
