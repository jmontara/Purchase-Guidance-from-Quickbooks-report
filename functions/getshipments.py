#  filename:  getshipments.py

import datetime
import cycletimes
		 
def getshipments(items):
	"""
	returns dictionary of shipments 
	
	Inputs:
	items 	- list of item objects
	
	Outputs:
	buyShipmentsByItem, sellShipmentsByItem 
			- list of dictionaries
				example: {item: [shipment1, shipment2, shipment3]}
	"""	
	buyShipmentsByItem = {}
	# startTransactionTypes 
			# - list, list of strings describing start transaction types.
	# endTransactionTypes 
			# - list, list of strings describing end transaction types.
	buyStartTransactionTypes = ['Purchase Order']
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

			if buy.getQty() == '0':
			
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
	
	Inputs:
	items - list of item objects
	
	Outputs:
	ret 
				example: {item: [shipment1, shipment2, shipment3]}
	"""	
	ret = {}
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
			
			# get the most recent end transaction
			leadTime = datetime.timedelta(999)
			for ship in sortedEndTransactions:
				shipDte = ship.getDate()
				thisLeadTime = shipDte - saleDte
				
				zeroLeadTime = shipDte - shipDte
				if zeroLeadTime <= thisLeadTime < leadTime:
					leadTime = thisLeadTime
					startTransaction = sale
					endTransaction = ship

					
			sells.append(cycletimes.Sell(startTransaction,endTransaction))
		
		# only make entries if there are sells
		itemName = item.getItemName()
		if len(sells)>0:
			ret[itemName] = sells
		
	return ret
			