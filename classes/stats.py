# filename stats.py


class Stats(object):
	"""
	The stats object is pointed to by and retrievable from 
	the item object.  Data and functions contained herein 
	are useful in determining the Reorder Point.

	Reorder Point = Cycle Stock + Demand Safety Stock + Supply Safety Stock.
		
	Safety Stock is roughly per http://media.apics.org/omnow/Crack%20the%20Code.pdf
	"""
	def __init__(self, item):
		""" 
		inputs:
		self 	- object, Stats object
		item	- object, item object
		"""
		# allow access via item.getStat()
		self.item = item
		self.item.setStat(self)		
		
		# Reorder Point = 
		# Cycle Stock + Demand Safety Stock + Supply Safety Stock
		# Cycle Stock = dmdPcMean 
		# Demand Safety Stock = Z * dmdPcStd
		# Supply Safety Stock = Z * supStd * dmdMean
		
		self.dmdPcMean = None		# Demand in PC mean (units 
									#  shipped per PC)
		self.dmdPcStd = None		# Demand in PC Std Dev		
		self.dmdPcN = None			# Demand in PC number of samples
		self.dmdMean = None			# Demand in day mean (units 
								    #  shipped per day)

		self.pc = None  			# Performance Cycle (PC, days)		
		
		self.supMean = None  		# Supply Cycle time
									#  (PO to Invoice, days)
		self.supStd = None			
		self.supN = None

		self.demMean = None  		# Demand Cycle time
									# (SO to Invoice, days)
		self.demStd = None			#  
		self.demN = None	

		self.successor = None   	# successor item adds to the PC	
		

	def setDmd(self):
		""" 
		# Sets demandPcMean and other demand statistics.

		"""
		print "entering Stats.setDmd()"
		
		
		for S in self.item.getDemandShipments():
			print S
			print "S.getStart():", S.getStart()
			print "S.getEnd()", S.getEnd()
			
			
		
			assert False

	def getItem(self):
		return self.item

	def getMeanStdN(self, X):
		try: # if there is any supply or demand
			N = len(X)
			mean = sum(X)/float(N)
			tot = 0.0
			for x in X:
				tot += (x - mean)**2
			std = (tot/N)**0.5	
			return mean, std, N
		except:
			return None, None, None
		
	def setStats(self, X, type):
		"""
		Sets mean and standard deviation of cycle times 
		of deliveries made by supplier or demanded by customer.  
		
		Inputs:
		X 		- list of ints or floats, example [1,2,3,4,5.0]
		type 	- str, either "supply", or "demand"
		
		Action: The following values are set
		mean	- float, mean or average of entries in list 
		std		- float, std deviation of entries
		N 		- int, number of entries
		"""
		
		mean, std, N = self.getMeanStdN(X)
		if type == "supply":
			self.supMean = mean
			self.supStd = std	
			self.supN = N
			self.setPerformanceCycle(meanPOtoInvoice = mean)
		if type == "demand":
			self.demMean = mean
			self.demStd = std	
			self.demN = N
	
	def getSupMean(self):
		""" gives mean of cycle times for supply, ie PO 
		time to Invoice time"""
		return self.supMean
	def getSupStd(self):
		""" gives std deviation of cycle times for supply"""
		return self.supStd
	def getSupN(self):
		""" gives sample size used to calculate supMean and supStd"""
		return self.supN
		
	def setPerformanceCycle(self, 
							meanOrder = 2,
							meanPOtoInvoice = 30,
							meanTransit = 2,
							meanBuild = 7
							):
		"""
		The performance cycle includes the time needed to perform functions 
		such as deciding what to order or produce, communicating orders 
		to the supplier, manufacturing and processing, and delivery and 
		storage, as well as any additional time required to return to the 
		start of the next cycle. 	
		
		PC time in days, example;
		order from supplier = 2
		receive from supplier = 30 ; mean cycle time PO to invoice 
		transit from supplier = 2 ; ship ground
		build, test, ship = 7 days
		PC = 41
		"""
		self.pc = float(meanOrder + meanPOtoInvoice + meanTransit + meanBuild)
		
	def getPerformanceCycle(self):
		"""
		Returns performance cycle of the item and the successor item.
		
		The performance cycle for an item that is issued on consignment
		to the pcb assembly house, for example, must consider 
		the performance cycle for the successor item delivered by the pcb
		assembly house.  
		"""
		
		if not self.successor == None:
			# print "\ntype(self.successor):", type(self.successor)
			# print "type(self.successor.getStat()):", type(self.successor.getStat())
			return self.successor.getStat().getPerformanceCycle() + self.pc
		return self.pc

	def setSuccessor(self, successor):
		""" 
		Inputs:
		successor  - object, item object
		"""
		self.successor = successor
		
	def getSuccessor(self):
		"""
		Outputs:
		successor 	- object, item object
		"""
		return self.successor
		
	def getDemMean(self):
		""" gives mean of cycle times for supply, ie SO 
		time to Invoice time"""
		return self.demMean
		
	def getDemStd(self):
		""" gives std deviation of cycle times for demand"""
		return self.demStd
		
	def getDemN(self):
		""" gives sample size """
		return self.demN		
	def __str__(self):

		str = "\nStats are roughly per http://media.apics.org/omnow/Crack%20the%20Code.pdf \n"
		str += "Stats object for item " + self.item.getItemName()
		str += "  (" + self.item.getItemDesc() + ")\n"
		
		str += "Supply (PO to invoice time, days) stats: \n"
		str += " Item alone:"
		str += "  Mean = " + self.getSupMean().__str__() +" "
		str += "  Std Dev = " + self.getSupStd().__str__() + " "
		str += "  N = " + self.getSupN().__str__() + "\n"
		str += "Mean Performance Cycle (PO to receive, assemble, ship, days)\n"		
		str += "  this item and successor item if any: " 
		str +=    self.getPerformanceCycle().__str__()  + "\n"
		successor = self.getSuccessor() 
		if not successor == None:
			str += "  successor is: " + successor.getItemName().__str__()
			str += " (" + successor.getItemDesc() + ")\n"
			str += "  successor item alone: "
			str += successor.getStat().getPerformanceCycle().__str__() + "\n"
		str += "Demand (SO to invoice time, days) stats: \n"
		str += " Mean = " + self.getDemMean().__str__() +"\n"
		str += " Std Dev = " + self.getDemStd().__str__() + "\n"
		str += " N = " + self.getDemN().__str__() + "\n"
		str += "Demand in Day Avg (dmdMean, units/day):  " + "\n" 
		str += "Demand in PC Avg (dmdPCmean, units/PC):  " + "\n"
		str += "Demand in PC Std Dev (dmdPCstd):  " + "\n "
		
		return str
	
		
