# filename:  cycletimes.py

### cycle times are :
### (1) A buy cycle time is the time between writing a purchase order 
###     for an item and that item being available to build. 
### (2) A sell cycle time is the time between writing a sales order 
###     for an item and that item being invoiced. 

import classes.item 
import classes.transaction
import datetime



class Shipment(object):	
	def __init__(self,startTransaction,endTransaction):
		self.start = startTransaction
		self.end = endTransaction
		# difference in days between start and end
		diff = endTransaction.getDate() - startTransaction.getDate()
		self.cycleTime = diff.days
		self.startDateYear = startTransaction.getDate().year
		self.startDateMonth = startTransaction.getDate().month
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
	def getStartDateYear(self):
		return self.startDateYear
	def getStartDateMonth(self):
		return self.startDateMonth
	def __str__(self):
		ret = '<Shipment, ' + self.getClass() + ':'
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
	def getDestination(self):
		return self.destination
		
class Sells(object):
	def __init__(self, sellShipmentsByItem):
		self.byItem = sellShipmentsByItem # dict
		self.byCustomer = self.populatebyCustomer()
		
	def getall(self):
		""" 
		gives list of all sell objects
		"""
		ret = []
		for item in self.byItem.keys():
			for sell in self.byItem[item]:
				ret.append(sell)
		return ret

	def getbyItem(self):
		return self.byItem		
	
	def populatebyCustomer(self):
		ret = {}
		for sell in self.getall():
			customerName = sell.getDestination()
			if customerName not in ret.keys():		
				ret[customerName] =	[sell]
			else:
				ret[customerName] =	ret[customerName] +	[sell]
		return ret
	
	def populatebyCategory(self):
		
		pass
	
	def getbyCustomer(self):
		return self.byCustomer

	
