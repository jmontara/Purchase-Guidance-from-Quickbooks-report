# filename stats.py


class Stats(object):
	"""
	The stats object is stored in the item object 
	and includes data and functions to determine Reorder Point.

	Reorder Point = Cycle Stock + Demand Safety Stock + Supply Safety Stock.
		
	Safety Stock is roughly per http://media.apics.org/omnow/Crack%20the%20Code.pdf
	"""
	def __init__(self):
		self.supMean = None  # supply stats
		self.supStd = None
		self.supN = None
		self.demMean = None  # demand stats
		self.demStd = None
		self.demN = None
		
		self.pc = None  # The performance cycle for this item alone
	
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
			
	def setDem(self, X):
		"""
		Sets mean and standard deviation of cycle times 
		of deliveries made to customer.  
		
		Inputs:
		X 	- list of ints or floats, example [1,2,3,4,5.0]
		
		X 	- list of ints or floats, example [1,2,3,4,5.0]
		
		mean	- float, mean or average of entries in list 
		std		- float, std deviation of entries
		N 		- int, number of entries
		"""
		mean, std, N = self.getMeanStdN(X)

	
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
		
		The performance cycle for an item that is issued on consignment
		to the pcb assembly house, for example, must consider 
		the performance cycle for the item delivered by the pcb
		assembly house.  
		"""
		self.pc = meanOrder + meanPOtoInvoice + meanTransit + meanBuild
		
	def getPerformanceCycle(self):
		return self.pc
	def setPerformanceCycleAssy(self, item):
		"""
		considers performance cycle of upper level assemblies
		"""
		raise notimplemented
	def __str__(self):
		str = "Stats object:\n"
		str += "Item Supply (PO to invoice time, days) stats: \n"
		str += " Mean = " + self.getSupMean().__str__() +"\n"
		str += " Std Dev = " + self.getSupStd().__str__() + "\n"
		str += " N = " + self.getSupN().__str__() + "\n"

		str += "Item Demand (SO to invoice time, days) stats: \n"
		str += " Mean = " + self.getDemMean().__str__() +"\n"
		str += " Std Dev = " + self.getDemStd().__str__() + "\n"
		str += " N = " + self.getDemN().__str__() + "\n"		
		return str
		
def testClassStats():
	import classes.item
	item = classes.item.Item("test itemName", "testitemDesc")
	stat = Stats()
	item.setStat(stat)
	stat.setPerformanceCycle()
	expected = 41
	actual = stat.getPerformanceCycle()
	if not actual == expected:
		print "incorrect result in stat.getPerformanceCycle():  ",
		print "got:", actual, "expected:", expected
	
	l = [1,2,3]
	stat.setStats(l, type = "supply")
	expected = 2.0
	actual = stat.getSupMean()
	if not abs(actual - expected) < 0.01:
		print "incorrect result in Stats.setSup(list):  ",
		print "got:", actual, "expected:", expected
	expected = 0.8164965809
	actual = stat.getSupStd()
	if not abs(actual - expected) < 0.01:
		print "incorrect result in Stats.getSupStd(list):  ",
		print "got:", actual, "expected:", expected
	expected = 3
	actual = stat.getSupN()
	if not abs(actual - expected) < 0.01:
		print "incorrect result in Stats.getSupN(list):  ",
		print "got:", actual, "expected:", expected
		
if __name__ == "__main__":	
	testClassStats()
