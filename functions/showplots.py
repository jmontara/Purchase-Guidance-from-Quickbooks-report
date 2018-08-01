# filename showplots.py

### 
# lec 15 w edits.py ... excerpts from; edited
###

import random, pylab    # see matplotlib.sourceforge.net	
import numpy  			# see https://docs.scipy.org/doc/numpy/reference/generated/numpy.arange.html
import calendar	
import classes.stats
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
	
def labelPlot(mean, sd, N):

	fs = '8' # fontsize
	xmin, xmax = pylab.xlim()
	ymin, ymax = pylab.ylim()
	# pylab.text(xmin + (xmax-xmin)*0.02, (ymax-ymin)/2,    
	pylab.text(xmin + (xmax-xmin)*0.4, (ymax-ymin)/2,   # locate  
			   'Mean = ' + str(round(mean, 1))           # & place text
			   + '\nSD = ' + str(round(sd, 1))
			   + '\nN = ' + str(N), fontsize = fs)          # on plot
			   
def makePlot(title, xLabel, yLabel, bins, rwidth, leadtimes, 
			showStats = False, xmin = None, xmax = None):
	"""
	plots histogram.  
	Shows mean, standard deviation, and sample size.
	
	requires executing pylab.show() after calling this function
	
	Inputs:
	supplier 	- str, supplier name
	xLabel
	yLabel
	bins
	rwidth
	leadtimes	- list, list of ints, ie, cycle times for supplier
	"""	
	fs = '7' # fontsize
	pylab.hist(leadtimes, bins = bins, rwidth = rwidth)        # Histogram!
	pylab.title(str(title), loc = 'left', fontsize = '12')
	pylab.xlabel(xLabel, fontsize = fs)
	pylab.ylabel(yLabel, fontsize = fs)
	pylab.xticks(fontsize = fs)
	if xLabel == 'Month':
		pylab.xticks( numpy.arange(12), calendar.month_name[1:13],
		rotation=90 )
	if xLabel == 'Month No Label':
		pylab.xticks( numpy.arange(12), ("","","","","","","","","","","",""),
		rotation=90 )
	pylab.yticks(fontsize = fs)

	# locs, labels = pylab.xticks()
	# print "\n\nlocs, labels:", locs, labels
	# for xtickslabel in labels:
		# print xtickslabel	
	
	if showStats:
		if len(leadtimes) == 0:
			N = 0.0
			sd = 0.0
			mean = 0.0
		else:
			N = str(len(leadtimes))
			sd = stdDev(leadtimes)
			mean = sum(leadtimes)/float(len(leadtimes))

		labelPlot( mean, sd, N)
	if not xmin == None:
		pylab.xlim(xmin, xmax)
	
def getsort(shipment):
	""" 
	gives something used in sort.
	Question:  inaccessible class Shipment function getCycleTime
	"""
	pass
	# cyclestring = shipment.getCycleTime()
	# ret = str(shipment.getCycleTime())
	# for i in range(10 - len(ret)):
		# ret = " " + ret
	# # ret += shipment.getItemName()
	# ret = shipment.getCycleTime()
	# return ret

