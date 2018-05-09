# itemStatsFxns.py
import datetime
import classes.itemStats

def total(transactions, dateStart, dateEnd):
	"""
	returns the sum of quantities in transactions that 
	occur on dateStart, on dateEnd, and between 
	dateStart and dateEnd.

	Inputs:
	transactions	- list, list of transaction objects
	dateStart		- datetime.date object
	dateEnd			- datetime.date object
	
	Outputs:
	ret				- str, string representation of total
	
	"""
	ret = 0.0
	for transaction in transactions:
		# skip if not between start and end date
		if not dateStart <= transaction.getDate() <= dateEnd:
			continue
		try:
			ret += float(transaction.getQty())
		except:
			# skip transactions that have "" in the qty column
			if not transaction.getQty() == "":
				print transaction
				print "\n\nError, garbage in transaction.getQty()"
				print "converting transaction qty to float"
				assert False			
	return str(ret)

def testTotal():
	""" 
	creates transactions
	sends to the function total
	returns value of total
	"""
	transactions = []

	for day in range(18):
		if day < 10:
			continue
		item = "item" + str(day)
		desc = "desc" + str(day)
		tNum = "tnum" + str(day)
		type = "type" + str(day)
		dte =  datetime.date.fromordinal(day+1)
		num = "num" + str(day)
		qty = str(1)
		soNum = "soNum" + str(day)
		transactions.append(classes.transaction.Transaction(item, desc, tNum, type, dte,
							num, qty, soNum, soDte=None))
	
	dayStart = datetime.date.fromordinal(10)
	dayEnd = datetime.date.fromordinal(20)
							
	return total(transactions, dayStart, dayEnd)
	
