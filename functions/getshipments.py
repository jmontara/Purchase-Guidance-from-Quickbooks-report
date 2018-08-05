#  filename:  getshipments.py

import datetime
import cycletimes
		 
def getshipments(items):
	"""
	returns dictionary of shipments 
	
	Inputs:
	items 	- list of item objects
	
	Outputs:
	buyShipmentsByItem
			- list of dictionaries
				example: {item: [shipment1, shipment2, shipment3]}
	"""	
	print "\n\nentering getshipments()"
	
	buyShipmentsByItem = {}
	# startTransactionTypes 
			# - list, list of strings describing start transaction types.
	# endTransactionTypes 
			# - list, list of strings describing end transaction types.
	buyStartTransactionTypes = ['Purchase Order', 'Credit Card Charge']
	buyEndTransactionTypes = ['Bill', 'Item Receipt']

	for item in items:
		startTransactions = []
		endTransactions = []
		buys = []
		# print "item:", item
		# print "item.getItemName():", item.getItemName()
		# assert False
		for transaction in item.getXactions():
			type = transaction.getType()
			qty = transaction.getQty()
			if type in buyStartTransactionTypes\
				and qty == '0':
				startTransactions.append(transaction)
				# print transaction, "\ntype,qty:", type, qty, "\n"
				# assert False
			if type in buyStartTransactionTypes\
				and not qty == '0'\
				and type == 'Credit Card Charge':
				startTransactions.append(transaction)
				# print transaction, "\ntype,qty:", type, qty, "\n"
				# assert False
			elif type in buyEndTransactionTypes\
				and not(qty == '0'):
				endTransactions.append(transaction)
				# print transaction, "\ntype,qty:", type, qty, "\n"
				# assert False		
				
		# look at most recent start transaction.
		def getDate(transaction):
			return transaction.getDate()
			
		sortedStartTransactions = sorted(startTransactions, 
									   key=getDate,
									   reverse=True)
		sortedEndTransactions = sorted(endTransactions, 
									   key=getDate,
									   reverse=True)
									   
		for buy in sortedStartTransactions:

			# Append to buys where there is no start + end transaction in data
			if buy.getType() == 'Credit Card Charge':
				startTransaction = buy
				endTransaction = buy
				buys.append(cycletimes.Buy(startTransaction,endTransaction))
				# print "after appending Credit Card Charge, buys:", buys
				# print "item.getItemName():", item.getItemName()
				# for buy in buys:
					# print "buy:", buy
				# assert False

			# Append to buys where there is start + end transaction in data
			elif buy.getQty() == '0':
			
				buyDte = buy.getDate()
				
				# get the most recent end transaction
				leadTime = datetime.timedelta(999)
				for ship in sortedEndTransactions:
					shipDte = ship.getDate()
					thisLeadTime = shipDte - buyDte
					
					zeroLeadTime = shipDte - shipDte
					if zeroLeadTime <= thisLeadTime < leadTime:
						leadTime = thisLeadTime
						startTransaction = buy
						endTransaction = ship

				# scrub transaction(s) entered with error:
				# <Shipment,Buy:  "Logic Hydraulic Controls Inc" --> "Manufacturing Warehouse"
					 # Lead time (days): 90
					 # <xaction:  Pump, Air, 230V, Air Compressor, 230V, 27745, Purchase Order, 2015-01-20, 2043, 0, , Logic Hydraulic Controls Inc, Air Compressor, 230V>
					 # <xaction:  Pump, Air, 230V, Air Compressor, 230V, 28541, Bill, 2015-04-20, 60621, 7, , Logic Hydraulic Controls Inc, Air Compressor, 230V>>
				if leadTime.days >89:
					continue
						
				buys.append(cycletimes.Buy(startTransaction,endTransaction))
		
		# only make entries if there are buys
		itemName = item.getItemName()
		if len(buys)>0:
			buyShipmentsByItem[itemName] = buys
		
	return buyShipmentsByItem

