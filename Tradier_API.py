import json
import csv
import requests

def get_tradier_data(stockSymbol,
                     infoType):  # Request: Market Quotes (https://sandbox.tradier.com/v1/markets/quotes?symbols=spy)

    # Headers
    headers = {"Accept": "application/json",
               "Authorization": "Bearer GbWVxb79dSCbEgiLprUUqNAAJhbG"}

    # pull todays quote information
    if (infoType == 'quote'):
        try:
            stockData = requests.get('https://sandbox.tradier.com/v1/markets/quotes?symbols=' + stockSymbol, headers=headers)
        except ValueError:
            print ('there was a problem getting the stock information')


    # pull historical information
    elif (infoType == 'history'):
        try:
            stockData = requests.get('https://sandbox.tradier.com/v1/markets/history?symbol=' + stockSymbol,headers=headers)
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
        with open('C:/Users/brucecurcio/Desktop/Investing/SPY_Data/' + stockSymbol + '.csv', 'w',
                  newline='') as f:  # Just use 'w' mode in 3.x
            w = csv.DictWriter(f, stock_dic['quotes']['quote'].keys())
            w.writeheader()
            w.writerow(stock_dic['quotes']['quote'])
        print('csv created')

    elif (infoType == 'historical'):
        with open('C:/Users/brucecurcio/Desktop/Investing/SPY_Data/SPY_Data.csv', 'w',
                  newline='') as f:  # Just use 'w' mode in 3.x
            w = csv.DictWriter(f, stock_dic['history']['day'].keys())
            w.writeheader()
            w.writerow(stock_dic['history']['day'])
        print('csv created')

    else:
        print('there seems to be a problem, goodbye')

    return

#question the user for input
getStock = input('please enter stock symbol you desire to get ')
getType = input('please enter \'quote\' or \'historical\' for data type desired ')

if (getType == 'quote' or getType == 'historical'):
    tradierResponse = get_tradier_data(getStock, getType)  # go to tradier to get data
    tradierDict = convert_response_to_dict(tradierResponse) #prepare date for csv writing
    send_to_csv(tradierDict, getType, getStock) #write date into csv
else:
    print('invalid input...goodbye')




# fieldname list to be used if resolve how to filter headers in python dictionary for quote pull
# fieldnames = ['trade_date', 'last', 'open', 'change_percentage', 'ask', 'description', 'close', 'average_volume',
#                  'low', 'change', 'week_52_high', 'symbol', 'volume', 'last_volume', 'prevclose', 'high', 'week_52_low']
