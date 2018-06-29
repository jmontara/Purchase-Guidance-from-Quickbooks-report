# filename:  statsLoad.py

import classes.stats

def supplycycles(items, buys):
	""" 
	populate supply cycles
	"""
	for item in items:

		itemName = item.getItemName()
		itemStat = item.getStat()
		
		try:
			# list of buy transactions for the item:
			xactions = buys.getbyItem()[itemName]
		except:
			# no buy transactions for the item
			continue 
			
		cycletimes = []
		for xaction in xactions:
			cycletimes.append(xaction.getCycleTime())
		itemStat.setStats(cycletimes, type = "supply")
		
		# print "itemStat:", itemStat
	# assert False

def performancecyclesofassyitem(items, itemName2Object):
	"""
	sets Performance Cycles  for each item in items 
	with consideration of the Performance Cycles
	of an item's upper level assembly.
	
	If the item has no upper level asy, sets equal Performance
	Cycle of the assembly equal to Performance Cycle of the item.
	"""

	for item in items:

		itemPC = item.getStat().getPerformanceCycle()
		if itemPC == None:
			# PO or record of purchase not available for this item:
			continue
		else:
			print "itemName", item.getItemName(), "has nonzero PC"
			# assert False
	
		asys = item.getUpperAssyNames() 
		upperAsyName =''
		upperAsyPC_highest = 0
		
		print "asys:", asys
		for asy in asys:
			upperAsyPC = itemName2Object[asy].getStat().getPerformanceCycle()
			# print "upperAsyPC:", upperAsyPC
			if upperAsyPC == None:
				# PO or record of purchase not available for this asy item
				continue
			if asy == item.getItemName():
				continue
			else:
				print "\n\nitemName", item.getItemName(), "has nonzero PC",
				print "and upper level assy", asy, " has nonzero PC"

			if  upperAsyPC_highest < upperAsyPC:
				upperAsyPC_highest = upperAsyPC
				upperAsyName = asy
		
		item.getStat().setPerformanceCycleAssy(itemPC + upperAsyPC_highest)
		if upperAsyPC_highest >0:
			print "itemName:", item.getItemName(), "(", item.getItemDesc(), ")"
			print "upperAsyName:", upperAsyName
			print "item.getStat():", item.getStat()
			assert False
		
def statsLoad(items, buys, sells):
	""" populate performance cycle for each item in items"""

	# create lookup directory and stats object within each item
	itemName2Object = {}
	for item in items:
		itemName2Object[item.getItemName()] = item
		import cycletimes
		itemStat = classes.stats.Stats()
		item.setStat(itemStat)
	
	supplycycles(items, buys)
	performancecyclesofassyitem(items, itemName2Object)
		
	for item in items:

		#populate demand performance cycle
		itemName = item.getItemName()
		itemStat = item.getStat()
		
		try:
			# list of buy transactions for the item:
			xactions = sells.getbyItem()[itemName]
		except:
			# no buy transactions for the item
			continue 
			
		cycletimes = []
		for xaction in xactions:
			cycletimes.append(xaction.getCycleTime())
		itemStat.setStats(cycletimes, type = "demand")
		
		# print  itemName,"(", item.getItemDesc(),")"
		# print "itemStat:", itemStat
		# assert False		
	