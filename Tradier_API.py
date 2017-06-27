import json
import csv
import requests
import os
from pprint import pprint


def pullData_buildCSV (getStock, getType, getStartDate):

    tradierResponse = get_tradier_data(getStock, getType, getStartDate)  # go to tradier to get data
    tradierDict = convert_response_to_dict(tradierResponse)  # prepare date for csv writing
    pprint ("these symbols were unmmatched " + str(tradierDict['quotes']['unmatched_symbols']['symbol']))
    send_to_csv(tradierDict, getType, getStock)  # write date into csv

    return

def get_tradier_data(stockSymbol,
                     infoType,
                     startDate):  # Request: Market Quotes (https://sandbox.tradier.com/v1/markets/quotes?symbols=spy)

    # get API key from local text file
    with open("API_Key.txt", "r") as mykey:
        apiKey = mykey.read()

    # Headers
    headers = {"Accept": "application/json",
               "Authorization": "Bearer " + apiKey}

    # pull todays quote information
    if (infoType == 'quote'):
        try:
            stockData = requests.get('https://sandbox.tradier.com/v1/markets/quotes?symbols=' + stockSymbol,
                                     headers=headers)
        except ValueError:
            print('there was a problem getting the stock information')


    # pull historical information
    elif (infoType == 'hist'):
        try:
            stockData = requests.get(
                'https://sandbox.tradier.com/v1/markets/history?symbol=' + stockSymbol + '&start=' + startDate,
                headers=headers)
        except ValueError:
            print('there was a problem getting the stock information')

    else:
        print('no selection made')

    return stockData


def convert_response_to_dict(stockData):  # converts request response to dictionary

    try:
        stock_str = stockData.text  # convert response to string
        stock_dic = json.loads(stock_str)  # convert string to dictionary

    except ValueError:
        print('uh-oh, there was a problem')

    return stock_dic


def send_to_csv(stock_dic, infoType, stockSymbol):  # write quote data to csv
    with open("OutputFileURL.txt", "r") as myUrl:
        outputURL = myUrl.read()

        #pprint (stock_dic)

    if (infoType == 'quote'):
        with open(outputURL + 'quote_raw.csv', 'w',
                  newline='') as f:  # Just use 'w' mode in 3.x
            w = csv.DictWriter(f, stock_dic['quotes']['quote'][0].keys())
            w.writeheader()
            w.writerows(stock_dic['quotes']['quote'])

        reorderQuoteColumns(stockSymbol)

    elif (infoType == 'hist'):
        with open(outputURL + stockSymbol + '_hist_raw.csv', 'w',
                  newline='') as f:  # Just use 'w' mode in 3.x

            # write column headers into csv
            current = 0
            w = csv.DictWriter(f, stock_dic['history']['day'][current])
            w.writeheader()

            # iterate through historical data and populate csv
            while current < len(stock_dic['history']['day']):
                w = csv.DictWriter(f, stock_dic['history']['day'][current])
                w.writerow(stock_dic['history']['day'][current])
                current += 1

        reorderHistColumns(getStock)

    else:
        print('there seems to be a problem, goodbye')

    return


def reorderHistColumns(stockSymbol):  # puts historical output into proper column order
    with open("OutputFileURL.txt", "r") as myUrl:
        outputURL = myUrl.read()

    with open(outputURL + stockSymbol + '_hist_raw.csv', 'r') as infile, \
            open(outputURL + stockSymbol + '_hist.csv', 'w', newline='') as outfile:
        # output dict needs a list for new column ordering
        fieldnames = ['date', 'open', 'high', 'low', 'close', 'volume']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        # reorder the header first
        writer.writeheader()

        for row in csv.DictReader(infile):
            writer.writerow(row)  # writes the reordered rows to the new file

    # delete the unformated csv file
    os.remove(outputURL + stockSymbol + '_hist_raw.csv')

    print('csv created')


def reorderQuoteColumns(stockSymbol):  # puts quote output into proper column order
    with open("OutputFileURL.txt", "r") as myUrl:
        outputURL = myUrl.read()

    with open(outputURL + 'quote_raw.csv', 'r') as infile, \
            open(outputURL + 'quote.csv', 'w', newline='') as outfile:


        # output dict needs a list for new column ordering
        fieldnames = ['trade_date', 'symbol', 'close', 'prevclose', 'open', 'low', 'high', 'change',
                      'change_percentage', \
                      'week_52_low', 'week_52_high', 'volume', 'last_volume', 'average_volume', 'bid', 'bid_date', \
                      'asksize', 'ask_date', 'ask', 'bidexch', 'description', 'type', 'bidsize', 'exch', 'root_symbols',
                      'askexch', 'last']

        keep_rows = ['symbol', 'close', 'prevclose', 'open', 'low', 'high', 'change', 'change_percentage', \
                     'week_52_low', 'week_52_high', 'volume', 'last_volume', 'average_volume', 'trade_date']

        writer = csv.DictWriter(outfile, fieldnames=keep_rows, extrasaction='ignore')

        # reorder the header first
        writer.writeheader()

        for row in csv.DictReader(infile):
            writer.writerow(row)  # writes the reordered rows to the new file

    # delete the raw (unformatted) csv file
    os.remove(outputURL + 'quote_raw.csv')

    print('csv created')

if __name__ == "__main__":

    # global variables
    getStartDate = None

    # question the user for input

    getType = input('please enter \'quote\' or \'hist\' for data type desired ')

    if (getType == 'hist'):
        getStock = input(
            'please enter stock symbol you desire to get, (only enter one symbol for historical data) ')
        getStartDate = input('please input your start date in the format YYYY-MM-DD ')
        pullData_buildCSV(getStock, getType, getStartDate)

    elif (getType == 'quote'):
        getStock = input(
            'please enter stock symbol you desire to get, separate each ticker by a comma ')
        pullData_buildCSV(getStock, getType, getStartDate)

    else:
        print('invalid input...goodbye')


# i could use this as input into a spreadsheet that tracks my portfolio daily
# i should put these data points into a database
