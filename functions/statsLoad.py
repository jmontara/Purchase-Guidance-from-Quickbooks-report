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
	Set Stats object for each item in items according to content in
	performanceCycle2.csv.
	
	Where one item must be purchased prior to purchase of another
	item, another item is referred to as a successor item.
	
	performanceCycle2.csv has the following columms.

	itemName, successorName 
	
	Example: If itemName has no successors,  pc  = thisPC
	Example:  If itemName has a successor, pc = thisPC + successorPC
	
	"""
	print "\n\n\nentering performancecyclesofassyitem(items, itemName2Object)"
	
	import functions.readperformancecycles2
	item2successor = functions.readperformancecycles2.readperformancecycles2()
	# print "item2successor:", item2successor
	# print "itemName2Object:", itemName2Object
	
	for  itemName in item2successor.keys():


		try:
			itemObject = itemName2Object[itemName]
		except:
			print "problem generating itemObject"
			assert False
		try:
			successorName = item2successor[itemName]
		except:
			print "\n\nfor itemName:", itemName
			print "problem generating successorName"
			assert False
		try:
			successorObject = itemName2Object[successorName]
		except:
			print "successorName:", successorName
			print "problem generating successor object"
			assert False
		try:
			itemStat = itemObject.getStat()
		except:
			print "problem with itemObject.getStat()"
			assert False
		try:
			itemStat.setSuccessor(successorObject)
		except:
			print "problem with itemStat.setSuccessor(successorObject)"
			assert False

	

			
		
def statsLoad(items, buys, sells):
	""" 
	populate performance cycle for each item in items.
	"""
	itemName2Object = {}
	for item in items:
		# create lookup directory
		itemName2Object[item.getItemName()] = item
		# create stats object within each item
		import cycletimes
		itemStat = classes.stats.Stats(item)
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
		

	