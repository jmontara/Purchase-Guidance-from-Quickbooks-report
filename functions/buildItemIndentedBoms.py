# buildItemIndentedBoms


import classes.indentedBom


def buildItemIndentedBoms(items):
	"""
	builds Indented bills of materials for each item
	in items list, and updates the item accordingly.

	Inputs:
	items 	- 	list, list of item objects
	"""

	for item in items:
		itemName = item.getItemName()
		buildItemIndentedBom(asyName=itemName,
							 asyQty='1',
							 items=items,
							 level ="")


def buildItemIndentedBom(asyName, asyQty, items, level):
	"""
	Gives a indented lists of BOMs, which display the
	assembly and every part and quantity of each lower
	level of assembly.

	Inputs:
	asyName	- str, name of assembly
	asyQty	- str, quantity of assembly for which to construct BOM
	boms	- list, list of all BOM objects
	level 	- str, indicates level of indentation of asyName

	Outputs:
	all		- list, list of (qty, level, item, description)
			  including quantity, level, itemName , and itemDesc 
			  of the item and every item in the asy.

	"""

	def getIbom(asyName='BP-2000-MP-4', asyQty='1',
				   items=items, level=''):
		"""
		helper function.

		iBom	- list, list of (qty, level, item, description)
		  including each quantity, level, item, and description
		  of every item in the asyName.
		"""
		global allInIndentedBom 

		for item in items:
			if item.getItemName() == asyName:
				asyDesc = item.getItemDesc()
				break
		
		allInIndentedBom += [(asyQty, level, asyName, asyDesc)]
		
		# base case of recursive calls
		# return when asyName does not match an item that is an assembly
		asyDesc = None
		for item in items:
			itemCreatingTransaction = item.getItemCreatingTransaction()
			if itemCreatingTransaction == None:
				continue
			itemName = itemCreatingTransaction.getItemName()
			itemDesc = itemCreatingTransaction.getItemDesc()
			if asyName == itemName:
				asyDesc = itemDesc
				thisBomContent = item.getBom().getSorted_tuples()
				break
		if asyDesc == None:
			asyDesc = "item description goes here"
			L = [(asyQty, level, asyName, asyDesc)]
			return L

		else: 
			T =(asyQty, level, asyName, asyDesc)
			level += "."
			# for each item 
			for item in thisBomContent:
				itemQty = str(float(item[0]) * float(asyQty))
				itemName = item[2]
				itemDesc = item[3]
				# recursively call to find the base case		
				L = getIbom(itemName, itemQty, 
									  items, level)
				# if the base case is not found
				if L == None:
					print "error: found no base case in buildItemIndentedBom"
					assert False
				else:
					# print "\nreturn from base case with L:	 ", L
					L = [T] + L
					
				# after reaching the base case and prepending any tuples
			return L

	# print "\n\nentering function:", asyName, asyQty, items, level
	global allInIndentedBom
	allInIndentedBom =[]
	getIbom(asyName, asyQty, items, level)
	# copy of global
	ret = allInIndentedBom[:]
	# print "\n\nret:", ret
	
	indentedBom = classes.indentedBom.IndentedBom()
	for item in items:
		if item.getItemName() == asyName:
			for indentedItem in ret:
				indentedBom.addItem(indentedItem)
			item.setIndentedBom(indentedBom)
	return ret

# asyName='BP-2000-MP-4'	
# print "\nbuildItemIndentedBom(*,*,*,..):"
# buildItemIndentedBom(asyName='BP-2000-MP-4', asyQty='2', 
					# items=items, level='')				   
# for item in items:
	# if item.getItemName() == asyName:
		# print item.getIbom()