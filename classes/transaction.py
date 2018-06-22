# filename:  transaction.py


class Transaction(object):
	def __init__(self, item, desc, tNum, type, dte,
				 num, qty, soNum, name, memo, soDte=None):
		self.itemName = item
		self.desc = desc
		self.tNum = tNum
		self.type = type
		self.date = dte
		self.num = num
		self.qty = qty
		self.name = name
		self.memo = memo
		# replace qty = "" with "0"
		# qty = "" is observed in QB csv lines that include "purchase order"
		if qty =="":
			self.qty = "0"
		self.soNum = soNum
		self.invoiceSaleDate = soDte
		# check if qb provides link from invoice to sales order
		try:
			if type == "Invoice":
				assert not soNum == ""
		except:
			# print "\nwarning Invoice has no S.O. in available data for:"
			# print self
			pass
	def getSoNum(self):
		return self.soNum
	def getItemName(self):
		return self.itemName
	def getItemDesc(self):
		return self.desc
	def getTnum(self):
		return self.tNum
	def getType(self):
		return self.type
	def getQty(self):
		return self.qty
	def getInvoiceSoNum(self):
		return self.soNum
	def setInvoiceSaleDate(self,date):
		# assert type(date) == datetime
		self.invoiceSaleDate = date
	def getInvoiceSaleDate(self):
		return self.invoiceSaleDate
	def getDate(self):
		return self.date
	def getNum(self):
		return self.num
	def getName(self):
		return self.name
	def getMemo(self):
		return self.memo
	def getShortStr(self):
		"""returns truncated data useful when printing Item objects"""
		ret = " <xaction:  " + self.itemName[:20] + ", "
		# ret += " Desc: "
		ret +=  self.desc[:20] + ", "
		# ret += " Xaction #: "
		ret +=  self.tNum + ", "
		# ret += " Type #: "
		ret += self.type + ", "
		# ret += " Date: "
		ret += self.date.__str__() + ", "
		# ret += " Num: "
		ret += self.num + ", "
		# ret += " Qty: "
		ret += self.qty + ", "
		# ret += " Invoice's S.O #: "
		ret += self.soNum + ", "
		ret += self.name + ", "
		ret += self.memo + ">\n"
		return ret
	def __str__(self):
		ret = "<Transaction:  " + self.itemName + "\n "
		ret += " Desc: " 		+ self.desc + "\n "
		ret += " Xaction #: " 	+ self.tNum + "\n "
		ret += " Type #: " 		+ self.type + "\n "
		ret += " Date: " 		+ self.date.__str__() + "\n "
		ret += " Num: "			+ self.num + "\n "
		ret += " Qty: " 		+ self.qty + "\n "
		ret += " Invoice's S.O #: " + self.soNum + "\n "
		ret += " Invoice's Sale Date " + self.invoiceSaleDate.__str__() + ">\n "
		ret += " Xaction Name: " + self.name + "\n "
		ret += " Xaction Memo:"  + self.memo 
		return ret

if __name__ == "__main__":

	import datetime
	dte = datetime.date(2018,6,12)
	t = Transaction("item", "desc", "tNum", "type", dte, "num","qty,","soNum", "name", "memo", "soDte")
	print t

	
	
	
	
	
	
	
	
	