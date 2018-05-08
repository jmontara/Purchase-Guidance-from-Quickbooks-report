# setTransactionSaleDate.py

def setTransactionSaleDate(transactions):
	"""
	Updates Transaction objects that are of type "Invoice" 
	with the date of the sales order associated with the invoice.
	
	Returns a list of these updated Transaction objects.
	
	Inputs:
	transactions	- list, list of Transaction objects
	
	Outputs:
	invoiceTransactions = list, list of updated Transaction objects
	"""
		
	salesOrders = {}
	ret = []

	for transaction in transactions:
		if transaction.getType() == "Sales Order":
			salesOrders[transaction.getNum()] = transaction.getDate()

	for transaction in transactions:
		if transaction.getType() == "Invoice":
			try:
				transaction.setInvoiceSaleDate(salesOrders[transaction.getSoNum()])
				ret.append(transaction)
			except:
				print "\nwarning, this invoice transaction has no sales order number in available data"
				print "warning, substituting invoice date as an approximation for sale date"
				print "warning, Doing this puts some sales into a different calendar year. "
				transaction.setInvoiceSaleDate(transaction.getDate())
				print transaction
				ret.append(transaction)
				
	return ret
	