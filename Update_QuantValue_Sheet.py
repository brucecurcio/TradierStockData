import json
import csv
import requests
import os
from pprint import pprint
import xlrd
from Tradier_API import pullData_buildCSV

with open("C:/Users/brucecurcio/Documents/GitHub/TradierAPI/SpreadSheetLocation.txt", "r") as myUrl:
    localURL = myUrl.read()

# open the workbook
xl_workbook = xlrd.open_workbook(localURL + "QuantValue_Practice.xlsx")

#pull the Live portfolio tab
xl_sheet = xl_workbook.sheet_by_name("Live Portfolio")

stockList = []
i = 1

# get all the stock symbols in the sheet
while xl_sheet.cell(i,0).value != "":
    stockList.append((xl_sheet.cell(i,0).value))
    i += 1

stockListString = str(stockList)
stockListString = stockListString.replace(" ", "") # prep string for Tradier, remove spaces
stockListString = stockListString.replace("'", "") # prep string for Tradier, remove quotes
#print (stockListString)

pullData_buildCSV (stockListString, 'quote', None)

# build a check for empty cells in the close column, tradier flushes the close,low and high values before the market opens.  If the data has been flushed
#refer to the previous close value, this is where the closing price has been moved to.
#next step is to update QuantValue spreadsheet with current stock prices on Live Portfolio tab, then move over to virtual portfolio tabs