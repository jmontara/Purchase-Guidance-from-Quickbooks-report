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

		self.item = item
		# allow access via item.getStat()
		self.item.setStat(self)		
		
		# assembling the successor requires the item
		self.successor = None 

		
		# Reorder Point = 
		# Cycle Stock + Demand Safety Stock + Supply Safety Stock
		# Cycle Stock = dmdPcMean 
		# Demand Safety Stock = Z * dmdPcStd
		# Supply Safety Stock = Z * supStd * dmdPcMean/pc
		
		self.dmdPcMean = None		# Demand in PC mean (units 
									#  shipped per PC)
		self.dmdPcStd = None		# Demand in PC Std Dev		
		self.dmdPcN = None			# Demand in PC number of samples

		self.pc = None  			# Performance Cycle (PC, days)		
		
		self.supMean = None  		# Supply Cycle time
									#  (PO to Invoice, days)
		self.supStd = None			
		self.supN = None

		self.demMean = None  		# Demand Cycle time
									# (SO to Invoice, days)
		self.demStd = None			#  
		self.demN = None	

 
	def setDmd(self):
		""" 
		Sets demandPcMean and other demand statistics as follows:
		
		self.dmdPcMean 	# Demand in PC mean (units shipped per PC)
		self.dmdPcStd 	# Demand in PC Std Dev		
		self.dmdPcN 	# Demand in PC number of samples
		
		These demand statistics are only set if the item is a purchased item
		and if the performance cycle is not None.
		"""

		# print "entering Stats.setDmd()"
		
		# for S in self.item.getDemandShipments():
			# print S
			# print "S.getStart():", S.getStart()
			# print "S.getEnd()", S.getEnd()		
			# assert False
	
	
		import datetime
		
		pc = self.pc
		try:
			assert self.item.isPurchased()
			assert not pc == None
		except:
			print "\nwarning for item ", self.item.getItemName(), self.item.getItemDesc(),
			print "isPurchased:", self.item.isPurchased(),
			print "pc:", pc
			return

		startTimes = [] # duration
		for shipment in self.item.getDemandShipments():
			# print "\nshipment.getQty", shipment.getQtyInt(),
			# print type(shipment.getQtyInt())
		# assert False	
			for qtyDemanded in range(shipment.getQtyInt()):
				startTimes.append(shipment.getStartDate().toordinal())
				
		# print "startTimes:", startTimes
		# print "len(startTimes):", len(startTimes)
		
		# count shipments in each performance cycle and put that into
		countOfQtyInPCList = []
		sortedStartTimes = sorted(startTimes)
		
		# The first day of the period for which data is being parsed
		periodStart = datetime.date(2015,1,1).toordinal()  #
		print "periodStart:", periodStart
		
		# The last day of the period for which data is being parsed
		periodEnd = datetime.date.today().toordinal()
		print "periodEnd:", periodEnd
		
		# the performance cycle
		print "pc:", pc, "for item:", self.item.getItemName(), self.item.getItemDesc()
		
		# number of full and partial PC cycles in periodStart - periodEnd
		pcCycles = int((periodEnd - periodStart)/pc) + 1
		# print "pcCycles:", pcCycles, "pc:", pc
		# first day of first pcCycle
		pcCycleStart = periodStart
		for pcCycle in range(pcCycles):
			# print "pcCycle:", pcCycle
			pcCycleEnd = pcCycleStart + pc
			countOfQtyInPC = 0
			
			for startTime in sortedStartTimes:
				# print "pcCycleStart:", pcCycleStart, "startTime:", startTime, 
				# print "pcCycleEnd:", pcCycleEnd,
				# print "countOfQtyInPC:", countOfQtyInPC
				if pcCycleStart <= startTime <= pcCycleEnd:
					countOfQtyInPC += 1
			countOfQtyInPCList.append(countOfQtyInPC)
			pcCycleStart += pc	
			
		self.dmdPcMean, self.dmdPcStd,	self.dmdPcN = self.getMeanStdN(countOfQtyInPCList)
		
			
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
		of deliveries made by supplier and demanded by customer.  
		
		Also sets the performance cycle to the sum of these two means.
		
		Assumes the call having type "demand" is made after a call having "supply"
		
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

		if type == "demand":
			self.demMean = mean
			self.demStd = std	
			self.demN = N
			self.setPerformanceCycle()

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
		
		Performance cycle is set to durations for 
		demand mean + supply mean, if available.
		If not available, which is the case if no transaction data 
		for buys or sells , input parameters are used to determine the
		performance cycle.
		
		The performance cycle for an item that is purchased, shipped
		to a supplier on consignment, placed in a sub-assembly 
		"successor item" built by the supplier, 
		placed in an assembly, then sold - the successor item adds to 
		the Performance Cycle of the item as follows:
		PC = PC (of item) + supplier mean delivery time (of successor item)
		"""			
		try:
			print "entering setPerformanceCycle() for", self.item.getItemName()
			print "self.getPerformanceCycle():", self.getPerformanceCycle()
			print "self.successor.getItemName():", self.successor.getItemName()
			print "self.successor.getStat().getSupMean() ", self.successor.getStat().getSupMean() 
		except:
			print "no successor"
			
			
		try:  # item with successor  

			self.pc = self.demMean + self.supMean +\
					  self.successor.getStat().getSupMean() 
			print "item with successor, self.pc =", self.pc
			
		except: 
			try: # item alone
				self.pc = self.demMean + self.supMean
				print "item alone, self.pc = ", self.pc
				
			except: #item alone with no qb buy or sell data
				self.pc = float(meanOrder + meanPOtoInvoice + meanTransit + meanBuild)
				print "item alone with no qb buy or sell data, self.pc =", self.pc
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
			
	def getPerformanceCycle(self):
		"""
		Returns performance cycle.
		"""
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
		""" gives mean of cycle times for demand, ie SO 
		time to Invoice time"""
		# print "self.demMean:", self.demMean, "type(self.demMean):", type(self.demMean)
		# if not self.demMean == None: 
			# return self.demMean
		# return 0.0
		return self.demMean
		
	def getDemStd(self):
		""" gives std deviation of cycle times for demand"""
		return self.demStd


	def getDemN(self):
		""" gives sample size """
		return self.demN		

	def getcyclestock(self):
		return self.dmdPcMean
	
	def getdemandSS(self):
		return self.dmdPcStd * 1.65
	
	def getsupplySS(self):
		# print "in getsupplySS"
		ret = 1.65 * self.getSupStd() * self.dmdPcMean / float(self.pc)
		# print ret
		return ret
	
	def getimplicitreorderpoint(self):
		# print "in getimplicitreorderpoint"
		ret = self.getcyclestock() + self.getdemandSS() + self.getsupplySS()
		# print "ret", ret, "type(ret)", type(ret)
		return ret
	def getunitcost(self):
		return self.item.getunitcost()
	def getPhantomROpoint(self):
		return self.item.getPhantomROpoint()
		
	def __str__(self):

		# ret = "\n\nStats are roughly per http://media.apics.org/omnow/Crack%20the%20Code.pdf \n\n"
		ret = "\n"
		ret += "Item: " + self.item.getItemName()
		ret += "  (" + self.item.getItemDesc() + ")\n"
		

		ret += "Supply (duration in days, PO to invoice time): \n"
		try:
			assert not self.getSupMean() == None
			ret += "  Mean = " + str(round(self.getSupMean(), 1))
			ret += "  Std Dev = " + str(round(self.getSupStd(), 1))
			ret += "  N = " + self.getSupN().__str__() + "\n"
		except: # there is no supply
			ret += "  Mean = " + self.getSupMean().__str__()
			ret += "  Std Dev = " + self.getSupStd().__str__() 
			ret += "  N = " + self.getSupN().__str__() + "\n" 
			
		ret += "Demand (duration in days, SO to invoice time):\n"
		try:
			assert not self.getDemMean() == None
			ret += "  Mean = " + str(round(self.getDemMean(), 1)) 
			ret += "  Std Dev = " + str(round(self.getDemStd(), 1))
			ret += "  N = " + self.getDemN().__str__() + "\n"
		except: # there is no demand
			ret += "  Mean = " +  self.getDemMean().__str__() 
			ret += "  Std Dev = " + self.getDemStd().__str__() 
			ret += "  N = " + self.getDemN().__str__() + "\n" 					
		
		ret += "Performance Cycle (PC) (duration in days, PO to receive, assemble, ship)\n"		
		try:
			assert not self.getPerformanceCycle() == None
			ret += "  Mean = " +  str(round(self.getPerformanceCycle(), 1))  + "\n"
		except:
			ret += "  Mean = " + self.getPerformanceCycle().__str__() + "\n"
			
		successor = self.getSuccessor() 
		if not successor == None:
			ret += "  successor is: " + successor.getItemName().__str__()
			ret += " (" + successor.getItemDesc() + ")\n"
			ret += "  successor item alone: "
			ret += successor.getStat().getPerformanceCycle().__str__() + "\n"
			ret += "  successor item supply mean "
			ret += successor.getStat().getSupMean().__str__() + "\n"
		
		ret += "Demand in PC (quantity sold in Performance Cycle):\n"
		try:
			ret += "  Mean = "    + str(round(self.dmdPcMean, 1))
			ret += "  Std Dev = " + str(round(self.dmdPcStd, 1)) 
			ret += "  N = "       + self.dmdPcN.__str__() + "\n"
			ret += "Demand in Day/Month/Year (mean quantity sold in period of time):\n"
			ret += "  per day = " + str(round(self.dmdPcMean / float(self.pc), 1)) 
			ret += "  per month = " + str(round((self.dmdPcMean * 365 /12)/ float(self.pc), 1)) 
			ret += "  per year = " + str(round((self.dmdPcMean * 365) / float(self.pc), 1)) + "\n" 
			ret += "Cycle Stock (cStock) = mean Demand in PC:\n"
			ret += "  cStock = " + str(round(self.getcyclestock(), 1)) + "\n"
			ret += "Demand Safety Stock (dSStock) 1.65 * Demand in PC Std Dev:\n"
			ret += "  dSStock = " + str(round(self.getdemandSS(), 1)) + "\n"
			ret += "Supply Safety Stock (sSStock) 1.65 * Supply Std Dev * Demand per day:\n"
			ret += "  sSStock = " + str(round(self.getsupplySS(), 1)) + "\n"	
			ret += "Implicit Reorder Point (I Ro Point) cStock + dSStock + sSStock:\n" 
			ret += "  iRoPoint = " + str(round(self.getimplicitreorderpoint(),1)) + "\n"
			# ret += "qb Reorder Point (qbRoPoint)\n"
			# ret += "  qbRoPoint = " + str(round(self.item.getROpoint(), 1)) + "\n"
			ret += "qb 'phantom' Reorder Point (qbRoPoint)\n"
			ret += "  getPhantomROpoint() = " + str(round(self.getPhantomROpoint(), 1)) + "\n"
			ret += "qb unit cost:\n"
			try:
				ret += "   getunitcost() = $" + str(round(self.getunitcost(), 2)) + "\n"
			except:
				pass

		except:  # there is no demand
			# ret += "Demand in PC (quantity sold in Performance Cycle):\n"
			# ret += "  Mean = 0"   
			# ret += "  Std Dev = 0" 
			# ret += "  N = 0 \n"       
			# ret += "Demand in Day/Month/Year (mean quantity sold in period of time):\n"
			# ret += "  per day = 0.0"  
			# ret += "  per month = 0.0" 
			# ret += "  per year = 0.0 \n" 
			# ret += "Cycle Stock = mean Demand in PC:\n"
			# ret += "  Mean = 0" 
			ret += "there is no demand\n"

		return ret
	
def testClassStats():
	import item as itemClass
	item = itemClass.Item("test itemName", "testitemDesc")
	itemStat = Stats(item)
	print "\nitemStat (prior to any initialization):", itemStat

	l = [1,2,3]
	itemStat.setStats(l, type = "supply")
	print "\nitemStat (after setting supply stats):", itemStat
	# assert False
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
		
	itemStat.setStats(l, type = "demand")
	print "\nitemStat (after Demand Update):", itemStat
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
		
	# successor = itemClass.Item("test successorName", "testSuccessorDesc")
	# itemStat.setSuccessor(successor)
	# # print "itemStat.getSuccessor():", itemStat.getSuccessor()
	# successorStat = Stats(successor)
	# successorStat.setStats(l, type = "supply")
	# successorStat.setStats(l, type = "demand")
	# print "successorStat.getPerformanceCycle():", successorStat.getPerformanceCycle()
	# successorStat.setPerformanceCycle()
	# itemStat.setPerformanceCycle()
	# print "after setPerformanceCycle:", successorStat.getPerformanceCycle()
	# # assert False
	# print "\n\nitemStat (after to successorStat Update):", itemStat
	# expected = 34
	# actual = itemStat.getPerformanceCycle()
	# if not abs(actual - expected) < 0.01:
		# print "incorrect result in Stats.getSupN(list):  ",
		# print "got:", actual, "expected:", expected
		
	


		
if __name__ == "__main__":	
	testClassStats()
