"""
                                Robinhood Trading Journal 

        All this method requires to login in your robinhood account and once you create robinhood object that object 
            is passed to method, hence self is that object in all the below methods 

Defined methods on Robinhood class

 'basicInstrumentSchema',
 'downloadPdf',
 'get_account',
 'get_dividends',
 'get_documentsInfo',
 'get_instrumentBasic',
 'get_instruments',
 'get_markets',
 'get_optionsInstrument',
 'get_optionsOrders',
 'get_optionsPositions',
 'get_orders',
 'get_portfolios',
 'get_positions',
 'get_quotes',
 'get_url',
 'get_user',
 'headers',
 'instrumentBasic',
 'instrumentObject',
 'instrumentsList',
 'login',
 'logout',
 'options_owned',
 'positions_owned',
"""


import pandas as pd
import numpy as np
import yfinance as yf


#Methods Portfolio
####### Getting stock portfolio dataframe visulaization
def stocksPortfolioDataframe(self):
    portfolio = pd.DataFrame(self.positions_owned())[["instrument","average_buy_price","quantity","updated_at"]]
    portfolio = self.get_instrumentBasic(portfolio['instrument'].tolist()).set_index('url').join(
                                                        portfolio.set_index('instrument')).reset_index()
    portfolio = portfolio[['market','updated_at','name','symbol','quote_time','quote','average_buy_price','quantity']]
    portfolio["quote"] = portfolio["quote"].astype(float)
    portfolio["average_buy_price"] = portfolio["average_buy_price"].astype(float)
    portfolio["quantity"] = portfolio["quantity"].astype(float)
    portfolio["unrealized_gain"] =  (portfolio.quote - portfolio.average_buy_price)*portfolio.quantity
    portfolio["Total Investment"] = portfolio.average_buy_price*portfolio.quantity
    return portfolio


def optionsPortfolioDataFrame(self):
    x = self.options_owned()
    for i in x:
        i.update(self.get_optionsObject(i["option"]))
    x = pd.DataFrame(x)
    x["average_buy_price"] = x['average_price'].astype(float)
    x["quantity"] = x['quantity'].astype(float)
    x["strikePrice"] = x['strikePrice'].astype(float)
    x = x[['updated_at','chain_symbol','optionName',"average_buy_price",'quantity','strikePrice', 'optionType', 'expDate','state' , 'type']]
    x['Total Investment'] = x.average_buy_price * x.quantity
    return x

#Getting orders
def pendingOrders(self):
    orders = self.get_orders()
    orders = pd.DataFrame(orders)
    orders = orders.rename(columns={"type":"orderType","state":"orderState","id":"orderId"})
    pending_orders = orders[orders.orderState =='confirmed'][['orderId','orderState','side','instrument','price','quantity', 'fees', 'orderType','last_transaction_at','executions']]
    pending_orders = self.get_instrumentBasic(pending_orders['instrument'].tolist())[['market','name','symbol','instrumentType','url']].set_index('url').join(pending_orders.set_index('instrument')).reset_index(drop = True)
    return pending_orders[['orderId',  'name','orderState','orderType','side', 'symbol','price', 'quantity', 'market',  'instrumentType','fees', 'last_transaction_at', 'executions']]


#stocks Order book method
def ordersDataFrame(self):
    orders = self.get_orders()
    orders = pd.DataFrame(orders)
    orders = orders[orders.executions.apply(lambda i: len(i) >0 )]
    orders = orders.rename(columns={"type":"orderType","state":"orderState","id":"orderId"})
    orders = self.get_instrumentBasic(orders.instrument.tolist()).set_index('url').join(orders[['orderId', 'instrument', 'fees', 'orderType', 'side','executions']].set_index('instrument'))
    orders = orders[['orderId', 'name','orderType','side', 'symbol', 'market',  'instrumentType', 'fees', 'executions']].reset_index(drop = True)
    exe_df = []
    for i in orders.itertuples():
        item = {'orderId':i.orderId, 'name':i.name,'orderType':i.orderType,'side':i.side, 'symbol':i.symbol, 'market':i.market,  'instrumentType':i.instrumentType }
        for j in i.executions:
            j.update(item)
            j["fees"] = float(i.fees)/len(i.executions)
            exe_df.append(j)

    exe_df = pd.DataFrame(exe_df)[['id', 'orderId','settlement_date', 'timestamp','market','name','symbol', 'instrumentType','orderType', 'side', 'fees', 'price', 'quantity']]
    exe_df = exe_df.rename(columns = {'id':'transactionId'})
    exe_df["price"] = exe_df["price"].astype(float)
    exe_df["quantity"] = exe_df["quantity"].astype(float)
    exe_df['timestamp'] = pd.to_datetime(exe_df['timestamp'])
    exe_df = exe_df.sort_values(by = ["timestamp"],ascending=False)
    return exe_df



