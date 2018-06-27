# filename showplots.py

### 
# lec 15 w edits.py ... excerpts from; edited
###

import random, pylab    # see matplotlib.sourceforge.net	
import numpy  			# see https://docs.scipy.org/doc/numpy/reference/generated/numpy.arange.html
import calendar	

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

def showPlots(items, supply, demand = None, toTest = True):
	""" 
	print data and plot histograms for each supplier 
	requires closing the plot to advance to the next supplier
	
	inputs:
	items 	- list, list of item objects
	supply 	- dictionary, ie, Buys.getbyItem(), Buys.getbySupplier()
	demand 	- dictionary, ie, Sells.getbyItem(), Sells.getbySupplier()
	toTest 	- bol, ie, True returns after plotting the first key in dict.
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
	
	for key in supply.keys():
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
	
		# pylab.figure()
		pylab.subplot(434)
		cycleTimes = [] # duration
		for shipment in demand[key]:
			cycleTimes.append(shipment.getCycleTime())	

		title = ""
		xLabel = "SO to Invoice (days)"
		yLabel = "Demand No. Ships"
		bins = 4
		rwidth =.95
		showStats = True 
		makePlot(title, xLabel, yLabel, bins, rwidth, cycleTimes, showStats)
		
		pylab.subplot(435)
		startTimes = [] # datetime
		for shipment in demand[key]:
			startTimes.append(shipment.getStartDateYear())
			# print "startTimes:", startTimes, "type(startTimes):", type(startTimes)
			# assert False
		title = ""
		xLabel = ""
		yLabel = ""
		cycleTimes = startTimes
		bins=yearBins
		makePlot(title, xLabel, yLabel, bins, rwidth, cycleTimes, 
				 showStats = False, xmin = yearXmin, xmax = yearXmax)
				 
		pylab.subplot(436)
		startTimes = [] # datetime
		for shipment in demand[key]:
			startTimes.append(shipment.getStartDateMonth())
			# print "startTimes:", startTimes, "type(startTimes):", type(startTimes)
			# assert False
		title = ""
		xLabel = "Month No Label"
		yLabel = ""
		cycleTimes = startTimes
		bins=monthBins
		makePlot(title, xLabel, yLabel, bins, rwidth, cycleTimes, 
				 showStats = False, xmin = monthXmin, xmax = monthXmax)
			
	
		# Show qty shipped in histogram
		# 
	
		pylab.subplot(437)
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
		
		pylab.subplot(438)
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
				 
		pylab.subplot(439)
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



		
		pylab.show()
		if toTest:
			return