# print(type(stockquote_dic))

# prints the entire json object as a test

# response, content = connection.request('https://sandbox.tradier.com/v1/markets/quotes?symbols=spy', 'GET', headers=headers)
# Success
# print('Response status ' + str(response.status))
#  pprint.pprint(content)
# except httplib2.httplib2error as e:
# Exception
#  print('Exception during request')






# open a file for writing

stock_data = open('C:/Users/brucecurcio/Desktop/Investing/SPY_Data/StockData.csv', 'w')

# create the csv writer object

csvwriter = csv.writer(stock_data)
# print(csvwriter)

count = 0

for stk in stockquote_dic['quotes']['quote']:
    print(stk)
    print(type(stk))
#
#     # if count == 0:
#
#     header = stk.keys()
#
# csvwriter.writerow(header)
#
# # count += 1
#
# # csvwriter.writerow(stk)
#
# stock_data.close()
