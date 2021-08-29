#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  3 19:45:28 2021

@author: Robinhood-trading-journal
"""

import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import pandas as pd
from app import table_type


try:
    orderBook = pd.read_csv("./data/order_book.csv")
    orderBook[["fees","price"]]=orderBook[["fees","price"]].round(decimals=2)
    
    orderBookTable = dash_table.DataTable(
                    id='datatable-interactivity-3', 
                    columns=[{"name": 'Timestamp', "id": 'timestamp','type': table_type(orderBook['timestamp'])},
                             {"name": 'Settlement Date', "id": 'settlement_date','type': table_type(orderBook['settlement_date'])},
                             {"name": 'Order ID', "id": 'orderId','type': table_type(orderBook['orderId'])},
                             {"name": 'Transaction ID', "id": 'transactionId','type': table_type(orderBook['transactionId'])},
                             {"name": 'Market', "id": 'market','type': table_type(orderBook['market'])},
                             {"name": 'Name', "id": 'name','type': table_type(orderBook['name'])}, 
                             {"name": 'Symbol', "id": 'symbol','type': table_type(orderBook['symbol'])},
                             {"name": 'Instrument Type', "id": 'instrumentType','type': table_type(orderBook['instrumentType'])},
                             {"name": 'Order Type', "id": 'orderType','type': table_type(orderBook['orderType'])},
                             {"name": 'Fees', "id": 'fees','type': table_type(orderBook['fees'])},
                             {"name": 'Price', "id": 'price','type': table_type(orderBook['price'])},
                             {"name": 'Qty', "id": 'quantity','type': table_type(orderBook['quantity'])},
                             {"name": 'Side', "id": 'side','type': table_type(orderBook['side'])},
                             ],
                    data = orderBook.to_dict('records'),
                    style_cell={'minWidth': '95px', 'maxWidth': '132px','whiteSpace': 'normal',
                                'border': '1px solid grey','height': 'auto'},
                    page_size = 50,
                    style_table={'border': '1px solid grey', 'overflowY': 'auto'},
                    fixed_rows = {'headers':True},
                    style_header={'fontWeight': 'bold','backgroundColor': 'rgb(230, 230, 230)',},
                    sort_action='native', 
                    filter_action="native",
                    sort_mode="multi",
                    virtualization=True,
                )
    
    stockslayout = html.Div(children=[
            dbc.Row(
                style={
                    'width': '100%', 'height': 15
                    }
                ),    
            dbc.Row(
                    dbc.Col(
                        html.H1("Stocks Order Book",
                            style={"textAlign":"center",'font-size':38,'width':"100x"},
                               ) )
                ),
            dbc.Row(
                style={
                    'width': '100%', 'height': 10
                    }
                ),
            dbc.Row(
                dbc.Table(orderBookTable),
                style={'width': '100%'},align="center",
                )
            
    ],style={'padding': '0px 20px 0px 20px','width': '100%'})
except FileNotFoundError:
    stockslayout = None



try:
    optionsOrderBook = pd.read_csv("./data/options_orderbook.csv")
    optionsOrderBook[["pricePerContract","quantity"]]= optionsOrderBook[["pricePerContract","quantity"]].round(decimals=2)
    
    optionsOrderTable = dash_table.DataTable(
                    columns=[{"name": 'Timestamp', "id": 'timestamp','type': table_type(optionsOrderBook['timestamp'])},
                            {"name": 'Settlement Date', "id": 'settlement_date','type': table_type(optionsOrderBook['settlement_date'])},
                            {"name": 'Order ID', "id": 'orderId','type': table_type(optionsOrderBook['orderId'])},
                            {"name": 'Transaction ID', "id": 'transactionId','type': table_type(optionsOrderBook['transactionId'])},
                            {"name": 'Symbol', "id": 'symbol','type': table_type(optionsOrderBook['symbol'])},
                            {"name": 'Name', "id": 'optionName','type': table_type(optionsOrderBook['optionName'])}, 
                            {"name": 'Option Type', "id": 'optionType','type': table_type(optionsOrderBook['optionType'])},
                            {"name": 'Price per Contract', "id": 'pricePerContract','type': table_type(optionsOrderBook['pricePerContract'])},
                            {"name": 'Qty', "id": 'quantity','type': table_type(optionsOrderBook['quantity'])},
                            {"name": 'Side', "id": 'side','type': table_type(optionsOrderBook['side'])},
                            {"name": 'Opening Strategy', "id": 'opening_strategy','type': table_type(optionsOrderBook['opening_strategy'])},
                            {"name": 'Closing Strategy', "id": 'closing_strategy','type': table_type(optionsOrderBook['closing_strategy'])},
                            ],
                    data = optionsOrderBook.to_dict('records'),
                    style_cell={'minWidth': '118px', 'maxWidth': '118px',
                                'border': '1px solid grey','whiteSpace': 'normal','height': 'auto'},
                    page_size = 50,
                    style_table={'border': '1px solid grey', 'overflowY': 'auto'},
                    fixed_rows = {'headers':True},
                    style_header={'fontWeight': 'bold','backgroundColor': 'rgb(230, 230, 230)',},
                    sort_action='native', 
                    filter_action="native",
                    sort_mode="multi",
                    virtualization=True,
                )
    
    optionslayout = html.Div(children=[
            dbc.Row(
                style={
                    'width': '100%', 'height': 15
                    }
                ),    
            dbc.Row(
                    dbc.Col(
                        html.H1("Options Order Book",
                            style={"textAlign":"center",'font-size':38,'width':"100x"},
                               ) )
                ),
            dbc.Row(
                style={
                    'width': '100%', 'height': 10
                    }
                ),
            dbc.Row(
                dbc.Table(optionsOrderTable),
                style={'width': '100%'},align="center",
                )
            
    ],style={'padding': '0px 20px 0px 20px','width': '100%'})
except FileNotFoundError :
    optionslayout = None



try:
    pendingOrderBook = pd.read_csv("./data/pending_orders.csv")
    pendingOrderTable = dash_table.DataTable(
                    columns=[{"name": 'Order ID', "id": 'orderId','type': table_type(pendingOrderBook['orderId'])},
                             {"name": 'Market', "id": 'market','type': table_type(pendingOrderBook['market'])},
                             {"name": 'Instrument Type', "id": 'instrumentType','type': table_type(pendingOrderBook['instrumentType'])},
                             {"name": 'Symbol', "id": 'symbol','type': table_type(pendingOrderBook['symbol'])},
                             {"name": 'Name', "id": 'name','type': table_type(pendingOrderBook['name'])}, 
                             {"name": 'Order State', "id": 'orderState','type': table_type(pendingOrderBook['orderState'])},
                             {"name": 'Order Type', "id": 'orderType','type': table_type(pendingOrderBook['orderType'])},
                             {"name": 'Side', "id": 'side','type': table_type(pendingOrderBook['side'])},
                             {"name": 'Price', "id": 'price','type': table_type(pendingOrderBook['price'])},
                             {"name": 'Qty', "id": 'quantity','type': table_type(pendingOrderBook['quantity'])},
                             {"name": 'Fees', "id": 'fees','type': table_type(pendingOrderBook['fees'])},
                             {"name": 'Last Transaction Time', "id": 'last_transaction_at','type': table_type(pendingOrderBook['last_transaction_at'])},
                             {"name": 'Executions', "id": 'executions','type': table_type(pendingOrderBook['executions'])},
                             ],
                    data = pendingOrderBook.to_dict('records'),
                    style_cell={'minWidth': '100px', 'maxWidth': '115px','whiteSpace': 'normal',
                                'border': '1px solid grey','height': 'auto'},
                    page_size = 50,
                    style_table={ 'overflowY': 'auto','border': '1px solid grey'},
                    fixed_rows = {'headers':True},
                    style_header={'fontWeight': 'bold','backgroundColor': 'rgb(230, 230, 230)',},
                    sort_action='native', 
                    filter_action="native",
                    sort_mode="multi",
                    virtualization=True,
                )
    
    
    pendingOrderslayout = html.Div(children=[
            dbc.Row(
                style={
                    'width': '100%', 'height': 15
                    }
                ),    
            dbc.Row(
                    dbc.Col(
                        html.H1("Stocks Pending Order Book",
                            style={"textAlign":"center",'font-size':38,'width':"100x"},
                               ) )
                ),
            dbc.Row(
                style={
                    'width': '100%', 'height': 10
                    }
                ),
            dbc.Row(
                dbc.Table(pendingOrderTable),
                style={'width': '100%'},align="center",
                )
            
    ],style={'padding': '0px 20px 0px 20px','width': '100%'})
except FileNotFoundError:
    pendingOrderslayout = None