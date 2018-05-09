# itemStats.py

import datetime

import classes.item
import functions.itemStatsFxns

class ItemStats(object):
	def __init__(self, item, transactions):

		assert type(item) == classes.item.Item

		# Make this object callable from the Item object & self
		item.setItemStats(self) 
		self.item = item
		
		# Make inDict with key being Transaction.getType()
		#    value being the transaction.
		#    example: {"pseudoSale": [transaction1, transaction2, ...] ;
		#			   "Build Assembly": [transaction6, transaction4, ...];
		#			   "Invoice": [transaction20, transaction30, ...];
		#			   "Sales Order": [transaction20, transaction30, ...];
		#			   "Bill": [transaction20, transaction30, ...]}				
		inDict = {}
		for xaction in item.getXactions():
			if xaction.getType() in inDict.keys():
				existingValue = inDict[xaction.getType()]
				inDict[xaction.getType()] = existingValue + [xaction]
			else:
				inDict[xaction.getType()] = [xaction]

		# Determine start and end dates in transactions.
		# Using proleptic Gregorian ordinal of the date, 
		# where January 1 of year 1 has ordinal 1
		transactionsStartDay = 836499 # many days into the future
		transactionsEndDay = 1		  # January 1 of year 1
		for transaction in transactions:
			if transaction.getDate().toordinal() < transactionsStartDay:
				transactionsStartDay\
				   = transaction.getDate().toordinal()
			if transaction.getDate().toordinal() > transactionsEndDay:
				transactionsEndDay\
				   = transaction.getDate().toordinal()
		dateStart = datetime.date.fromordinal(transactionsStartDay)
		dateEnd = datetime.date.fromordinal(transactionsEndDay)
		
		
		# Make outDict with key being Transaction.getType()
		#    and value being paired lists statDesc and statValue.
		#    example:  {"PseudoSale": ["total"], [105]}
		# Parse inDict for stats and load these into outDict.
		#    example:  {"PseudoSale": ["total", "2017"], [105, 33]}
		#    example:  {"PseudoSale": ["total", "2017", "2016"], [105, 33, 28]}
		# Continue to parse and load for each key in inDict.		
		#    example:  {"PseudoSale": ["total"], [105]}
		#    example:  {"PseudoSale": ["total", "2017"], [105, 33]}
		#    example:  {"PseudoSale": ["total", "2017", "2016"], [105, 33, 28]}
		#    example:  {"Build Assembly": ["total", "2017"], [105, 33]}
		#    example:  {"Build Assembly": ["total", "2017"], [105, 33]}
		#    example:  {"Build Assembly": ["total", "2017", "2016"], [105, 33, 28]}
		self.outDict = {}
		
		
		# self.statFunctions contain the following:
		#  statFunction - function located in __main__
		#  dateStart	- function parameter, object, datetime.date  
		#  dateEnd		- function parameter, object, datetime.date
		#  descShort	- str, description of statFunction
		#  desc			- str, description of statFunction
		
		self.statFunctions = []
		self.statFunctions +=\
		 [(functions.itemStatsFxns.total, dateStart, dateEnd, "total", "total for all days")]
		self.statFunctions +=\
		 functions.itemStatsFxns.getStatFunctionsString(functions.itemStatsFxns.total, dateStart, dateEnd, "total for year", "year" )
		# self.statFunctions +=\
		 # getStatFunctionsString(total, dateStart, dateEnd, "total for month", "month" )
		# self.statFunctions +=\
		 # getStatFunctionsString(maxmonth, dateStart, dateEnd, "Maximum total for month in year", "year" )
		self.statFunctions +=\
		 functions.itemStatsFxns.getStatFunctionsString(functions.itemStatsFxns.max30day, dateStart, dateEnd, "Maximum total for 30 days in year", "year" )
		self.statFunctions +=\
		 functions.itemStatsFxns.getStatFunctionsString(functions.itemStatsFxns.max10day, dateStart, dateEnd, "Maximum total for 10 days in year", "year" )
		

		
		for key in inDict.keys():
			xactions = inDict[key]
			self.outDict[key] = []
			if key == None:
				print "key:", key 
				print "error key should not be none"
				assert False
			for statFunctionRow in self.statFunctions:
				
				statFunction = statFunctionRow[0]
				dateStart = statFunctionRow[1]
				dateEnd = statFunctionRow[2]
				self.outDict[key] = self.outDict[key]\
									+ [statFunction(xactions,
													dateStart,
													dateEnd)] 
				
	def getOutDict(self):
		return self.outDict
		
	# def getOutDictPhantomSalesStr(self):
		# ret = ""
		# for key in self.outDict.keys()
			# if key == "Phantom Sales":
				# print key, self.outDict[key]
	
		
	def __str__(self):
		""" example output
		#    Summary stats for item V0052 (Some description)
		#    Columns Key:
		#    Column Name, column description (statFunction)
		#    
		#	 buildType 		Total 	2017	2016	...
		#    pseudoSale 	105		33		28		...
		#    build assembly	105		33		28		...	
		#	 ...	  		... 	...		...		...					
		"""
		ret = "==================================================\n"
		ret += "Summary stats for " + self.item.getItemName() +"\n"
		ret += "                 (" + self.item.getItemDesc() + ")\n"
		ret += "Columns Key:\n"
		for statFunctionRow in self.statFunctions:
			ret += " " + statFunctionRow[3] 
			ret += " - " + statFunctionRow[4] 
			ret += " (" + statFunctionRow[1].__str__()
			ret += " through " + statFunctionRow[2].__str__()
			ret += ")\n"
		ret += "-------------------------------------------------\n"
		# first row
		ret += "              "
		for statFunctionRow in self.statFunctions:
			padLength = 7 - len(statFunctionRow[3])
			pad =""
			for padCount in range(padLength):
				pad += " "
			ret += statFunctionRow[3] + pad
		ret += "\n"	
		# other rows 
		for key in sorted(self.outDict.keys()):
			# first column truncate and pad to fit, ie "Build Assembly" becomes "Build Assemb  "
			padLength = 14 - len(key[:12])
			pad = ""
			for padCount in range(padLength):
				pad += " "
			ret += key[:12] + pad

			# other columns
			for stat in self.outDict[key]:
				# other columns are padded to fit.  ie "0.0" becomes "0.0    "
				padLength = 7 - len(stat)
				pad = ""
				for padCount in range(padLength):
					pad += " "
				ret += stat + pad 
			ret += "\n"	
		return ret	
				
				
			
# itemName = 'BP-2000-MP-6-220V'		
# for item in items:
	# if item.getItemName() == itemName:
		# itemStats = ItemStats(item, transactions)
		# break
# for item in items:
	# if item.getItemName() == itemName:
		# print item
