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
			endTransaction Type "Bill"
			returns days between the date of the Bill
			and the date of the Purchase Order.
		Example:
			startTransaction Type "Sales Order"
			endTransactionType "Invoice"
			returns days between the date of the 
			Sales Order and the date of the Invoice. 
		"""
		return self.time
	def getOrigin(self):
		return self.origin
	def getDestination(self):
		return self.destination
	def __str__(self):
		ret = '<Shipment.' + self.getClass() + ':'
		ret += '  "' + self.origin + '" --> "' + self.destination + '"\n'
		ret += ' Lead time (days): ' + self.time.__str__() + '\n'
		ret += self.start.getShortStr()
		ret += self.end.getShortStr()
		ret = ret[:-1] + '>'
		return ret

class Buy(Shipment):
	def __init__(self,startTransaction,endTransaction):
		Shipment.__init__(self,startTransaction,endTransaction)
		self.origin = startTransaction.getName() # supplier name
		self.destination = "Manufacturing Warehouse"
		self.item = startTransaction.getItemName()
		# self.category =
	def getClass(self):
		return "Buy"

# class Buys(object):
	# def __init__(self, buyShipmentsByItem):
		# self.byItem = buyShipmentsByItem # dict
		
		# self.bySupplier = {}
		# shipments = []
		# for item in self.byItem.keys():

			# for shipment in self.byItem[item]:

				# shipments.append(shipment)
				
		# for shipment in shipments:

			# supplierName = shipment.getOrigin()
			
			# if supplierName not in bySupplier.keys():		
				# bySupplier[supplierName] =\
					# [shipment.getCycleTime()]
			# else:
				# bySupplier[supplierName] =\
					# bySupplier[supplierName] +\
					# [shipment.getCycleTime()]
		
	# def getbuys(self):
		# """ gives list all buy objects"""
		# ret = []
		# for item in self.byItem.keys():
			# for shipment in buyItems[item]:
				# ret.append(shipment)
				
			
		
class Sell(Shipment):
	def __init__(self,startTransaction,endTransaction):
		Shipment.__init__(self,startTransaction,endTransaction)
		self.destination = startTransaction.getName()
		self.origin = "Manufacturing Warehouse"
	def getClass(self):
		return "Buy"
		
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
						
				buys.append(Buy(startTransaction,endTransaction))
				
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
							"num","qty","soNum", "Supplier Name","memo", "soDte")
	print t
	
	print "\n\n### test some print statements"
	print Buy(t,t)
	# print Sell(t,t)	
	
	item.addXaction(classes.transaction.Transaction("item", "desc", "11", 
					"Bill", datetime.date(2017,6,19)
					, "num","11","soNum", "Supplier Name","memo", "soDte")
					)	
	item.addXaction(classes.transaction.Transaction("item", "desc", "11", 
					"Bill", datetime.date(2017,6,19)
					, "num","11","soNum", "Supplier Name","memo", "soDte")
					)	
	item.addXaction(classes.transaction.Transaction("item", "desc", "11", 
					"Build Assembly", datetime.date(2017,7,19)
					, "num","11","soNum", "Supplier Name","memo", "soDte")
					)		
	item.addXaction(classes.transaction.Transaction("item", "desc", "11", 
					"Bill", datetime.date(2017,10,17)
					, "num","11","soNum", "Supplier Name","memo", "soDte")
					)	
	item.addXaction(classes.transaction.Transaction("item", "desc", "11", 
					"Bill", datetime.date(2017,10,17)
					, "num","11","soNum", "Supplier Name","memo", "soDte")
					)	
	item.addXaction(classes.transaction.Transaction("item", "desc", "11", 
					"Bill", datetime.date(2017,10,17)
					, "num","11","soNum", "Supplier Name","memo", "soDte")
					)	
	item.addXaction(classes.transaction.Transaction("item", "desc", "11", 
					"Build Assembly", datetime.date(2017,11,11)
					, "num","11","soNum", "Supplier Name","memo", "soDte")
					)	
	item.addXaction(classes.transaction.Transaction("item", "desc", "11", 
					"Bill", datetime.date(2017,11,28)
					, "num","11","soNum", "Supplier Name","memo", "soDte")
					)	
	item.addXaction(classes.transaction.Transaction("item", "desc", "11", 
					"Bill", datetime.date(2017,11,28)
					, "num","11","soNum", "Supplier Name","memo", "soDte")
					)	
	item.addXaction(classes.transaction.Transaction("item", "desc", "11", 
					"Build Assembly", datetime.date(2018,2,9)
					, "num","11","soNum", "Supplier Name","memo", "soDte")
					)	
	item.addXaction(classes.transaction.Transaction("item", "desc", "11", 
					"Item Receipt", datetime.date(2018,5,29)
					, "num","11","soNum", "Supplier Name","memo", "soDte")
					)	
	item.addXaction(classes.transaction.Transaction("item", "desc", "11", 
					"Build Assembly", datetime.date(2018,6,1)
					, "num","11","soNum", "Supplier Name","memo", "soDte")
					)	

	item.addXaction(classes.transaction.Transaction("item", "desc", "11", 
					"Purchase Order", datetime.date(2017,5,23)
					, "num","0","soNum", "Supplier Name","memo", "soDte")
					)	
	item.addXaction(classes.transaction.Transaction("item", "desc", "11", 
					"Purchase Order", datetime.date(2017,9,6)
					, "num","0","soNum", "Supplier Name","memo", "soDte")
					)	
	item.addXaction(classes.transaction.Transaction("item", "desc", "11", 
					"Purchase Order", datetime.date(2017,10,31)
					, "num","0","soNum", "Supplier Name","memo", "soDte")
					)	
	item.addXaction(classes.transaction.Transaction("item", "desc", "11", 
					"Purchase Order", datetime.date(2018,4,23)
					, "num","0","soNum", "Supplier Name","memo", "soDte")
					)	

	### small test using above item				
	items = [item]
	
	
    ############################
	# UN-COMMENT OUT THE BLOCK OF CODE BELOW TO RUN LARGE TEST
	############################
	### larger test using items in iiqr
	### locations for input files on laptop:
	iiqrLocation ='C:\Users\Moore\Dropbox (Visitech)\Company Forms\Inventory\Purchase Guidance\iiqr.csv'
	issbiLocation ='C:\Users\Moore\Dropbox (Visitech)\Company Forms\Inventory\Purchase Guidance\issbi.csv'
	### locations for output files on laptop:
	purchaseguidanceLocation ='C:\Users\Moore\Dropbox (Visitech)\Company Forms\Inventory\Purchase Guidance\purchaseguidance.txt'
	itemFilesOutDir = 'C:\Users\Moore\Dropbox (Visitech)\Company Forms\Inventory\Purchase Guidance\item files showing history of builds & demand from sales\\'

	### location for input files on desktop
	iiqrLocation = 'C:\Users\john\Dropbox (Visitech)\Company Forms\Inventory\Purchase Guidance\iiqr.csv'
	issbiLocation= 'C:\Users\john\Dropbox (Visitech)\Company Forms\Inventory\Purchase Guidance\issbi.csv'
	### location for output files on desktop
	purchaseguidanceLocation ='C:\Users\john\Dropbox (Visitech)\Company Forms\Inventory\Purchase Guidance\purchaseguidance.txt'
	itemFilesOutDir = 'C:\Users\john\Dropbox (Visitech)\Company Forms\Inventory\Purchase Guidance\item files showing history of builds & demand from sales\\'

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

	transactions, itemStatsFromIiqr = functions.readiiqr.readiiqr(iiqrLocation)	

	items = functions.buildItems.buildItems(
								transactions = transactions,
								itemStatsFromIiqr = itemStatsFromIiqr)
	

	############################
	# COMMENT OUT THE BLOCK OF CODE ABOVE TO RUN TEST OF SINGLE
	# ITEM WHOSE TRANSACTIONS ARE DEFINED HEREIN
	############################
	
	# limit to last item
	# items = items[-1:]
	
	print "\n\n### getshipments(items):"
	buyShipmentsByItem = getshipments(items)
	# buys = Buys(buyShipmentsByItem)
	
	# show shipments by item
	shipments = []
	for item in buyShipmentsByItem.keys():
		print "\n\nshowing buyShipmentsByItem:"
		print "\nitem.getItemName():", item.getItemName()
		for shipment in buyShipmentsByItem[item]:
			print shipment
			shipments.append(shipment)
			
	# show shipments by supplier
	buyShipmentsBySupplier = {}
	for shipment in shipments:
		#supplier
		supplierName = shipment.getOrigin()
		if supplierName not in buyShipmentsBySupplier.keys():		
			buyShipmentsBySupplier[supplierName] =\
				[shipment.getCycleTime()]
		else:
			buyShipmentsBySupplier[supplierName] =\
				buyShipmentsBySupplier[supplierName] +\
				[shipment.getCycleTime()]
			

	for supplier in buyShipmentsBySupplier.keys():
		print "supplier:", supplier, " lead times: ",
		print buyShipmentsBySupplier[supplier]
		

	for supplier in buyShipmentsBySupplier.keys():

		leadTimes = buyShipmentsBySupplier[supplier]
		shipments = 0
		sumLeadTimes = 0
		min = 99999999
		max = -1
		for leadTime in leadTimes:
			shipments += 1
			sumLeadTimes += int(leadTime)
			if leadTime < min:
				min = leadTime
			if leadTime > max:
				max = leadTime
		avg = sumLeadTimes / shipments
		
		print "\n\n", supplier, 
		print " cycle times: ",
		print buyShipmentsBySupplier[supplier],		
		print "\n lead time stats: ",
		print " shipments:", shipments, "min:", min, "avg:", avg, "max:", max
	
	### 
	# lec 15 w edits.py ... excerpts from; edited
	###

	import random, pylab    # see matplotlib.sourceforge.net			

	###
	#
	# simple plot
	#
	
	# pylab.figure(1)
	# pylab.plot([1,2,3], [1,2,3], 'go-', label='line 1', linewidth=2)
	# pylab.plot([1,2,3], [1,4,9], 'rs-',  label='line 2', linewidth=1)
	# pylab.legend()
	# pylab.title('pylab dot title is this')
	# pylab.xlabel('pylab dot xlabel is this')
	# pylab.ylabel('pylab dot ylabel is this')
	# pylab.savefig('pylab_savefig')
	# pylab.show()
	
	def stdDev(X):
		mean = sum(X)/float(len(X))
		tot = 0.0
		for x in X:
			tot += (x - mean)**2
		return (tot/len(X))**0.5

	# def flip(numFlips):
		# heads = 0.0
		# for i in range(numFlips):
			# if random.random() < 0.5:
				# heads += 1.0
		# return heads/numFlips

	# def flipSim(numFlipsPerTrial, numTrials):
		# fracHeads = []
		# for i in range(numTrials):
			# fracHeads.append(flip(numFlipsPerTrial))
		# return fracHeads
		
	def labelPlot(supplier, mean, sd):
		pylab.title(str(supplier) + ' (' + str(len(supplier)) + ' Shipments) ')
		pylab.xlabel('Cycle Time (days)')
		pylab.ylabel('Number of Shipments')
		xmin, xmax = pylab.xlim()
		ymin, ymax = pylab.ylim()
		pylab.text(xmin + (xmax-xmin)*0.02, (ymax-ymin)/2,   # locate  
				   'Mean = ' + str(round(mean, 6))           # & place text
				   + '\nSD = ' + str(round(sd, 6)))          # on plot
				   
	def makePlot(supplier, leadtimes):
		""""""	
		pylab.hist(leadtimes, bins = 80)        # Histogram!
		xmin,xmax = pylab.xlim()                #  axis values for current fig
		ymin,ymax = pylab.ylim()
		
		sd = stdDev(leadtimes)
		mean = sum(leadtimes)/float(len(leadtimes))
		labelPlot(supplier, mean, sd)
		# pylab.figure()
	
	# plot first supplier in list along with relevant shipments
	supplier = buyShipmentsBySupplier.keys()[0]
	leadTimes = buyShipmentsBySupplier[supplier]
	# relevant shipments
	print "\n\nsupplier name:", supplier
	print "leadTimes:", leadTimes
	print "\n Plot of histograms fails to make sense !"
	print "try printing each buy from the supplier"
	print "maybe need to refactor buyShipmentsBySupplier"
	# 
	makePlot(supplier, leadTimes)
	pylab.show()
	
	