# file item.py


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
		
		# itemStatsFromPbid
		# from QB purchases by item detail
		self.unitCost = None
		
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
		self.itemStat = None # stores an item's Stat object
		# from addItemPhantoms
		self.phantomSOqty = 0.0
		self.phantomOHqty = 0.0
		self.phantomROpoint = 0.0
		self.upperAssyNames = []
		self.demandShipments = []
	
		self.costPrice = None
		
	def setItemStatsFromPbid(self, costPrice, unitOfMeasure):
		"""
		Add a row of information from pbid.cvs
		
		Inputs:
		costPrice 	- float, cost paid per unit of measure
		unitOfMeasure - float, unit of measure.  
		"""
		try: 
			self.unitCost = float(costPrice)/float(unitOfMeasure)
		except:
			# print "warning:  failed setItemStatsFromPbid(costPrice, unitOfMeasrue)"
			# print "  costPrice =", costPrice
			# print "  unitOfMeasure = ", unitOfMeasure
			# print "  itemName = ", self.getItemName()
			# assert False
			pass
	def getunitcost(self):
		"""
		returns unit cost paid for the most recent purchase
		"""
		return self.unitCost
		
	def getDemandShipments(self):
		return self.demandShipments
	
	def addDemandShipment(self, shipment):
		""" 
		Add shipment indicating sale of this item
		or sale of an upper level assembly item
		"""
		self.demandShipments.append(shipment) 
		
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
		appends to list of Upper Assy Names.
		
		See function addItemPhantoms.
		
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
	
	def whereused(self):
		pass
		
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
		
		Inputs:
		self 	- object, Item object
		roPoint	- str, string representation of QB reorder point
					example:  "0"
					example:  "5"	
		"""			
		roPoint = float(roPoint)
		self.roPoint = roPoint
				
	def setItemStats(self, itemStats):
		self.itemStats = itemStats
		
	def getItemStats(self):
		return self.itemStats
	
	def setStat(self, itemStat):
		self.itemStat = itemStat
	
	def getStat(self):
		"""
		returns itemStat object associated with item
		"""
		return self.itemStat
	
	def getItemName(self):
		return self.itemName
		
	def getItemDesc(self):
		return self.itemDesc
	
	def addXaction(self, transaction):
		"""
		Appends transaction to the item's transaction list.
		
		Sets self.itemCreatingTransaction 
		if transaction has has the following characteristics:
			type = "Build Assembly"
			qty  > 0
			most recent
			
		Sets self.costPrice 
		if transaction has the following charactoristics:
			type = "Bill"
			qty > 0
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
			# print "\n\n\nwarningshould be an item not ever on a purchase order:"
			# print item
			return abs(self.getPhantomSOqty())\
				   - abs(self.getPhantomOHqty())\
				   + abs(self.getPhantomROpoint())\

	def getExpediteQty(self):
		"""
		Returns quantity that must be expedited to fill Open
		Sales orders.

		If the return is a negative value, no
		purchase is required.
		
		If the return is a positive value,
		purchase of the returned quantity is required 
		
		"""
		# return a negative value for non-purchased items.
		if not self.isPurchased():
			return -1.0

		# item created by purchase order transaction
		return abs(self.getPhantomSOqty())\
			   - abs(self.getPhantomOHqty())\
		
	def getTotPO(self):
		"""returns quantity on open PO """
		if self.totPO == None:
			return 0.0
		return self.totPO

	def __str__(self):
		ret = "<Item: " 
		ret += self.itemName  
		ret += " (" + self.itemDesc + ")>\n"
		# ret += self.getIbom().__str__() 
		# ret += self.getXactionsStr()
		ret += self.itemStats.__str__()
		ret += "\n On Hand: " + self.totOH.__str__()
		ret += "    On Sales Order: " + self.totSO.__str__()
		ret += "    On Purchase Order: " + self.totPO.__str__()
		ret += "    RO Point: "   + self.roPoint.__str__()
		ret += "\n Where used: " + self.upperAssyNames.__str__()
		ret += "\n Phantom RO Point: "   + self.phantomROpoint.__str__()
		ret += "\n Phantom OH: " + self.phantomOHqty.__str__()
		ret += "\n Phantom SO: " + self.phantomSOqty.__str__()
		return ret