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
import os, shutil, sys
from Robinhood_Base import Robinhood
#Methods Portfolio
####### Getting stock portfolio 
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

#Getting Options Portfolio
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

#Getting Pending Orders
def pendingOrders(self): 
    orders = self.get_orders() 
    orders = pd.DataFrame(orders) 
    orders = orders.rename(columns={"type":"orderType","state":"orderState","id":"orderId"}) 
    pending_orders = orders[orders.orderState =='confirmed'][['orderId','orderState','side','instrument','price','quantity', 'fees', 'orderType','last_transaction_at','executions']] 
    if len(pending_orders) == 0:
        return False
    else:
        pending_orders = self.get_instrumentBasic(pending_orders['instrument'].tolist())[['market','name','symbol','instrumentType','url']].set_index('url').join(pending_orders.set_index('instrument')).reset_index(drop = True) 
        return pending_orders[['orderId', 'name','orderState','orderType','side', 'symbol','price', 'quantity', 'market', 'instrumentType','fees', 'last_transaction_at', 'executions']]

#Stocks Order book method
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

    exe_df = pd.DataFrame(exe_df)[['timestamp','settlement_date', 'orderId', 'id','market','name','symbol', 'instrumentType','orderType', 'fees', 'price', 'quantity', 'side']]
    exe_df = exe_df.rename(columns = {'id':'transactionId'})
    exe_df["price"] = exe_df["price"].astype(float)
    exe_df["quantity"] = exe_df["quantity"].astype(float)
    exe_df['timestamp'] = pd.to_datetime(exe_df['timestamp'])
    exe_df = exe_df.sort_values(by = ["timestamp"],ascending=False)
    return exe_df


#Stocks Journal
def ordersJournal(df): #Takes in  oerderBook dataframe to calculate gains, can also take in orderDataFrame(rh)
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
            print("Symbol : %s, %s has no buys backing up SELL transaction. It may be because of option excercised, stock merger or portfolio was transfered from another institution \n" 
                      %(stock,name))
            continue 
        try:
            try: 
                splits = yf.Ticker(stock).splits
                if type(splits) is list:
                    splits = None
                    print(f"If this stocks - {stock} was split, there is no data provided by library, hence this method will be not able to identify splits and will not account for So!")
                    print(f"There might be chance of wrong calculation in stocks_journal regarding this stock - {stock} \n")
            except : 
                splits = None 
            stocks_splited = []
            buystack = temp_buy[["quantity","price","timestamp"]].values.tolist()
            for j in temp_sell.itertuples():
                avgPrice = {"qty":[],"price" : []}
                item = {"timestamp":j.timestamp,"market":j.market,"symbol":stock,"stockName":name,"fees":j.fees,"sellQty" : j.quantity,"sellPrice":j.price}
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
                        print(f"Error in ordersJournal inner loop : {e} \n")
                    
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
            print(f"Error in ordersJournal outer loop : {e} stock \n")
    returnList = pd.DataFrame(returnList)
    returnList["profit_loss/stock"] = returnList["sellPrice"] - returnList["avgBuyPrice"]
    returnList["sellAmount"] = returnList["sellQty"]*returnList["sellPrice"]
    returnList["buyAmount"] = returnList["sellQty"]*returnList["avgBuyPrice"]
    returnList["total_gain"] = returnList["sellAmount"]-returnList["buyAmount"]
    return returnList.sort_values(by = ["timestamp"],ascending=False)


#This method is for Option orders history 
def optionsOrderDataFrame(self):
    optionsOrders =  self.get_optionsOrders()
    optionsOrders = pd.DataFrame(optionsOrders)
    #can get pending options orders
    #pendingOrders = optionsOrders[optionsOrders.pending_quantity.apply(lambda i: float(i)>0)].copy()
    
    optionsOrders = optionsOrders[optionsOrders.legs.apply(lambda i: len(i[0]['executions'])>0)][["chain_symbol","opening_strategy","closing_strategy","legs","direction"]]
    exe_df = []
    for i in optionsOrders.itertuples():
        item = {'orderId':i.legs[0]["id"], 'symbol':i.chain_symbol, 'opening_strategy':i.opening_strategy, 'closing_strategy':i.closing_strategy,'side':i.legs[0]["side"] }
        item.update(self.get_optionsObject(i.legs[0]['option']))
        for j in i.legs[0]["executions"]:
            j.update(item)
            exe_df.append(j)
    exe_df = pd.DataFrame(exe_df)[['timestamp','settlement_date', 'orderId','id','symbol', 'optionName','optionType', 'price', 'quantity', 'side', 'opening_strategy', 'closing_strategy']]
    exe_df = exe_df.rename(columns = {'id':'transactionId','price':'pricePerContract'})
    exe_df["pricePerContract"] = exe_df["pricePerContract"].astype(float)*100
    exe_df["quantity"] = exe_df["quantity"].astype(float)
    exe_df['timestamp'] = pd.to_datetime(exe_df['timestamp'])
    exe_df = exe_df.sort_values(by = ["timestamp"],ascending=False)
    return exe_df

