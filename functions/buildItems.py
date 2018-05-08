# buildItems.py

import classes.item 

	
def buildItems(transactions, itemStatsFromIiqr):
	"""
	Reads list of Transaction objects.
	Builds Item objects and returns a list of these,
	which is sorted in order of item name.  
	
	Inputs:
	transactions 		- list, list of Transaction objects
	itemStatsFromIiqr	- list, a list of tuples taking the form			
								(itemName, itemDesc, value, qty)
								 where value is a subset of 
								 ["Tot On Hand"
								 , "Tot On Sales Order"
								 , "Tot On Purchase Order"]
	
	Returns:
	items 			- list, list of Item objects, which is sorted in order of item name
	"""
	# print itemStatsFromIiqr
	# assert False 
	
	items = []

	itemNames =[]
	for t in transactions:
				
		# Create item and populate with first transaction. 
		if not t.getItemName() in itemNames:
			itemNames.append(t.getItemName())
			newItem = classes.item.Item(t.getItemName(), t.getItemDesc())
			newItem.addXaction(t)
			items.append(newItem)

		# add transaction to existing Item
		else:
			for item in items:
				if item.getItemName() == t.getItemName():
					item.addXaction(t)
					break
					
	for itemStatFromIiqr in itemStatsFromIiqr:

		itemName = itemStatFromIiqr[0]
		itemDesc = itemStatFromIiqr[1]
		value = itemStatFromIiqr[2]
		qty = itemStatFromIiqr[3]
		
		# add itemStat to existing item
		for item in items:		
			if item.getItemName() == itemName\
			   and item.getItemDesc() == itemDesc:

				item.setItemStatsFromIiqr(value, qty)
				# break # leave this for loop
	
	# return a sorted list 
	ret = sorted(items, key=itemsSortKey) # new list
	
	return ret


def itemsSortKey(item):
	return item.getItemName()