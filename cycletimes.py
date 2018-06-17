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
		self.cycleTime = diff.days
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
		return self.cycleTime
	def getItemName(self):
		return self.start.getItemName()
	def getOrigin(self):
		return self.origin
	def getDestination(self):
		return self.destination
	def __str__(self):
		ret = '<Shipment,' + self.getClass() + ':'
		ret += '  "' + self.origin + '" --> "' + self.destination + '"\n'
		ret += ' Lead time (days): ' + self.cycleTime.__str__() + '\n'
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

class Buys(object):
	def __init__(self, buyShipmentsByItem):
		self.byItem = buyShipmentsByItem # dict
		self.bySupplier = self.populatebySupplier()
		
	def getall(self):
		""" 
		gives list of all buy objects
		"""
		ret = []
		for item in self.byItem.keys():
			for buy in self.byItem[item]:
				ret.append(buy)
		return ret

	def getbyItem(self):
		return self.byItem		
	
	def populatebySupplier(self):
		ret = {}
		for buy in self.getall():
			supplierName = buy.getOrigin()
			if supplierName not in ret.keys():		
				ret[supplierName] =	[buy]
			else:
				ret[supplierName] =	ret[supplierName] +	[buy]
		return ret
	
	def getbySupplier(self):
		return self.bySupplier
		
		
class Sell(Shipment):
	def __init__(self,startTransaction,endTransaction):
		Shipment.__init__(self,startTransaction,endTransaction)
		self.destination = startTransaction.getName()
		self.origin = "Manufacturing Warehouse"
	def getClass(self):
		return "Buy"
		
def getshipments(items):
	"""
	returns dictionary
	
	Inputs:
	items - list of item objects
	
	Outputs:
	buyShipmentsByItem 
				example: {item: [shipment1, shipment2, shipment3]}
	"""	
	buyShipmentsByItem = {}
	# and a subsequent ending transaction is expected  
	buyStartTransactionTypes = ['Purchase Order']
	buyEndTransactionTypes = ['Bill', 'Item Receipt']

	for item in items:
		startTransactions = []
		endTransactions = []
		buys = []
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

				# scrub transactions entered with error:
				# <Shipment,Buy:  "Logic Hydraulic Controls Inc" --> "Manufacturing Warehouse"
					 # Lead time (days): 90
					 # <xaction:  Pump, Air, 230V, Air Compressor, 230V, 27745, Purchase Order, 2015-01-20, 2043, 0, , Logic Hydraulic Controls Inc, Air Compressor, 230V>
					 # <xaction:  Pump, Air, 230V, Air Compressor, 230V, 28541, Bill, 2015-04-20, 60621, 7, , Logic Hydraulic Controls Inc, Air Compressor, 230V>>
				if leadTime.days >89:
					continue
						
				buys.append(Buy(startTransaction,endTransaction))
		
		# only make entries if there are buys
		if len(buys)>0:
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
	# COMMENT OUT THE ABOVE BLOCK OF CODE TO RUN TEST OF SINGLE
	# ITEM WHOSE TRANSACTIONS ARE DEFINED ABOVE
	############################
	
	# limit to last item
	# items = items[-1:]
	
	print "\n\n### getshipments(items):"
	buyShipmentsByItem = getshipments(items)
	
	# show shipments by item
	shipments = []
	for item in buyShipmentsByItem.keys():
		print "\n\nshowing buyShipmentsByItem:"
		print "\nitem.getItemName():", item.getItemName()
		for shipment in buyShipmentsByItem[item]:
			print shipment
			shipments.append(shipment)
	# assert False
			
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
		
	def labelPlot(supplier, samples, mean, sd):
		pylab.title(str(supplier) + ' (' + samples + ' Shipments) ')
		pylab.xlabel('Cycle Time (days)')
		pylab.ylabel('Number of Shipments')
		xmin, xmax = pylab.xlim()
		ymin, ymax = pylab.ylim()
		pylab.text(xmin + (xmax-xmin)*0.02, (ymax-ymin)/2,   # locate  
				   'Mean = ' + str(round(mean, 6))           # & place text
				   + '\nSD = ' + str(round(sd, 6)))          # on plot
				   
	def makePlot(supplier, leadtimes):
		"""
		plots histogram of supplier delivery cycle times
		
		requires executing pylab.show() after calling this function
		
		Inputs:
		supplier 	- str, supplier name
		leadtimes	- list, list of ints, cycle times for supplier
		
		"""	
		pylab.hist(leadtimes, bins = 8)        # Histogram!
		xmin,xmax = pylab.xlim()                #  axis values for current fig
		ymin,ymax = pylab.ylim()
		
		samples = str(len(leadtimes))
		sd = stdDev(leadtimes)
		mean = sum(leadtimes)/float(len(leadtimes))
		labelPlot(supplier, samples, mean, sd)
		# pylab.figure()
	
	def getsort(shipment):
		""" 
		gives something used in sort.
		Question:  inaccessible class Shipment function getCycleTime
		"""
		cyclestring = shipment.getCycleTime()
		ret = str(shipment.getCycleTime())
		for i in range(10 - len(ret)):
			ret = " " + ret
		# ret += shipment.getItemName()
		ret = shipment.getCycleTime()
		return ret
	
	def showPlots(dict):
		""" 
		print data and plot histograms for each supplier 
		requires closing the plot to advance to the next supplier
		
		inputs:
		dict 	- dictionary, ie, Buys.getbyItem(), Buys.getbySupplier()
		"""
		for key in dict.keys():
			shipments = dict[key]
			sortedshipments = sorted(shipments, key=getsort)		
			print "\nsortedshipments:", sortedshipments
			cycleTimes = []
			for shipment in sortedshipments:
				print shipment
				cycleTimes.append(shipment.getCycleTime())	
			
			makePlot(key, cycleTimes)
			pylab.show()
			
	buys = Buys(buyShipmentsByItem)
	# all = buys.getall()
	# byItem = buys.getbyItem()
	# bySupplier = buys.getbySupplier()			
	showPlots(buys.getbySupplier())
			
	
	
	