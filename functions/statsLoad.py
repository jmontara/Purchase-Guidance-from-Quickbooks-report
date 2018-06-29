# filename:  statsLoad.py

import classes.stats


def statsLoad(items, buys, sells):
	""" populate performance cycle for each item in items"""

	# create lookup directory and stats object within each item
	itemName2Object = {}
	for item in items:
		itemName2Object[item.getItemName()] = item
		import cycletimes
		itemStat = classes.stats.Stats()
		item.setStat(itemStat)
	

	for item in items:

		#populate buy performance cycle for item alone 
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

		
		print "\nitemName:", itemName,"(", item.getItemDesc(),")"
		print "itemStat:", itemStat
	
	
			
		# assert False
		
	