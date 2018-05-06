# indentedBom.py

class IndentedBom(object):
	def __init__(self):
		"""
		Inputs:
		self	-	object, IndentedBom object
		"""
		self.items =[]
		
	def addItem(self,T):
		"""
		Inputs:
		T		- tuple, item's variables
				  
		example: 
		T = (itemQty, itemLevel, itemName, itemDesc)
		"""
		self.items.append(T)
		
	def getItems(self):
		return self.items
	
	def __str__(self):
		ret = "-----------------------------------------------\n"
		ret += "Indented Bill of Materials: \n"
		ret += "qty 	level	item	(description  snipped \n"
		ret +="--------------------------------------------------"
		for item in self.items:
			ret += "\n"
			ret += item[0] + " \t"
			ret += item[1] + " "
			ret += item[2] + " ("
			ret += item[3] + " ..."
		ret += "\n\n"
		return ret			

