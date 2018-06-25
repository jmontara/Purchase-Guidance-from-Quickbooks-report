# filename showplots.py

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
def makePlotStartTimes(supplier, startTimes, xlabel = None, xmin = None, xmax = None, bins = None):
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
	if xmax == None:
		return
	pylab.xlim(xmin, xmax)
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
		xmin = 2014
		xmax = 2019
		makePlotStartTimes(key, startTimes, xlabel = xlabel, xmin = xmin, xmax = xmax, bins = 4)				

		# pylab.figure()
		pylab.subplot(333)
		startTimes = [] # datetime
		for shipment in sortedshipments:
			startTimes.append(shipment.getStartDateMonth())
			# print "startTimes:", startTimes, "type(startTimes):", type(startTimes)
			# assert False
		xlabel = 'Month of Supply'
		xmin = 0
		xmax = 13
		makePlotStartTimes(key, startTimes, xlabel = xlabel, xmin = xmin, xmax = xmax, bins = 12)					
		
		pylab.show()
		# if toTest:
			# return