# filename:  getsupplystats.py

class Shipment(object):
	def __init__(self,buytransaction,shiptransaction):
		self.buy = buytransaction
		self.ship = shiptransaction
		# difference in days between buy and shipment
		diff = shiptransaction.getDate() - buytransaction.getDate()
		self.time = diff.days
	def gettime(self):
		return self.time
	def __str__(self):
		ret = '\n<Shipment:\n'
		ret += ' Lead time (days): ' + self.time.__str__() + '\n'
		ret += self.buy.getShortStr()
		ret += self.ship.getShortStr()
		ret += ' >'
		return ret

def getshipments(item):
	"""
	Gives lead times for each purchase of the product.
	
	Inputs:
	item 		- object, item object
	
	Outputs:
	shipments 	- list, list of shipment objects
	"""

	shiptransactions = []
	shiptransactionTypes = ['Bill', 'Item Receipt']
	buytransactions = []
	buytransactionTypes = ['Purchase Order']
	shipments = []
	
	for transaction in item.getXactions():
		type = transaction.getType()
		if type in shiptransactionTypes:
			shiptransactions.append(transaction)
		elif type in buytransactionTypes:
			buytransactions.append(transaction)
	print "buytransactions:", buytransactions
	print "shiptransactions:", shiptransactions
	
	# (1)look at most recent Purchase Order transaction.
	def getDate(transaction):
		return transaction.getDate()
		
	sortedbuytransactions = sorted(buytransactions, 
								   key=getDate,
								   reverse=True)
	sortedshiptransactions = sorted(shiptransactions, 
								   key=getDate,
								   reverse=True)
								   
	for buy in sortedbuytransactions:
		print "buy:", buy.getShortStr()
		# (2)if received, the quantity will be zero
		#    and a subsequent Item Receipt or Bill is expected.
			
		if buy.getQty() == '0':
		
			buyDte = buy.getDate()
			
			leadTime = datetime.timedelta(999)
			for ship in sortedshiptransactions:
				shipDte = ship.getDate()
				thisLeadTime = shipDte - buyDte 
				zeroLeadTime = shipDte - shipDte
				print "buy:", buy.getShortStr()
				print "ship:", ship.getShortStr()
				print "thisLeadTime:", thisLeadTime, "/n"
				# print "type(thisLeadTime):", type(thisLeadTime)
				if zeroLeadTime <= thisLeadTime < leadTime:
					# possible purchase has shipment arriving after buy
					leadTime = thisLeadTime
					buyTransaction = buy
					shipTransaction = ship
					
			shipments.append(Shipment(buyTransaction,shipTransaction))

	
	return shipments
		

	

	
if __name__ == "__main__":

	import sys
	sys.path.insert(0, '../classes')

	import item
	item = item.Item("test itemName", "test itemDesc")
	print item

	import transaction
	import datetime
	dte = datetime.date(2018,6,12)
	t = transaction.Transaction("item", "desc", "tNum", "type", dte, "num","qty","soNum", "soDte")
	print t
	
	item.addXaction(transaction.Transaction("item", "desc", "11", 
					"Bill", datetime.date(2017,6,19)
					, "num","11","soNum", "soDte")
					)	
	item.addXaction(transaction.Transaction("item", "desc", "11", 
					"Bill", datetime.date(2017,6,19)
					, "num","11","soNum", "soDte")
					)	
	item.addXaction(transaction.Transaction("item", "desc", "11", 
					"Build Assembly", datetime.date(2017,7,19)
					, "num","11","soNum", "soDte")
					)		
	item.addXaction(transaction.Transaction("item", "desc", "11", 
					"Bill", datetime.date(2017,10,17)
					, "num","11","soNum", "soDte")
					)	
	item.addXaction(transaction.Transaction("item", "desc", "11", 
					"Bill", datetime.date(2017,10,17)
					, "num","11","soNum", "soDte")
					)	
	item.addXaction(transaction.Transaction("item", "desc", "11", 
					"Bill", datetime.date(2017,10,17)
					, "num","11","soNum", "soDte")
					)	
	item.addXaction(transaction.Transaction("item", "desc", "11", 
					"Build Assembly", datetime.date(2017,11,11)
					, "num","11","soNum", "soDte")
					)	
	item.addXaction(transaction.Transaction("item", "desc", "11", 
					"Bill", datetime.date(2017,11,28)
					, "num","11","soNum", "soDte")
					)	
	item.addXaction(transaction.Transaction("item", "desc", "11", 
					"Bill", datetime.date(2017,11,28)
					, "num","11","soNum", "soDte")
					)	
	item.addXaction(transaction.Transaction("item", "desc", "11", 
					"Build Assembly", datetime.date(2018,2,9)
					, "num","11","soNum", "soDte")
					)	
	item.addXaction(transaction.Transaction("item", "desc", "11", 
					"Item Receipt", datetime.date(2018,5,29)
					, "num","11","soNum", "soDte")
					)	
	item.addXaction(transaction.Transaction("item", "desc", "11", 
					"Build Assembly", datetime.date(2018,6,1)
					, "num","11","soNum", "soDte")
					)	

	item.addXaction(transaction.Transaction("item", "desc", "11", 
					"Purchase Order", datetime.date(2017,5,23)
					, "num","0","soNum", "soDte")
					)	
	item.addXaction(transaction.Transaction("item", "desc", "11", 
					"Purchase Order", datetime.date(2017,9,6)
					, "num","0","soNum", "soDte")
					)	
	item.addXaction(transaction.Transaction("item", "desc", "11", 
					"Purchase Order", datetime.date(2017,10,31)
					, "num","0","soNum", "soDte")
					)	
	item.addXaction(transaction.Transaction("item", "desc", "11", 
					"Purchase Order", datetime.date(2018,4,23)
					, "num","0","soNum", "soDte")
					)	

			
	# for t in item.getXactions():
		# print "\n\ntransactions in item:\n"	
		# print t
		
	shipments = getshipments(item)
	
	for shipment in shipments:
		print shipment

	