def showPlots(items, supply, demand = None):
	""" 
	print data and plot histograms for each supplier 
	requires closing the plot to advance to the next supplier
	
	requires that start of period for which data is plotted be 
	periodStart = datetime.day(2015,1,1).toordinal()
	
	inputs:
	items 	- list, list of item objects
	supply 	- dictionary, ie, Buys.getbyItem(), Buys.getbySupplier()
	demand 	- dictionary, ie, Sells.getbyItem(), Sells.getbySupplier()
	"""
	
	# standard plot scales that "look ok":
	yearBins = 4  # num of years in data 
	yearXmin =2014 # year before earliest year in data
	yearXmax =2019 # year after latest year in data
	monthBins = 12 
	monthXmin = 0
	monthXmax =13
	
	itemName2Object = {}
	for item in items:
		itemName2Object[item.getItemName()] = item
		# import cycletimes
		# itemStats = cycletimes.classes.stats.Stats()
		# item.setStat(itemStats)
		
	for key in supply.keys():
		# to look at only one item, uncomment the following two lines
		# if not key == "Heater-3x5-220":
			# continue
	
		# pylab.figure()
		pylab.subplot(431)
		cycleTimes = [] # duration
		for shipment in supply[key]:
			cycleTimes.append(shipment.getCycleTime())	
		title = key 
		if key in itemName2Object.keys():
			# key is an item name, add the description
			title += " (" + itemName2Object[key].getItemDesc()[:25] + " ...)"
			title = title[:50]
		xLabel = "PO to Invoice (days)"
		yLabel = "Supply No. Ships"
		bins = 4
		rwidth =.95
		showStats = True 
		makePlot(title, xLabel, yLabel, bins, rwidth, cycleTimes, 
				showStats)
		
		meanPOtoInvoice = 0

		for cycleTime in cycleTimes:
			meanPOtoInvoice += cycleTime
		meanPOtoInvoice=meanPOtoInvoice/len(cycleTimes)
		itemName2Object[key].getStat().setPerformanceCycle(
							 meanPOtoInvoice=meanPOtoInvoice)
		# print "cycleTimes:", cycleTimes		
		# print "meanPOtoInvoice:", meanPOtoInvoice
		# print "itemName2Object[key].getStat().getPerformanceCycle():",
		# print itemName2Object[key].getStat().getPerformanceCycle()
		
		### The following lines are test of Stats object for consistency with graph
		# itemStats.setStats(cycleTimes, type = "supply")
		# print "itemStats:", itemStats
		
		# pylab.figure()
		pylab.subplot(432)
		startTimes = [] # datetime
		for shipment in supply[key]:
			startTimes.append(shipment.getStartDateYear())
			# print "startTimes:", startTimes, "type(startTimes):", type(startTimes)
			# assert False
		title = ""
		xLabel = ""
		yLabel = ""
		cycleTimes = startTimes
		bins = yearBins
		makePlot(title, xLabel, yLabel, bins, rwidth, cycleTimes, 
				 showStats = False, xmin = yearXmin, xmax = yearXmax)
		
		# pylab.figure()
		pylab.subplot(433)
		startTimes = [] # datetime
		for shipment in supply[key]:
			startTimes.append(shipment.getStartDateMonth())
			# print "startTimes:", startTimes, "type(startTimes):", type(startTimes)
			# assert False
		title = ""
		xLabel = "Month No Label"
		yLabel = ""
		cycleTimes = startTimes
		bins =monthBins
		makePlot(title, xLabel, yLabel, bins, rwidth, cycleTimes, 
				 showStats = False, xmin = monthXmin, xmax = monthXmax)
	
		# # pylab.figure()
		# pylab.subplot(434)
		# cycleTimes = [] # duration
		# for shipment in demand[key]:
			# cycleTimes.append(shipment.getCycleTime())	

		# title = ""
		# xLabel = "SO to Invoice (days)"
		# yLabel = "Demand No. Ships"
		# bins = 4
		# rwidth =.95
		# showStats = True 

		# print "demand[key]:", demand[key]
		# for shipment in demand[key]:
			# print shipment
		# print "key:", key
		# print "cycletimes:", cycleTimes
		# makePlot(title, xLabel, yLabel, bins, rwidth, cycleTimes, showStats)
		
		# pylab.subplot(435)
		# startTimes = [] # datetime
		# for shipment in demand[key]:
			# startTimes.append(shipment.getStartDateYear())
			# # print "startTimes:", startTimes, "type(startTimes):", type(startTimes)
			# # assert False
		# title = ""
		# xLabel = ""
		# yLabel = ""
		# cycleTimes = startTimes
		# bins=yearBins
		# makePlot(title, xLabel, yLabel, bins, rwidth, cycleTimes, 
				 # showStats = False, xmin = yearXmin, xmax = yearXmax)
				 
		# pylab.subplot(436)
		# startTimes = [] # datetime
		# for shipment in demand[key]:
			# startTimes.append(shipment.getStartDateMonth())
			# # print "startTimes:", startTimes, "type(startTimes):", type(startTimes)
			# # assert False
		# title = ""
		# xLabel = "Month No Label"
		# yLabel = ""
		# cycleTimes = startTimes
		# bins=monthBins
		# makePlot(title, xLabel, yLabel, bins, rwidth, cycleTimes, 
				 # showStats = False, xmin = monthXmin, xmax = monthXmax)
			
	
		# Show qty shipped in histogram
		# 
	
		pylab.subplot(434)
		cycleTimes = [] # duration
		for shipment in demand[key]:
			# print "\nshipment.getQty", shipment.getQtyInt(),
			# print type(shipment.getQtyInt())
		# assert False	
			for qtyDemanded in range(shipment.getQtyInt()):
				cycleTimes.append(shipment.getCycleTime())	

		title = ""
		xLabel = "PO/SO to Invoice (days)"
		yLabel = "Demand Qty. "
		bins = 4
		rwidth =.95
		showStats = True 
		makePlot(title, xLabel, yLabel, bins, rwidth, cycleTimes, showStats)
		### The following lines are test of Stats object for consistency with graph
		# itemStats.setStats(cycleTimes, type = "demand")
		# print "itemStats:", itemStats

		
		pylab.subplot(435)
		startTimes = [] # datetime
		for shipment in demand[key]:
			for qtyDemanded in range(shipment.getQtyInt()):
				startTimes.append(shipment.getStartDateYear())
			# print "startTimes:", startTimes, "type(startTimes):", type(startTimes)
			# assert False
		xLabel = 'Year'
		yLabel = ''
		cycleTimes = startTimes
		bins=yearBins
		makePlot(title, xLabel, yLabel, bins, rwidth, cycleTimes, 
				 showStats = False, xmin = yearXmin, xmax = yearXmax)
				 
		pylab.subplot(436)
		startTimes = [] # datetime
		for shipment in demand[key]:
			for qtyDemanded in range(shipment.getQtyInt()):
				startTimes.append(shipment.getStartDateMonth())
			# print "startTimes:", startTimes, "type(startTimes):", type(startTimes)
			# assert False
		xLabel = 'Month'
		cycleTimes = startTimes
		bins=monthBins
		makePlot(title, xLabel, yLabel, bins, rwidth, cycleTimes, 
				 showStats = False, xmin = monthXmin, xmax = monthXmax)

				 
		# subplot in 4 row 3 column matrix position 12	
		item = itemName2Object[key]
		pc = item.getStat().getPerformanceCycle()		
		import datetime
		pylab.subplot(4,3,12)
		startTimes = [] # duration
		for shipment in demand[key]:
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
		# The last day of the period for which data is being parsed
		periodEnd = datetime.date.today().toordinal()
		# number of full and partial PC cycles in periodStart - periodEnd
		try:
			pcCycles = int((periodEnd - periodStart)/pc) + 1
		except:
			pcCycles = 0
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

		# print "countOfQtyInPCList:", countOfQtyInPCList
		
		
		title = "Demand Qty Vs. Count"
		xLabel = "Qty in Performance Cycle"
		yLabel = "Count of Qty in Performance Cycle"
		bins = 8
		rwidth =.95
		showStats = True 
		cycleTimes = countOfQtyInPCList
		makePlot(title, xLabel, yLabel, bins, rwidth, cycleTimes, showStats)
			
		pylab.subplot(4,3,10)
		item = itemName2Object[key]
		pc = item.getStat().getPerformanceCycle()
		pcDmdAvg = ''
		pcDmdStd = ''
		supLtStd = ''
		yrDmdAvg = ''
		pcDmdAvg = ''
		ssDemand = ''
		ssSupply = ''
		roPt1 = '0'
		roPt2 = '0'
		roPt3 = '0'
		unitCost = '0'
		
		
		str = "(roughly per http://media.apics.org/omnow/Crack%20the%20Code.pdf )\n"
		str += "Safety Stock (SS) CALCULATIONS:\n"
		str += "Performance Cycle (PC): " + pc.__str__() + " (days)\n"
		str += "Demand in PC Avg (pcDmdAvg): " + pcDmdAvg.__str__() + " units/PC\n"
		str += "Demand in PC Std Dev (pcDmdStd): " + pcDmdStd.__str__() + " units\n"
		str += "Supply lead Time Std Dev (supLtStd): " + supLtStd.__str__() + "days"
		str += "Demand in Day Avg (dayDmdAvg): " + yrDmdAvg.__str__() + " units/day\n"
		str += "\n"
		str += "Cycle Stock = pcDmdAvg = " + pcDmdAvg.__str__() + " units\n"
		str += "Demand SS = 1.65 * pcDmdStd: = " + ssDemand.__str__() +" units\n"
		str += "Supply SS = 1.65 * supLtStd * dayDmdAvg = " + ssSupply.__str__() + " units\n"
		str += "R.O. Point = Cycle Stock + Demand SS + Supply SS\n " 
		str += "      = " + roPt1.__str__() + "units\n"
		str += "R.O. Point = Cycle Stock + ((Demand SS)^2 + (Supply SS)^2)^(1/2) \n"
		str += "      = " + roPt2.__str__() + "units\n"
		str += "\n"
		str += "R.O. Point from Quickbooks = " + roPt3.__str__() + " units\n"
		str += "Unit Cost = " + unitCost.__str__() + " $\n"
		str += "Savings Possible = (R.O. Point from QB - R.O. Point) * Unit Cost \n"
		savings = (float(roPt3) - float(roPt2)) * float(unitCost)
		str += "      = " + savings.__str__() + "$ savings possible\n"
		
		pylab.hist([])
		pylab.xticks( numpy.arange(12), ("","","","","","","","","","","",""),
		rotation=90 )		
		pylab.yticks( numpy.arange(12), ("","","","","","","","","","","",""),
		rotation=90 )				
		xmin, xmax = pylab.xlim()
		ymin, ymax = pylab.ylim()	
		pylab.text(xmin + (xmax-xmin)*0.02, (ymax-ymin)/10, str, fontsize = "5")
				
		print "item:", item
		print "itemStat:", item.getStat()
		
		pylab.show()
		# if toTest:
			# return