if __name__ == "__main__":


	item = classes.item.Item("test itemName", "test itemDesc")
	print "*****item object:", item

	dte = datetime.date(2018,6,12)
	t = classes.transaction.Transaction("item", "desc", "tNum", "type", dte, 
							"num","qty","soNum", "Supplier Name","memo", "soDte")
	print "*****transaction object:", t
	
	print "*****Buy object:", Buy(t,t)
	# assert False
	
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
	# UN-COMMENT THE "items = ..." LINE OF CODE BELOW TO RUN LARGE TEST
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
	
	import functions.getshipments

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
	
	print "\n\n### functions.getshipments.getshipments(items):"
	buyShipmentsByItem = functions.getshipments.getshipments(items)
	
	# show shipments by item
	shipments = []
	for item in buyShipmentsByItem.keys():
		print "\n\nshowing buyShipmentsByItem:"
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
		
	def labelPlot(Title, samples, mean, sd):
		pylab.title(str(Title), loc = 'left')
		pylab.xlabel('Cycle Time (days)')
		pylab.ylabel('Number of Shipments')
		xmin, xmax = pylab.xlim()
		ymin, ymax = pylab.ylim()
		# pylab.text(xmin + (xmax-xmin)*0.02, (ymax-ymin)/2,   # locate  
		pylab.text(xmin + (xmax-xmin)*0.02, (ymax-ymin)/2,   # locate  
				   'Mean = ' + str(round(mean, 1))           # & place text
				   + '\nSD = ' + str(round(sd, 1))
				   + '\nN = ' + str(samples))          # on plot
				   
	def makePlot(supplier, leadtimes):
		"""
		plots histogram of supplier delivery cycle times including mean
		and standard deviation.
		
		requires executing pylab.show() after calling this function
		
		Inputs:
		supplier 	- str, supplier name
		leadtimes	- list, list of ints, cycle times for supplier
		
		"""	
		
		pylab.hist(leadtimes, bins = 4, rwidth = .95)        # Histogram!
		xmin,xmax = pylab.xlim()                #  axis values for current fig
		ymin,ymax = pylab.ylim()
		
		samples = str(len(leadtimes))
		sd = stdDev(leadtimes)
		mean = sum(leadtimes)/float(len(leadtimes))
		labelPlot(supplier, samples, mean, sd)
		# pylab.figure()
		
	def labelPlotStartTimes(supplier, samples, dates):
		pylab.title(str(supplier) + ' (' + samples + ' Shipments) ')
		pylab.xlabel('Year of Shipments')
		# pylab.ylabel('Number of Shipments')
		xmin, xmax = pylab.xlim()
		ymin, ymax = pylab.ylim()
		# pylab.text(xmin + (xmax-xmin)*0.02, (ymax-ymin)/2,   # locate  
		# pylab.text(xmin + (xmax-xmin)*0.8, (ymax-ymin)/2,   # locate  
				   # 'Mean = ' + str(round(mean, 1))           # & place text
				   # + '\nSD = ' + str(round(sd, 1)))          # on plot
	def makePlotStartTimes(supplier, startTimes, xlabel = None, bins = None):
		"""
		plots histogram
		
		requires executing pylab.show() after calling this function
		
		Inputs:
		supplier 	- str, supplier name
		leadtimes	- list, list of ints, cycle times for supplier
		
		"""	
		if bins == None:
			uniqueBinContent = []
			for startTime in startTimes:
				if startTime in uniqueBinContent:
					continue
				uniqueBinContent.append(startTime)
			bins = len(uniqueBinContent)
		pylab.hist(startTimes, bins, rwidth = .9)        # Histogram!
		pylab.xlabel(xlabel)
		xmin,xmax = pylab.xlim()            #  axis values for current fig
		ymin,ymax = pylab.ylim()
		
		# samples = str(len(startTimes))
		# labelPlotStartTimes(supplier, samples, startTimes)
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
	
	def showPlots(dict, toTest = True):
		""" 
		print data and plot histograms for each supplier 
		requires closing the plot to advance to the next supplier
		
		inputs:
		dict 	- dictionary, ie, Buys.getbyItem(), Buys.getbySupplier()
		toTest 	- bol, ie, True returns after plotting the first key in dict.
		"""
		for key in dict.keys():
			shipments = dict[key]
			sortedshipments = sorted(shipments, key=getsort)		
			
			# pylab.figure()
			pylab.subplot(331)
			cycleTimes = [] # duration
			for shipment in sortedshipments:
				cycleTimes.append(shipment.getCycleTime())	
			print "key:", key, "type(key)", type(key)
			makePlot(key, cycleTimes)
			
			# pylab.figure()
			pylab.subplot(332)
			startTimes = [] # datetime
			for shipment in sortedshipments:
				startTimes.append(shipment.getStartDateYear())
				# print "startTimes:", startTimes, "type(startTimes):", type(startTimes)
				# assert False
			xlabel = 'Year of Supply'
			makePlotStartTimes(key, startTimes, xlabel = xlabel, bins = 3)				

			# pylab.figure()
			pylab.subplot(333)
			startTimes = [] # datetime
			for shipment in sortedshipments:
				startTimes.append(shipment.getStartDateMonth())
				# print "startTimes:", startTimes, "type(startTimes):", type(startTimes)
				# assert False
			xlabel = 'Month of Supply'
			makePlotStartTimes(key, startTimes, xlabel = xlabel, bins = 12)					
			
			pylab.show()
			# if toTest:
				# return
			
			
	buys = Buys(buyShipmentsByItem)
	# showPlots(buys.getbySupplier())
	
	showPlots(buys.getbyItem())
	# sellShipmentsByItem = functions.getshipments.getshipmentscustomer(items)
	# sells = Sells(sellShipmentsByItem)
	# showPlots(sells.getbyItem())
	# showPlots(sells.getbyCustomer())
	
	
	
			
	### safety stock per http://media.apics.org/omnow/Crack%20the%20Code.pdf
	
	# populate item with indented bom
	# For every invoice transaction for every item in demand,
	#   populate a transaction or transactions of type "demand " 
	#   Appropriate quantity is a multiple of the quantity on 
	#    the invoice transaction and the quantity on the bill of materials.
	#   Appropriate date for transaction is the date of 
	#	 the sales order associated with the invoice.
	
	# populate item with unit price, reorder point
	
	# rank items by strategic value, estimated by something like
	#   itemCostPerYr = avg annual demand * unit cost
	#   itemCostNowInInventory = current inventory * unit cost
	#   itemCostAtROPoint 	= reorder point * unit cost
	# 
	# Limit to look at 10% most strategic parts.	
	# plot demand by item histogram 
	# print 
	#   As Is: 
	#    RO Point 
	#	 * Unit Cost
	#	 =   
	#   Calcs:
	#	PC = 53 days
	#	itemCycleStock = cs (see below)
	#	itemSafetyStockDemand = ss (see below) 	
	#	Proposed:  
	#	 RO Point = 
	#	 
	# Calculate safety stock to accommodate demand variability:
	# 
	# per http://media.apics.org/omnow/Crack%20the%20Code.pdf
	#
	# ss = safety stock
	# Z = Z score, 1.65 for 95% cycle 
	# PC = performance cycle, another term for total lead time 
	# T1 = time increment used for calculating standard deviation of demand  
	# thetaD = standard deviation of demand.
	#
	# ss = Z * sqrt(PC/T1) * thetaD
	#
	# The performance cycle includes the time needed to perform functions 
	# such as deciding what to order or produce, communicating orders 
	# to the supplier, manufacturing and processing, and delivery and 
	# storage, as well as any additional time required to return to the 
	# start of the next cycle. 	
	# 
	# PC time in days, example;
	# order from supplier = 1
	# receive from supplier = 30 ; mean cycle time PO to invoice 
	# transit from supplier = 7 ; ship ground
	# receive = 1 day
	# build, test, ship = 14 days
	# PC = 53
	#
	# cs = cycle stock = PC * avg daily demand
	# 
	# Z = 1 cycle service level = 84% 
	# Z = 1.65 cycle service level = 95% 
	# Note: cycle service level would be significantly 
	# lower than fill rate where actual purchase quantity is 
    # significantly higher than cycle stock.
	# 
	# 
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	