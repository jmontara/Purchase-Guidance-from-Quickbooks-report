# buildItemBoms.py

import classes.bom

def buildItemBoms(trans, items):
	"""
	Reads list of transactions and items.  Updates items with
	a bill of materials.

	Inputs:
	trans		- list, list of Transaction objects
	items		- list, list of Item objects

	"""
	for item in items:

		itemCreatingTransaction = item.getItemCreatingTransaction()
		# skip item if not an assembly
		if itemCreatingTransaction == None:
			continue


		itemName = itemCreatingTransaction.getItemName()
		transNum = itemCreatingTransaction.getTnum()
		transQty = itemCreatingTransaction.getQty()
		itemName = itemCreatingTransaction.getItemDesc()
		bom = classes.bom.Bom(itemName, itemName, transNum)		
		level = "."
		for t in trans:
			# disregard unless a build
			if not t.getType() == "Build Assembly":
				continue
			# disregard unless lower asy
			if not float(t.getQty()) < 0:
				continue
			if t.getTnum() == transNum:
				itemQty = float(t.getQty())/float(transQty)
				itemQty = str(itemQty)[:5]
				bom.addItem(t.getItemName(), t.getItemDesc(), 
							itemQty, level)	
		item.setBom(bom)
