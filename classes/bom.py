# bom.py


class Bom(object):
	""" Holds an item and items required to build that item"""
	def __init__(self, asy, desc, tNum = ''):
		"""
		Inputs:
		self	- object, BOM object
		asy		- str, item name
		asyDesc - str, description of item
		tNum 	- str, the transaction number upon which this	
					   BOM is built
		"""
		assert type(asy) == str
		self.asy = asy 
		self.desc = desc
		self.tNum = tNum
		self.items = []
		self.descs = []
		self.qtys = []
		self.levels = [] 
	def getAsyName(self):
		return self.asy
	def getAsyDesc(self):
		return self.desc
	def addItem(self, item, desc, qty, level):
		self.items.append(item)
		self.descs.append(desc)
		self.qtys.append(str(abs(float(qty))))
		self.levels.append(level)
		assert len(self.items) == len(self.descs)
		assert len(self.items) == len(self.qtys)
		assert len(self.items) == len(self.levels)
	def getSorted_tuples(self):
		""" returns a list of tuples sorted by item name
		"""
		bomItem_tuples =[] 
		for row in range(len(self.items)):
			bomItem_tuples.append((
						   self.qtys[row][:6],
						   self.levels[row],
						   self.items[row],
						   self.descs[row][:40]
						   ))
		sortedBomItem_tuples = sorted(bomItem_tuples,
							key=lambda item: item[2]) #sort by item	
		return sortedBomItem_tuples
	def __str__(self):
		ret = "-----------------------------------------------\n"
		# ret += "BOM for: "
		ret += self.asy + " (" + self.desc + ")\n" 
		ret += "\t\t\t\t\t(built from Transaction #" + self.tNum +")\n"
		ret += "Qty \t level item \t description\n"
		ret +="--------------------------------------------------"
		
		# 
		sortedBomItem_tuples = self.getSorted_tuples() 
		# for row in range(len(self.items)):
			# bomItem_tuples.append((
						   # self.qtys[row][:6],
						   # self.levels[row],
						   # self.items[row],
						   # self.descs[row][:40]
						   # ))
		# sortedBomItem_tuples = sorted(bomItem_tuples,
							# key=lambda item: item[2]) #sort by item	
		
		for row in range(len(self.items)):
			ret += "\n"
			ret += sortedBomItem_tuples[row][0] + " \t"
			ret += sortedBomItem_tuples[row][1] + " "
			ret += sortedBomItem_tuples[row][2] + " ("
			ret += sortedBomItem_tuples[row][3] + " ..."
		ret += "\n\n"
		return ret	
	