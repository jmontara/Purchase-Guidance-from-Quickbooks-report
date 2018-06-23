# filename writepurchaseguidance.py

import csv

print "\n\nin writepurchaseguidance(items)"


def writepurchaseguidance(items, purchaseguidanceLocation):
	"""
    Write file summarizing purchasing guidance.  
	"""

	str = "\nPurchases required to fill Sales Orders and Maintain RO point:"
	print "\nPurchases required to fill Sales Orders and Maintain RO point:"
	countItemsToPurchase = 0
	for item in items:
		if item.getPurchase2() > -0.0:
			purchQty = item.getPurchase2().__repr__()
			str += '\n'
			str += "  Purchase qty " + purchQty + " of " + item.getItemName()
			str += item.getItemDesc()
			print "  Purchase qty ", purchQty, " of ", item.getItemName(),
			print " ", item.getItemDesc()
			countItemsToPurchase += 1

	str += "\n"
	str += "Purchase of " + countItemsToPurchase.__repr__() + "item(s) required to fill Sales Orders and Maintain RO point"
	print "Purchase of ", countItemsToPurchase, "item(s) required to fill Sales Orders and Maintain RO point"

	str += "\n\nExpedite of item(s) on Purchase Orders required to build Sales Orders:"
	print "\nExpedite of item(s) on Purchase Orders required to build Sales Orders:"
	countItemsToExpedite = 0
	for item in items:
		if item.getExpediteQty() > -0.0:
			expediteQty = item.getExpediteQty().__repr__()
			str +="\n  expedite qty " + expediteQty + " of " + item.getItemName() + item.getItemDesc()
			print "  expedite qty ", expediteQty, " of ", item.getItemName(),
			print " ", item.getItemDesc()
			countItemsToExpedite += 1
	str += "\nExpedite of " + countItemsToExpedite.__repr__() + "item(s) is required;  These items are on Purchase orders and the quantity listed above must be received prior to build of Sales Orders." 
	print "Expedite of ", countItemsToExpedite, "item(s) is required;  These items are on Purchase orders and the quantity listed above must be received prior to build of Sales Orders."

	str +=" \n\n Purchase of items(s) required to fill Sales Orders:" 
	print "\nPurchase of item(s) required to fill Sales Orders:"
	countItemsToPurchase = 0
	for item in items:
		if item.getPurchase1() > -0.0:
			purchQty = item.getPurchase1().__repr__()
			print "\n Purchase qty ", purchQty, " of ", item.getItemName(),
			print " ", item.getItemDesc()
			str += "/n Purchase qty " + purchQty + " of " 
			str += item.getItemName() + " " + item.getItemDesc()
			countItemsToPurchase += 1
	print "Purchase of ", countItemsToPurchase, "item(s) is required to build open Sales Orders.  "
	str += "Purchase of " + countItemsToPurchase.__repr__() + " item(s) is required to build open sales Orders."

	print "\nOpen purchase orders exist for the following items:"
	str += "\n\nOpen purchase orders exist for the following items:"
	countItemsPurchased = 0
	for item in items:
		if item.getTotPO() > 0.01:
			purchQty = item.getTotPO().__repr__()
			print "  Purchased qty ", purchQty, " of ", item.getItemName(),
			print " ", item.getItemDesc()
			str += "\n  Purchased qty " + purchQty + " of "
			str += item.getItemName() + " "
			str += item.getItemDesc()
			countItemsPurchased += 1
	print "Receipt of", countItemsPurchased, " item(s) is expected; these items have been purchased"
	str += "\nReceipt of " + countItemsPurchased.__repr__() + " item(s) is expected"
	str += " these items have been purchased."

	print "\nThe following items have negative quantities:"
	str += "\n\n The following items have negative quantities:"
	countItemsToBuild = 0
	for item in items:
		if item.getTotOH() <=-.01:
			buildQty = item.getTotOH().__repr__()
			print "  Build qty ", buildQty, " of ", item.getItemName() + " (" + item.getItemDesc() + ")"
			str += "\n  Build qty" + buildQty + " of "
			str += item.getItemName() + " ("
			str += item.getItemDesc() + ")."
			countItemsToBuild += 1
	print "QB inventory adjust or logical build could correct negative counts of:", countItemsToBuild, "item(s)."
	str += "\nQB inventory adjust or logical build could correct"
	str += " negative counts of " + countItemsToBuild.__repr__() + " item(s)\n"		

	with open(purchaseguidanceLocation, "w") as text_file:
		text_file.write(str)