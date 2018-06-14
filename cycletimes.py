# filename:  cycleTimes.py

### cycle times are :
### (1) time between placing an order with a supplier and items received
###     in the warehouse and available to build
### (2) time between customer placing an order and completed systems
###     leaving dock and headed to customer.

class Shipment(object):	
	def __init__(self,startTransaction,endTransaction):
		self.start = startTransaction
		self.end = endTransaction
		# difference in days between start and end
		diff = endTransaction.getDate() - startTransaction.getDate()
		self.time = diff.days
	def getCycleTime(self):
		""" 
		returns the time between start transaction and
		end transaction.  
		Example:
			startTransaction Type "Purchase Order"
			endTransaction Type is "Bill"
			returns days between the date of the Bill
			and the date of the Purchase Order.
		Example:
			startTransaction Type "Sales Order"
			endTransactionType is "Invoice"
			returns days between the date of the 
			Sales Order and the date of the Invoice. 
			
		"""
		return self.time
		
	def __str__(self):
		ret = '\n<Shipment:\n'
		ret += ' Lead time (days): ' + self.time.__str__() + '\n'
		ret += self.start.getShortStr()
		ret += self.end.getShortStr()
		ret += ' >'
		return ret

class Buy(Shipment):
	def getSource(self):
		return self.start.getName()
	def getDest(self):
		return "Manufacturing Warehouse"
		
class Sell(Shipment):
	def getSource(self):
		return "Manufacturing Warehouse"
	def getDest(self):
		return self.end.getName()
		
def getshipments(items):
	"""
	returns dictionaries of objects
	
	Inputs:
	items - list of item objects
	
	Outputs:
	A tuple of dictionaries pointing to shipments,
	buyShipmentsByItem 
				example: {item: [shipment1, shipment2, shipment3]}
	buyShipmentsBySupplier
				example: {supplier: [shipment1, shipment2, shipment3]}
	buyShipmentsByCategory
				example: {category: [shipment1, shipment2, shipment3]}				
	sellShipmentsByItem
				example: {item: [shipment1, shipment2, shipment3]}
	sellShipmentsByCustomer
				example: {customer: [shipment1, shipment2, shipment3]}
	sellShipmentsByCategory
				example: {category: [shipment1, shipment2, shipment3]}
				  
	"""
	#(4) use (2) to populate buyShipmentsBySupplier
	##(5) use (2) to populate buyShipmentsByCategory
	##(6) use (1) to populate sellShipmentsByItem
	##(7) use (6) to populate sellShipmentsByCustomer
	##(8) use (6) to populate sellShipmentsByCategory
	##(9) generate summary stats like samples, lead times, covariance 		
	
	buyShipmentsByItem = {}
	buyStartTransactionTypes = ['Purchase Order']
	buyEndTransactionTypes = ['Bill', 'Item Receipt']

	for item in items:
		startTransactions = []
		endTransactions = []
		buys = []
		for transaction in item.getXactions():
			type = transaction.getType()
			if type in buyStartTransactionTypes:
				startTransactions.append(transaction)
			elif type in buyEndTransactionTypes:
				endTransactions.append(transaction)
		
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
			# If received, the quantity will be zero
			# and a subsequent Item Receipt or Bill is expected.
			if buy.getQty() == '0':
			
				buyDte = buy.getDate()
				
				leadTime = datetime.timedelta(999)
				for ship in sortedEndTransactions:
					shipDte = ship.getDate()
					thisLeadTime = shipDte - buyDte 
					zeroLeadTime = shipDte - shipDte

					if zeroLeadTime <= thisLeadTime < leadTime:
						leadTime = thisLeadTime
						startTransaction = buy
						endTransaction = ship
						
				buys.append(Shipment(startTransaction,endTransaction))
				
		buyShipmentsByItem[item] = buys
		
	return buyShipmentsByItem
		
	