def orderJournal(df): #Takes in  oerderBook dataframe to calculate gains, can also take in orderDataFrame(rh)
    returnList = []
    temp = df.copy().groupby(["side"])
    buy = temp.get_group("buy")
    sell = temp.get_group("sell")
    for i in sell.groupby(["symbol"]):
        stock = i[0]
        temp_sell = i[1].sort_values(by = ["timestamp"])
        name = temp_sell["name"].iloc[0]
        temp_buy = buy[buy.symbol == stock].sort_values(by = ["timestamp"],ascending=False)
        
        if temp_buy.empty: 
            print("Symbol : %s, %s has no buys backing up SELL transaction. It may be because of stock merger or portfolio was transfered from another institution" 
                      %(stock,name))
            continue 
        try:
            try: 
                splits = yf.Ticker(stock).splits
            except : 
                splits = None 
            stocks_splited = []
            buystack = temp_buy[["quantity","price","timestamp"]].values.tolist()
            for j in temp_sell.itertuples():
                avgPrice = {"qty":[],"price" : []}
                item = {"timestamp":j.timestamp,"market":j.market,"stock":stock,"stockName":name,"fees":j.fees,"sellQty" : j.quantity,"sellPrice":j.price}
                leftqty = j.quantity
                
                while leftqty >0:
                    leftqty = round(leftqty,6)
                    buy_pop = buystack.pop()
                    #This try block should account for splits situation in your trading history
                    try: #Checks for wether needs to account for splits
                        d = buy_pop[2]
                        if (d.date() not in stocks_splited) and (splits is not None):
                            splits_keys = splits.keys()[[y.date() < j.timestamp.date() for y in splits.keys()]]
                            splits_keys = splits_keys[[ d.date() < x.date() for x in splits_keys]]
                            loop = False
                            for k in splits_keys:
                                buy_pop[0] *=  splits[k]
                                buy_pop[1] /=  splits[k]
                                loop = True
                            if loop: stocks_splited.append(d.date())
                    except Exception as e:
                        print(e)
                    
                    if leftqty >= buy_pop[0]:
                        avgPrice["qty"].append(buy_pop[0])
                        avgPrice["price"].append(buy_pop[1])
                        leftqty -= buy_pop[0]
                    else:
                        avgPrice["qty"].append(leftqty)
                        avgPrice["price"].append(buy_pop[1])
                        buy_pop[0] -= leftqty
                        buystack.append(buy_pop)
                        leftqty = 0
                item["avgBuyPrice"] = np.average(avgPrice["price"], weights=avgPrice["qty"])
                returnList.append(item)
        except Exception as e:
            print(str(e),stock)
    returnList = pd.DataFrame(returnList).set_index("timestamp")
    returnList["profit_loss/stock"] = returnList["sellPrice"] - returnList["avgBuyPrice"]
    returnList["sellAmount"] = returnList["sellQty"]*returnList["sellPrice"]
    returnList["buyAmount"] = returnList["sellQty"]*returnList["avgBuyPrice"]
    returnList["total_gain"] = returnList["sellAmount"]-returnList["buyAmount"]
    return returnList


#This method is for Option orders history 
def optionOrderDataFrame(self):
    " Working on It"
    pass

def optionOrderJournal(df):
    pass