def testClassStats():
	import item as itemClass
	item = itemClass.Item("test itemName", "testitemDesc")
	itemStat = Stats(item)
	print "\n\nitemStat (prior to any initialization):", itemStat	
	itemStat.setPerformanceCycle()
	expected = 41
	actual = itemStat.getPerformanceCycle()
	if not actual == expected:
		print "incorrect result in itemStat.getPerformanceCycle():  ",
		print "got:", actual, "expected:", expected
		assert False
	l = [1,2,3]
	itemStat.setStats(l, type = "supply")
	expected = 2.0
	actual = itemStat.getSupMean()
	if not abs(actual - expected) < 0.01:
		print "incorrect result in Stats.setSup(list, type = 'supply'):  ",
		print "got:", actual, "expected:", expected
	expected = 0.8164965809
	actual = itemStat.getSupStd()
	if not abs(actual - expected) < 0.01:
		print "incorrect result in Stats.getSupStd(list):  ",
		print "got:", actual, "expected:", expected
	expected = 3
	actual = itemStat.getSupN()
	if not abs(actual - expected) < 0.01:
		print "incorrect result in Stats.getSupN(list):  ",
		print "got:", actual, "expected:", expected

	print "\n\nitemStat (prior to successorStat Update):", itemStat		
	successor = itemClass.Item("test successorName", "testSuccessorDesc")
	itemStat.setSuccessor(successor)
	successorStat = Stats(successor)
	successorStat.setStats(l, type = "supply")
	successorStat.setPerformanceCycle(meanPOtoInvoice = 10)
	
	print "\n\nitemStat (after to successorStat Update):", itemStat
	expected = 34
	actual = itemStat.getPerformanceCycle()
	if not abs(actual - expected) < 0.01:
		print "incorrect result in Stats.getSupN(list):  ",
		print "got:", actual, "expected:", expected
	

	itemStat.setStats(l, type = "demand")
	print "\n\nitemStat (after Demand Update):", itemStat
	expected = 2.0
	actual = itemStat.getDemMean()
	if not abs(actual - expected) < 0.01:
		print "incorrect result in Stats.getDemMean():  ",
		print "got:", actual, "expected:", expected,
		print "for list:", l
	expected = 3
	actual = itemStat.getDemN()
	if not abs(actual - expected) < 0.01:
		print "incorrect result in Stats.getDemN():  ",
		print "got:", actual, "expected:", expected,
		print "for list:", l
		
if __name__ == "__main__":	
	testClassStats()