def getshipmentscustomer(items):
	"""
	returns dictionary of shipments of items to customers
	The dictionary is populated only with shipments that are
	directly shipped to customers.  
	
	Inputs:
	items - list of item objects
	
	Outputs:
	ret 		itemshipments
				example: {item: [shipment1, shipment2, shipment3]}
	"""	
	print "entering getshipmentscustomer(items)"
	itemshipments = {}
	sellStartTransactionTypes = ['Sales Order']
	sellEndTransactionTypes = ['Invoice']

	for item in items:
		startTransactions = []
		endTransactions = []
		sells = []
		# print "item:", item
		# print "item.getItemName():", item.getItemName()
		# assert False
		for transaction in item.getXactions():
			type = transaction.getType()
			qty = transaction.getQty()
			if type in sellStartTransactionTypes\
				and qty == '0':
				startTransactions.append(transaction)
				# print transaction, "\ntype,qty:", type, qty, "\n"
				# assert False
			elif type in sellEndTransactionTypes\
				and not(qty == '0'):
				endTransactions.append(transaction)
				# print transaction, "\ntype,qty:", type, qty, "\n"
				# assert False		
				
		# look at most recent start transaction.
		def getDate(transaction):
			return transaction.getDate()
			
		sortedStartTransactions = sorted(startTransactions, 
									   key=getDate,
									   reverse=True)
		sortedEndTransactions = sorted(endTransactions, 
									   key=getDate,
									   reverse=True)
									   
		for sale in sortedStartTransactions:
	
			saleDte = sale.getDate()
			saleCustomer = sale.getName()
			
			# get the most recent end transaction for the customer
			# 
			leadTime = datetime.timedelta(9999)
			for ship in sortedEndTransactions:
				
				shipCustomer = ship.getName()
				shipDte = ship.getDate()
				thisLeadTime = shipDte - saleDte				
				zeroLeadTime = shipDte - shipDte
				
				# print "sale.getName():", sale.getName()
				# print "ship.getName():", ship.getName()
				# assert False

				try:
					assert shipCustomer == saleCustomer
					assert zeroLeadTime <= thisLeadTime
					assert thisLeadTime < leadTime
					leadTime = thisLeadTime
					startTransaction = sale
					endTransaction = ship					
					
				except:
					pass
					
					
			demandShipment = cycletimes.Sell(startTransaction,endTransaction)
			sells.append(demandShipment)
			# print "\nSell object (demand shipment precursor): "
			# print cycletimes.Sell(startTransaction,endTransaction)
			
			try:
				# show an errant shipment
				assert demandShipment.getDestination() == "Bristol-Myers Squibb - Basso"
				print "demandShipment.getDestination()", demandShipment.getDestination()
				print "demandShipment:", demandShipment
				print "\n"
			except:
				pass

			
		# only make entries if there are sells
		itemName = item.getItemName()
		if len(sells)>0:
			itemshipments[itemName] = sells
			
	# assert False
	return itemshipments
	
def addDemandShipments(itemShipments, items, toTest = True):
	"""
 	Looks at shipments for each item in itemshipments.   
	Adds a representative demand shipment to the item and to 
	each item in the item's indented bill of materials. 
		
	Inputs:
	itemshipments 	- dict,
					example, itemshipments[itemName] = list of sell shipments
	items 			- list of item objects
	
	Outputs:
	itemDemandShipments
				example: {item: [shipment1, shipment2, shipment3]}
	"""
	print "\n\nentering addDemandShipments()"
	
	itemDemandShipments  = {}	
	
	#Item name to object lookup dictionary
	itemName2Object = {}
	for item in items:
		itemName2Object[item.getItemName()] = item
	
	for itemSoldName  in itemShipments.keys():
		# print "\nitemSoldName:", itemSoldName
		itemSold = itemName2Object[itemSoldName]
		
		itemsInItemSoldIbom = itemSold.getIbom().getItems()
		# print "\nitemsInItemSoldIbom:", itemsInItemSoldIbom
		# assert False
		
		for itemSoldShipment in itemShipments[itemSoldName]:
			# print "\nitemSoldShipment:", itemSoldShipment
			# assert False
			
			itemSoldQty = itemSoldShipment.getQty()

		
			for itemInItemSoldIbom in itemsInItemSoldIbom:
				
				# print "itemInItemSoldIbom:", itemInItemSoldIbom
				# assert False
				
				demandQty = str(float(itemSoldQty) * float(itemInItemSoldIbom[0]))[:4]
				demandItemName = itemInItemSoldIbom[2]
				demandItemDesc = itemInItemSoldIbom[3]

				# generate a new shipment taking dates from the itemSoldShipment
				# and quantities from above
				
				demandShipment = itemSoldShipment.getModifiedClone(demandQty, demandItemName, 
												demandItemDesc)
					
				itemName2Object[demandItemName].addDemandShipment(demandShipment)
				# show an errant shipment
				# try:
					# assert demandShipment.getDestination() == "Bristol-Myers Squibb - Basso"
					# print "demandShipment.getDestination()", demandShipment.getDestination()
					# print "demandShipment:", demandShipment
					# print "\n"
				# except:
					# pass
				# assert False
				
		# if toTest:
			# print "toTest:", toTest
			# break
	# assert False
	for key in itemName2Object.keys():
		item = itemName2Object[key]
		# populate with all shipments, including those of parts not purchased
		itemDemandShipments[item.getItemName()] = item.getDemandShipments()
		
		# Alternative implementation:
		# limit population to look only at purchased items:
		# if item.isPurchased():
			# itemDemandShipments[item.getName()] = item.getDemandShipments()
		
		
	return itemDemandShipments

if __name__ == "__main__":	
	pass
	