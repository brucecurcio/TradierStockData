import json
import csv
import requests
import os

def get_tradier_data(stockSymbol,
                     infoType, startDate):  # Request: Market Quotes (https://sandbox.tradier.com/v1/markets/quotes?symbols=spy)

    #get API key from local text file
    with open("API_Key.txt", "r") as mykey:
        apiKey = mykey.read()

    # Headers
    headers = {"Accept": "application/json",
               "Authorization": "Bearer " + apiKey}

    # pull todays quote information
    if (infoType == 'quote'):
        try:
            stockData = requests.get('https://sandbox.tradier.com/v1/markets/quotes?symbols=' + stockSymbol, headers=headers)
        except ValueError:
            print ('there was a problem getting the stock information')


    # pull historical information
    elif (infoType == 'hist'):
        try:
            stockData = requests.get('https://sandbox.tradier.com/v1/markets/history?symbol=' + stockSymbol + '&start=' + startDate,headers=headers)
        except ValueError:
            print ('there was a problem getting the stock information')

    else:
        print('no selection made')

    return stockData


def convert_response_to_dict(stockData):  # converts request response to dictionary

    try:
        stock_str = stockData.text  # convert response to string
        stock_dic = json.loads(stock_str)  # convert string to dictionary
    except ValueError:
        print ('uh-oh, there was a problem')

    return stock_dic


def send_to_csv(stock_dic, infoType, stockSymbol):  # write quote data to csv

    if (infoType == 'quote'):
        with open(outputURL + stockSymbol + '_quote.csv', 'w',
                  newline='') as f:  # Just use 'w' mode in 3.x
            w = csv.DictWriter(f, stock_dic['quotes']['quote'].keys())
            w.writeheader()
            w.writerow(stock_dic['quotes']['quote'])
        print('csv created')

    elif (infoType == 'hist'):
        with open(outputURL + stockSymbol + '_hist_raw.csv', 'w',
                  newline='') as f:  # Just use 'w' mode in 3.x

            #write column headers into csv
            current = 0
            w = csv.DictWriter(f, stock_dic['history']['day'][current])
            w.writeheader()

            #iterate through historical data and populate csv
            while current < len(stock_dic['history']['day']):
                w = csv.DictWriter(f, stock_dic['history']['day'][current])
                w.writerow(stock_dic['history']['day'][current])
                current += 1

    else:
        print('there seems to be a problem, goodbye')

    return

def reorderColumns(stockSymbol): # puts historical output into proper column order
    with open(outputURL + stockSymbol + '_hist_raw.csv', 'r') as infile, \
            open(outputURL + stockSymbol + '_hist.csv', 'w', newline='') as outfile:

        # output dict needs a list for new column ordering
        fieldnames = ['date', 'open', 'high', 'low', 'close', 'volume']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        # reorder the header first
        writer.writeheader()

        for row in csv.DictReader(infile):
            writer.writerow(row) # writes the reordered rows to the new file

    #delete the unformated csv file
    os.remove(outputURL + stockSymbol + '_hist_raw.csv')

    print('csv created')

#global variables
with open("OutputFileURL.txt", "r") as myUrl:
    outputURL = myUrl.read()
getStartDate = None

#question the user for input

getStock = input('please enter stock symbol you desire to get ')
getType = input('please enter \'quote\' or \'hist\' for data type desired ')
if (getType == 'hist'):
    getStartDate = input ('please input your start date in the format YYYY-MM-DD ')

if (getType == 'quote' or getType == 'hist'):
    tradierResponse = get_tradier_data(getStock, getType, getStartDate)  # go to tradier to get data
    tradierDict = convert_response_to_dict(tradierResponse) #prepare date for csv writing
    send_to_csv(tradierDict, getType, getStock) #write date into csv
    if (getType == 'hist'):
        reorderColumns(getStock)
else:
    print('invalid input...goodbye')

#clean up columns for quote data, also code in the ability to pull quotes for multiple stocks at once
#i could use this as input into a spreadsheet that tracks my portfolio daily
# i should put these data points into a database
