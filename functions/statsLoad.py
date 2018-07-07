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
			assert item.isPurchased() == True
			print "\n\nitem:", item
			print "item isPurchased() == True"
			# list of buy transactions for the item:
			xactions = buys.getbyItem()[itemName]
			print "xactions:", xactions
			for xaction in xactions:
				print xaction
		except:
			# no buy transactions for the item
			print "\n\nno buy transactions for this item:"
			print item
			print "xactions:", xactions
			# assert False
			continue 
			
		cycletimes = []
		for xaction in xactions:
			cycletimes.append(xaction.getCycleTime())
		itemStat.setStats(cycletimes, type = "supply")
	
		print "itemStat:", itemStat
		
	
		# print "itemStat:", itemStat
	# assert False

def performancecyclesofassyitem(items, itemName2Object"):
	"""
	For each item, sets Stats object according to content in
	performanceCycle2.csv.
	
	Where one item must be purchased prior to purchase of another
	item, the one item is referred to herein as a successor item.
	
	performanceCycle2.csv has the following columms.

	itemName, successorName
	
	Example: If itemName has no successors,  pc  = thisPC
	Example:  If itemName has a successor, pc = thisPC + successorPC
	
	"""
	import functions.readperformancecycles2
	itemNameSuccesorNames = functions.readperformancecycles2.readperformancecycles2()
	
	for item in items:

		itemPC = item.getStat().getPerformanceCycle()
		# PO or record of purchase not available for this item:
		if item.isPurchased() == False:
			continue
		
		if item.getItemName() in item2successor.keys():
			itemStatsObject = item.getStat()
			successorStatsObject = itemName2Object[item2successor[item.getItemName()]].getStat()
		
		for asy in asys:
			asyObject = itemName2Object[asy]
			upperAsyPC = asyObject.getStat().getPerformanceCycle()
			# print "asyObject:", asyObject
			
			# PO or record of purchase not available for this asy item
			if upperAsyPC == None:

				print "upperAsyPC == None for item:", 
				print item.getItemName(), "upperAsy:", asyObject.getItemName(),
				print asyObject.getItemDesc()
				continue
			# print "not upperAsyPC == None for item:", 
			# print item.getItemName(), "upperAsy:", asyObject.getItemName()			
			# if asyObject.isPurchased() == False:
				# print "asyObject.isPurchased() == False",
				# print "for item:", item.getItemName(),"asy:", asyObject.getItemName()
				# continue
			print "asyObject.isPurchased() == True"
			print "for item:", item.getItemName(),"asy:", asyObject.getItemName()
			assert False
			if asy == item.getItemName():
				continue
			else:
				print "itemName", item.getItemName(), "has nonzero PC",
				print "and upper level assy", asy, " has nonzero PC"

			if  upperAsyPC_highest < upperAsyPC:
				upperAsyPC_highest = upperAsyPC
				selectedAsyObject = asyObject
		
		if upperAsyPC_highest >0:
			
			asyName = selectedAsyObject.getItemName() + " (" + selectedAsyObject.getItemDesc() + ")"
			mean = selectedAsyObject.getStat().getSupMean()
			std = selectedAsyObject.getStat().getSupStd()
			item.getStat().setStats2(asyName, mean, std)
			
			# test:  uncomment the following block to show purchased asy item.
			print "\n\n\nitemName:", item.getItemName(), "(", item.getItemDesc(), ")\n"
			print "asyName:", asyName
			print "item.getStat():\n", item.getStat()
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
	