# print testTotal()
# assert False
	
	
def getStatFunctionsString(statFunction, dateStart, dateEnd, desc, slice="year"):
	""" 
	returns a list of tuples used within ItemStat object
	
	Inputs:
	statFunction 	- function name, statFunction
	dateStart 		- object, datetime.date 
	dateEnd			- object, dateTime.date
	desc			- str, description
	slice			= str, description of the slices of dates for each tuple in list to be output	
	Outputs:
	L				= list of tuples having the form used within statFunctions
					  
					  if slice == "year" and statFunction == total	
					  example [(total, dateStart1, dateEnd1, "Y0", "total"),
							   (total, dateStart2, dateEnd2, "Y1", "total"),
							   ...
							   (total, dateStart3, dateEnd3, "Yn", "total")]
							   
					  if slice == "month" and statFunction == total	
					  example [(total, dateStart1, dateEnd1, "Y0M1", "total"),
							   (total, dateStart2, dateEnd2, "Y0M2", "total"),
							   ...
							   (total, dateStart12, dateEnd12, "Y0M12", "total"),]

   				      if slice == "year" and and statFunction == maxMonth
					  example [(max, dateStart1, dateEnd1, "MMY0", "max month total"),
							   (max, dateStart2, dateEnd2, "MMY1", "max month total"),
							   ...
							   (max, dateStartn, dateEndn, "MMYn", desc), "max month total"]
							   
   				      if slice == "year" and and statFunction == max30day
					  example [(max, dateStart1, dateEnd1, "M30Y0", "max 30 day total"),
							   (max, dateStart2, dateEnd2, "M30Y1", "max 30 day total"),
							   ...
							   (max, dateStartn, dateEndn, "M30Yn", desc), "max 30 day total"]

   				      if slice == "year" and and statFunction == max10day
					  example [(max, dateStart1, dateEnd1, "M10Y0", "max 10 day total"),
							   (max, dateStart2, dateEnd2, "M10Y1", "max 10 day total"),
							   ...
							   (max, dateStartn, dateEndn, "M10Yn", desc), "max 10 day total"]
							   
	"""
	L = []
	limit = 12 # columns limited to print nicely
	
	if slice == "year" and statFunction == total:
		yearsStart = dateStart.__getattribute__("year")
		yearsEnd = dateEnd.__getattribute__("year") 
		year = yearsStart
		while year <= yearsEnd:
			dateStartSlice = datetime.date(year, 1, 1)
			year += 1
			
			dateEndSlicePlus1day = datetime.date(year, 1, 1)
			dateEndSliceOrdinal = dateEndSlicePlus1day.toordinal() - 1
			dateEndSlice = datetime.date.fromordinal(dateEndSliceOrdinal)
			
			descShort = "Y" + str(year - yearsStart -1)

			T = (statFunction, 
				 dateStartSlice,
				 dateEndSlice,
				 descShort,
				 desc)
			L += [T]
			
		return L[:limit]		
	
	if slice == "month" and statFunction == total:
		yearsStart = dateStart.__getattribute__("year")
		yearsEnd = dateEnd.__getattribute__("year") 
		year = yearsStart - 1
		while year <= yearsEnd:
			year += 1
			month = 0
			while month < 12:
				month += 1
				dateStartSlice = datetime.date(year, month, 1)
				try: 
					dateEndSlicePlus1day = datetime.date(year, month + 1, 1)
				except: # the 13th month
					dateEndSlicePlus1day = datetime.date(year+1, 1, 1)
				dateEndSliceOrdinal = dateEndSlicePlus1day.toordinal() - 1
				dateEndSlice = datetime.date.fromordinal(dateEndSliceOrdinal)			
			
				descShort = "Y" + str(year - yearsStart)	
				descShort += "M" + str(month)
			
				T = (statFunction, 
					 dateStartSlice,
					 dateEndSlice,
					 descShort,
					 desc)
				L += [T]
				
		return L[:limit]

	if slice == "year" and statFunction == maxmonth:
		yearsStart = dateStart.__getattribute__("year")
		yearsEnd = dateEnd.__getattribute__("year") 
		year = yearsStart - 1
		while year < yearsEnd:
			year += 1
			dateStartSlice = datetime.date(year, 1, 1)
			dateEndSlicePlus1day = datetime.date(year +1, 1, 1)
			dateEndSliceOrdinal = dateEndSlicePlus1day.toordinal() - 1
			dateEndSlice = datetime.date.fromordinal(dateEndSliceOrdinal)			

			descShort = "MM"		
			descShort += "Y" + str(year - yearsStart)	
		
			T = (statFunction, 
				 dateStartSlice,
				 dateEndSlice,
				 descShort,
				 desc)
			L += [T]
				
		return L[:limit]
		
	if slice == "year" and statFunction == max30day:
		yearsStart = dateStart.__getattribute__("year")
		yearsEnd = dateEnd.__getattribute__("year") 
		year = yearsStart - 1
		while year < yearsEnd:
			year += 1
			dateStartSlice = datetime.date(year, 1, 1)
			dateEndSlicePlus1day = datetime.date(year +1, 1, 1)
			dateEndSliceOrdinal = dateEndSlicePlus1day.toordinal() - 1
			dateEndSlice = datetime.date.fromordinal(dateEndSliceOrdinal)			

			descShort = "M30"		
			descShort += "Y" + str(year - yearsStart)	
		
			T = (statFunction, 
				 dateStartSlice,
				 dateEndSlice,
				 descShort,
				 desc)
			L += [T]
				
		return L[:limit]

	if slice == "year" and statFunction == max10day:
		yearsStart = dateStart.__getattribute__("year")
		yearsEnd = dateEnd.__getattribute__("year") 
		year = yearsStart - 1
		while year < yearsEnd:
			year += 1
			dateStartSlice = datetime.date(year, 1, 1)
			dateEndSlicePlus1day = datetime.date(year +1, 1, 1)
			dateEndSliceOrdinal = dateEndSlicePlus1day.toordinal() - 1
			dateEndSlice = datetime.date.fromordinal(dateEndSliceOrdinal)			

			descShort = "M10"		
			descShort += "Y" + str(year - yearsStart)	
		
			T = (statFunction, 
				 dateStartSlice,
				 dateEndSlice,
				 descShort,
				 desc)
			L += [T]
				
		return L[:limit]
		