#Options Journal
def optionsOrderJournal(df): #Takes in  optionOrderBook dataframe to calculate gains, can also take in orderDataFrame(rh)
    returnList = []
    temp = df.copy().groupby(["side"])
    buy = temp.get_group("buy")
    sell = temp.get_group("sell")
    for i in set(buy.optionName)-set(sell.optionName):
        for j in buy[buy.optionName == i].itertuples():
            item1 = {"timestamp":j.timestamp,"symbol":j.symbol,"optionName":j.optionName,
                    "optionType":j.optionType,"sellQty" : j.quantity, "sellPrice":0, "avgBuyPrice": j.pricePerContract}
            returnList.append(item1)
    for i in sell.groupby(["optionName"]):
        name = i[0]
        temp_sell = i[1].sort_values(by = ["timestamp"])
        stock = temp_sell["symbol"].iloc[0]
        temp_buy = buy[buy.optionName == name].sort_values(by = ["timestamp"],ascending=False)
        
        if temp_buy.empty: 
            print("Option : %s has no buys backing up SELL transaction. It may be because of covered call/put, stock merger or portfolio was transfered from another institution \n"  %(name))
            continue 
        try:
            try:
                splits = yf.Ticker(stock).splits
                if type(splits) is list:
                    splits = None
                    print(f"If this stocks - {stock} was split, there is no data provided by library, hence this method will be not able to identify splits and will not account for So!")
                    print(f"There might be chance of wrong calculation in options_journal regarding this stock - {stock} \n")
            except : 
                splits = None 
            stocks_splited = []
            buystack = temp_buy[["quantity","pricePerContract","timestamp","optionName","optionType"]].values.tolist()
            for j in temp_sell.itertuples():
                avgPrice = {"qty":[],"price" : []}
                item = {"timestamp":j.timestamp,"symbol":stock,
                        "optionName":j.optionName,"optionType":j.optionType,
                        "sellQty" : j.quantity,"sellPrice":j.pricePerContract}
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
                        print(f"Error in optionsOrdersJournal inner loop while splits : {e} \n")
                    
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
            #need to add option expirateion
            for p in buystack:
                item2 = {"timestamp":p[2],"symbol":stock,
                        "optionName":p[3],"optionType":p[4],
                        "sellQty" : p[0],"sellPrice":0,"avgBuyPrice": p[1]}
                returnList.append(item2)
        except Exception as e:
            print(f"Error in optionsOrderJournal outer loop : {e} stock \n")
    returnList = pd.DataFrame(returnList)
    returnList["profit_loss/option"] = returnList["sellPrice"] - returnList["avgBuyPrice"]
    returnList["sellAmount"] = returnList["sellQty"]*returnList["sellPrice"]
    returnList["buyAmount"] = returnList["sellQty"]*returnList["avgBuyPrice"]
    returnList["total_gain"] = returnList["sellAmount"]-returnList["buyAmount"]
    return returnList.sort_values(by = ["timestamp"],ascending=False)




if __name__ == '__main__':
    print("*_"*75)
    print("\n\nChecking for data folder \"./dashApp/data\" , \nIf found will delete folder and create new folder in order to update with new data, Otherwise will create ./dashApp/data folder and store all required data in there")
    try:
        if os.path.isdir("./data"):
            decision = input("\nFound directory ./dashApp/data :\nPlease type 'YES' to confirm deletation of directory and its contents\nType 'NO' if you want to store copy of previous data,"+
                                 "\nIf 'NO', please change the name of directory or store it outside dashApp folder.\nScript will exit at 'NO', creating new data folder is required so files don't overlap.\n >>>>>>>>>>>>>>>>>  ").lower()
            if decision[0] == 'n':
                sys.exit("!!!!!!!!!!!!   Ending script. Data directory requirement - Failed   !!!!!!!!!!!!")
            shutil.rmtree("./data")
        os.mkdir("./data")
    except OSError:
        print("Error in creating a data directory folder for dataframes from Robin_hood.py ::: \n")
    
    print()
    rh = Robinhood()
    print("\n \nLogin Successful...  : ", rh.login(username = None , password = None))
    print()
    print(".............Downloading data from Robinhood................."*2)
    print()
    
    try:
        stocks_portfolio = stocksPortfolioDataframe(rh)
        stocks_portfolio.to_csv('./data/stocks_portfolio.csv',index = False)
    except Exception as e:
        print("No Records Found!! or Error getting Stocks Portfolio in Robin_hood.py main  ::: \n", e)
   
    try:
        options_portfolio = optionsPortfolioDataFrame(rh)
        options_portfolio.to_csv('./data/options_portfolio.csv',index = False)
    except Exception as e:
        print("No Records Found!! or Error getting Options Portfolio in Robin_hood.py main  ::: \n", e)
        
    try:    
        pending_orders = pendingOrders(rh)
        pending_orders.to_csv('./data/pending_orders.csv',index = False)
    except Exception as e:
        print("No Records Found!! or Error getting Pending Orders in Robin_hood.py main  ::: \n", e)
       
    try:
        order_book = ordersDataFrame(rh)
        order_book.to_csv('./data/order_book.csv',index = False)
    except Exception as e:
        print("No Records Found!! or Error getting Stocks OrderBook in Robin_hood.py main  ::: \n", e)
       
    try:
        options_orderbook = optionsOrderDataFrame(rh)
        options_orderbook.to_csv('./data/options_orderbook.csv',index = False)
    except Exception as e:
        print("No Records Found!! or Error getting Options OrderBook in Robin_hood.py main  ::: \n", e)
       
    try:
        stocks_journal = ordersJournal(order_book).sort_values(by = ["timestamp"],ascending = False)
        stocks_journal.to_csv('./data/stocks_journal.csv',index = False)
    except Exception as e:
        print("No Records Found!! or Error getting Stocks Journal in Robin_hood.py main  ::: \n", e)
   
    try:
        options_journal = optionsOrderJournal(options_orderbook)
        options_journal.to_csv('./data/options_journal.csv',index = False)
    except Exception as e:
        print("No Records Found!! or Error getting Options Journal in Robin_hood.py main  ::: \n", e)
        
    print()
    print(rh.logout())
    print("All of the dataframe needed for Plotly DASH App are stored in .csv format in given ./dashApp/data directory")
    print("*_"*100) 
    
    
