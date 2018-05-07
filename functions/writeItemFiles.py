# writeItemFiles.py

import csv

def writeItemFiles(items, outDir):
	"""
	Export item indented boms to csv files 	
	Export item.__str__() to file
	
	Inputs:
	items - list, list of item objects
	outDir - str, directory where output files are written
			 assumes this is directory is already created
	
	Outputs:
	files showing indented boms having the name similar to item.getItemName()
	files showing item.__str__()
	
	"""
 
	allowedFileNameChars ="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

	for item in items:

		#if char in outFileName is not allowed, 
		# replace it with _
		# outFileName = ''
		outFileName = '.\itemFiles\\'
		# outFileName = '.\' + outDir + '\\'
		for char in item.getItemName():
			if char in allowedFileNameChars:
				outFileName += char
			else:
				outFileName += '_'
		# outFileName += '.csv'
		outFileName = outFileName + '-ibom.csv'

		with open(outFileName, 'wb') as f:
			csv_writer = csv.writer(f)
			# header row
			qty = "qty"
			level = "level"
			itemName = "itemName"
			itemDesc = "itemDesc"
			csv_writer.writerow([qty, level, itemName, itemDesc]) 
			for indentedItem in item.getIbom().getItems():
				qty = indentedItem[0]
				level = indentedItem[1]
				itemName = indentedItem[2]
				itemDesc = indentedItem[3]
				csv_writer.writerow([qty, level, itemName, itemDesc]) 
		# assert False
		#if char in outFileName is not allowed, 
		# replace it with _
		# outFileName = ''
		outFileName = '.\itemFiles\\'
		# outFileName = '.\' + outDir + '\\'
		for char in item.getItemName():
			if char in allowedFileNameChars:
				outFileName += char
			else:
				outFileName += '_'
		# outFileName += '.csv'
		outFileName = outFileName + '-summary.txt'

		with open(outFileName, "w") as text_file:
			text_file.write(item.__str__())
		# assert False