def maxmonth(transactions, dateStart, dateEnd):
	""" 
	assumes dateStart - dateEnd is a period of one year.
	returns the maximum of totals of quantities that fall within a one month period
	"""
	maxMonthTotal = 0.0

	thisYear = dateStart.__getattribute__('year')
	for month in range(1,13,1):
		monthTotal = 0.0
		periodStart = datetime.date(thisYear,month,1)
		try:
			periodEndPlus1Ordinal = datetime.date(thisYear, month +1, 1 ).toordinal()
		except:
			periodEndPlus1Ordinal = datetime.date(thisYear+1, 1,1).toordinal()
		periodEndOrdinal = periodEndPlus1Ordinal -1
		periodEnd = datetime.date.fromordinal(periodEndOrdinal)
		for transaction in transactions:
			if periodStart <= transaction.getDate() <= periodEnd:
				monthTotal += float(transaction.getQty())
				if abs(monthTotal) > abs(maxMonthTotal):
					maxMonthTotal = monthTotal
	
	return str(maxMonthTotal)[:6]

def max30day(transactions, dateStart, dateEnd):
	""" 
	assumes dateStart - dateEnd is a period of one year
	returns the maximum of totals of quantities that fall within a 30 day period
	
	"""
	maxPeriodTotal = 0.0
	
	periodDays = 30

	thisYear = dateStart.__getattribute__('year')
	periodStartOrdinal = datetime.date(thisYear, 1, 1).toordinal()
	periodEndOrdinal = periodStartOrdinal + periodDays
	
	while datetime.date.fromordinal(periodEndOrdinal) <= dateEnd:
		periodTotal = 0.0
		for transaction in transactions:
			if periodStartOrdinal <= transaction.getDate().toordinal() <= periodEndOrdinal:
				periodTotal += float(transaction.getQty())
		if abs(periodTotal) > abs(maxPeriodTotal):
			maxPeriodTotal = periodTotal
		
		periodStartOrdinal += 1
		periodEndOrdinal += 1

	# print "\n\n"	
	# print "dateStart.toordinal()", dateStart.toordinal(), "dateStart:", dateStart.__str__()
	# print "dateEnd.toordinal()", dateEnd.toordinal(), "dateEnd:", dateEnd.__str__()
	# print "periodStartOrdinal", periodStartOrdinal, "periodStart:", datetime.date.fromordinal(periodStartOrdinal).__str__()
	# print "periodEndOrdinal", periodEndOrdinal, "periodEnd:", datetime.date.fromordinal(periodEndOrdinal).__str__()
	# assert False
	
	return str(maxPeriodTotal)[:6]	


def max10day(transactions, dateStart, dateEnd):
	""" 
	assumes dateStart - dateEnd is a period of one year
	returns the maximum of totals of quantities that fall within a 10 day period
	
	"""
	maxPeriodTotal = 0.0
	
	periodDays = 10

	thisYear = dateStart.__getattribute__('year')
	periodStartOrdinal = datetime.date(thisYear, 1, 1).toordinal()
	periodEndOrdinal = periodStartOrdinal + periodDays
	
	while datetime.date.fromordinal(periodEndOrdinal) <= dateEnd:
		periodTotal = 0.0
		for transaction in transactions:
			if periodStartOrdinal <= transaction.getDate().toordinal() <= periodEndOrdinal:
				periodTotal += float(transaction.getQty())
		if abs(periodTotal) > abs(maxPeriodTotal):
			maxPeriodTotal = periodTotal
		
		periodStartOrdinal += 1
		periodEndOrdinal += 1

	# print "\n\n"	
	# print "dateStart.toordinal()", dateStart.toordinal(), "dateStart:", dateStart.__str__()
	# print "dateEnd.toordinal()", dateEnd.toordinal(), "dateEnd:", dateEnd.__str__()
	# print "periodStartOrdinal", periodStartOrdinal, "periodStart:", datetime.date.fromordinal(periodStartOrdinal).__str__()
	# print "periodEndOrdinal", periodEndOrdinal, "periodEnd:", datetime.date.fromordinal(periodEndOrdinal).__str__()
	# assert False
	
	return str(maxPeriodTotal)[:6]	
	

def setItemsStats(items, transactions):
	print "\nsetting items stats"
	for item in items:
		itemStats = classes.itemStats.ItemStats(item, transactions)