if __name__ == "__main__":

	# import sys
	# sys.path.insert(0, '../classes')

	import classes.item 
	item = classes.item.Item("test itemName", "test itemDesc")
	print item

	import classes.transaction
	import datetime
	dte = datetime.date(2018,6,12)
	t = classes.transaction.Transaction("item", "desc", "tNum", "type", dte, 
							"num","qty","soNum", "name","memo", "soDte")
	print t
	
	
	
	item.addXaction(classes.transaction.Transaction("item", "desc", "11", 
					"Bill", datetime.date(2017,6,19)
					, "num","11","soNum", "name","memo", "soDte")
					)	
	item.addXaction(classes.transaction.Transaction("item", "desc", "11", 
					"Bill", datetime.date(2017,6,19)
					, "num","11","soNum", "name","memo", "soDte")
					)	
	item.addXaction(classes.transaction.Transaction("item", "desc", "11", 
					"Build Assembly", datetime.date(2017,7,19)
					, "num","11","soNum", "name","memo", "soDte")
					)		
	item.addXaction(classes.transaction.Transaction("item", "desc", "11", 
					"Bill", datetime.date(2017,10,17)
					, "num","11","soNum", "name","memo", "soDte")
					)	
	item.addXaction(classes.transaction.Transaction("item", "desc", "11", 
					"Bill", datetime.date(2017,10,17)
					, "num","11","soNum", "name","memo", "soDte")
					)	
	item.addXaction(classes.transaction.Transaction("item", "desc", "11", 
					"Bill", datetime.date(2017,10,17)
					, "num","11","soNum", "name","memo", "soDte")
					)	
	item.addXaction(classes.transaction.Transaction("item", "desc", "11", 
					"Build Assembly", datetime.date(2017,11,11)
					, "num","11","soNum", "name","memo", "soDte")
					)	
	item.addXaction(classes.transaction.Transaction("item", "desc", "11", 
					"Bill", datetime.date(2017,11,28)
					, "num","11","soNum", "name","memo", "soDte")
					)	
	item.addXaction(classes.transaction.Transaction("item", "desc", "11", 
					"Bill", datetime.date(2017,11,28)
					, "num","11","soNum", "name","memo", "soDte")
					)	
	item.addXaction(classes.transaction.Transaction("item", "desc", "11", 
					"Build Assembly", datetime.date(2018,2,9)
					, "num","11","soNum", "name","memo", "soDte")
					)	
	item.addXaction(classes.transaction.Transaction("item", "desc", "11", 
					"Item Receipt", datetime.date(2018,5,29)
					, "num","11","soNum", "name","memo", "soDte")
					)	
	item.addXaction(classes.transaction.Transaction("item", "desc", "11", 
					"Build Assembly", datetime.date(2018,6,1)
					, "num","11","soNum", "name","memo", "soDte")
					)	

	item.addXaction(classes.transaction.Transaction("item", "desc", "11", 
					"Purchase Order", datetime.date(2017,5,23)
					, "num","0","soNum", "name","memo", "soDte")
					)	
	item.addXaction(classes.transaction.Transaction("item", "desc", "11", 
					"Purchase Order", datetime.date(2017,9,6)
					, "num","0","soNum", "name","memo", "soDte")
					)	
	item.addXaction(classes.transaction.Transaction("item", "desc", "11", 
					"Purchase Order", datetime.date(2017,10,31)
					, "num","0","soNum", "name","memo", "soDte")
					)	
	item.addXaction(classes.transaction.Transaction("item", "desc", "11", 
					"Purchase Order", datetime.date(2018,4,23)
					, "num","0","soNum", "name","memo", "soDte")
					)	

	items = [item]
	
	# for t in item.getXactions():
		# print "\n\ntransactions in item:\n"	
		# print t
		
	buyShipmentsByItem = getshipments(items)
	
	print ""
	for item in buyShipmentsByItem.keys():
		print "item.getItemName():", item.getItemName()
		for shipment in buyShipmentsByItem[item]:
			print " shipment:", shipment


	