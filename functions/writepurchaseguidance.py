# filename writepurchaseguidance.py

print "\n\nin writepurchaseguidance(items)"


def writepurchaseguidance(items, purchaseguidanceLocation):
	"""
    Write file summarizing purchasing guidance.  
	"""
	
	str = "\n\n"
	str += "Expedite of item(s) on Purchase Orders is required to fill Sales Orders:"
	countItemsToExpedite = 0
	for item in items:
		if item.getExpediteQty() > -0.0:
			expediteQty = item.getExpediteQty().__repr__()
			str +="\n"
			str += " Expedite qty " + expediteQty + " of "
			str += item.getItemName() + " (" + item.getItemDesc() + ")"
			countItemsToExpedite += 1
	str += "\n"
	str += " Expedite of " + countItemsToExpedite.__repr__() 
	str += " item(s) required."
	
	str +="\n\n"
	str += "Purchase of items(s) required to fill Sales Orders:"
	countItemsToPurchase = 0
	for item in items:
		if item.getPurchase1() > -0.0:
			purchQty = item.getPurchase1().__repr__()
			str += "\n"
			str += " Purchase qty " + purchQty + " of " 
			str += item.getItemName() + " (" + item.getItemDesc() +")"
			countItemsToPurchase += 1
	str += "\n"
	str += " Purchase of " + countItemsToPurchase.__repr__() 
	str += " item(s) required." 
	
	str += "\n\n"
	str += "Purchase of item(s) required to fill Sales Orders and maintain RO point:"
	countItemsToPurchase = 0
	for item in items:
		if item.getPurchase2() > -0.0:
			purchQty = item.getPurchase2().__repr__()
			str += '\n'
			str += " Purchase qty " + purchQty 
			str += " of " + item.getItemName() + " (" + item.getItemDesc() +")"
			countItemsToPurchase += 1

	str += "\n"
	str += " Purchase of " + countItemsToPurchase.__repr__() 
	str += " item(s) is required."

	str += "\n\n"
	str += "Open purchase orders exist for the following items:"
	countItemsPurchased = 0
	for item in items:
		if item.getTotPO() > 0.01:
			purchQty = item.getTotPO().__repr__()
			str += "\n"
			str += " Purchased qty " + purchQty + " of " 
			str += item.getItemName() + " (" + item.getItemDesc() +")"
			countItemsPurchased += 1
	str += "\n"
	str += " Receipt of " + countItemsPurchased.__repr__()
	str += " item(s) expected."


	str += "\n\n"
	str += "The following items have negative quantities:"
	countItemsToBuild = 0
	for item in items:
		if item.getTotOH() <=-.01:
			buildQty = item.getTotOH().__repr__()
			str += "\n Build qty" + buildQty + " of "
			str += item.getItemName() + " (" + item.getItemDesc() +")"
			countItemsToBuild += 1
	str += "\n"
	str += " QB inventory adjust or logical build could correct"
	str += " negative counts of " + countItemsToBuild.__repr__() + " item(s)."		

	with open(purchaseguidanceLocation, "w") as text_file:
		text_file.write(str)