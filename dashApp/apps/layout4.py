#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  3 19:45:28 2021

@author: Robinhood-trading-journal
"""
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
from app import app, table_type
import plotly.express as px
import dash_table
from dash_table.Format import Format, Group, Scheme
from datetime import datetime



try:
    stocksJournal = pd.read_csv("./data/stocks_journal.csv")
    stocksJournal['timestamp'] = pd.to_datetime(stocksJournal['timestamp'])
    stocksJournal['gainPercent'] = (stocksJournal['total_gain']/stocksJournal['buyAmount'])*100
    instrumentStocksJrnlLayout = [
        dbc.Row(dbc.Col(
                 dbc.Button( "Stock Journal",id = 'btn-collapse2',n_clicks=0,color="primary", className="mr-1",style={'font-size':24,'width':"100x"},) )
                ),
        dbc.Row(style={'width': '100%', 'height': 10}
            ),
        dbc.Row(dbc.Collapse(dbc.Table(
                    dash_table.DataTable(
                        id = 'InstrumentStocksJrnl',
                        columns=[
                              {"name":"Timestamp" , "id": "timestamp" ,'type': table_type(stocksJournal["timestamp"])},
                              {"name": "Market", "id":"market" ,'type': table_type(stocksJournal["market"])},
                              {"name": "Symbol", "id": "symbol",'type': table_type(stocksJournal["symbol"])},
                              {"name": "Name", "id": "stockName",'type': table_type(stocksJournal["stockName"])},
                              {"name": "Fees", "id": "fees",'type': table_type(stocksJournal["fees"]),"format": Format(precision=3, scheme=Scheme.fixed, group=Group.yes, groups=[3])},
                              {"name": "Sell Qty", "id": "sellQty",'type': table_type(stocksJournal["sellQty"]),"format": Format(precision=3, scheme=Scheme.fixed, group=Group.yes, groups=[3])},
                              {"name": "Sell Price", "id": "sellPrice",'type': table_type(stocksJournal["sellPrice"]),"format": Format(precision=3, scheme=Scheme.fixed, group=Group.yes, groups=[3])},
                              {"name": "Avg Buy Price", "id": "avgBuyPrice",'type': table_type(stocksJournal["avgBuyPrice"]),"format": Format(precision=3, scheme=Scheme.fixed, group=Group.yes, groups=[3])},
                              {"name": "Profit/Loss per Stock", "id": "profit_loss/stock",'type': table_type(stocksJournal[ "profit_loss/stock"]),"format": Format(precision=3, scheme=Scheme.fixed, group=Group.yes, groups=[3])},
                              {"name": "Sell Amount", "id": "sellAmount",'type': table_type(stocksJournal["sellAmount"]),"format": Format(precision=3, scheme=Scheme.fixed, group=Group.yes, groups=[3])},
                              {"name": "Buy Amount", "id": "buyAmount" ,'type': table_type(stocksJournal["buyAmount"]),"format": Format(precision=3, scheme=Scheme.fixed, group=Group.yes, groups=[3])},
                              {"name": "Total Gain", "id": "total_gain",'type': table_type(stocksJournal['total_gain']),"format": Format(precision=3, scheme=Scheme.fixed, group=Group.yes, groups=[3])},
                              {"name": "Percentage Gain %%", "id": "gainPercent",'type':'numeric',"format": Format(precision=4, scheme=Scheme.fixed,) }
                              ],
                        style_cell={'minWidth': '110px','width':'110px','maxWidth': '110px','whiteSpace': 'normal','height': 'auto','border': '1px solid grey'},
                        style_table={'border': '1px solid grey','height': 'auto','overflowY': 'auto'},
                        page_size = 50,
                        fixed_rows = {'headers':True},
                        style_header={'fontWeight': 'bold','backgroundColor': 'rgb(230, 230, 230)',},
                        sort_action='native', 
                        filter_action="native",
                        sort_mode="multi",
                        virtualization=True,
                      ),
                    style={'width': '100%'}),
                id='collapse2',is_open=True),style={'width': '100%'}
            ),
        dbc.Row(style={'width': '100%', 'height': 10}
            ),]
    @app.callback(
        Output("collapse2", "is_open"),
        [Input("btn-collapse2", "n_clicks")],
        [State("collapse2", "is_open")],
        )
    def toggle_collapse2(n, is_open):
        if n:
            return not is_open
        return is_open
   
    @app.callback(
        Output('InstrumentStocksJrnl', 'data'),
        Output('stcksjrnl','style'),
        Input('select-in', 'value'),
        Input('instrument-date', 'start_date'),
        Input('instrument-date', 'end_date')
        )
    def tabledata2(value,start_date,end_date):
        if value is None: return [None,{'display':'none'}]
        sj = stocksJournal[stocksJournal["symbol"]==value].copy()
        if start_date is not None:
            sj = sj[sj["timestamp"].dt.date >= datetime.strptime(start_date,"%Y-%m-%d").date()]
        if end_date is not None:
            sj = sj[sj["timestamp"].dt.date <= datetime.strptime(end_date,"%Y-%m-%d").date()]
        sj = sj.to_dict('records')
        hideDiv = {'display':'block'}
        if len(sj) == 0:
            hideDiv = {'display':'none'}
        return [sj, hideDiv]
        
except:
    stocksJournal = None
    

try:
    optionsJournal = pd.read_csv("./data/options_journal.csv")
    optionsJournal['timestamp'] = pd.to_datetime(optionsJournal['timestamp'])
    optionsJournal['gainPercent'] = (optionsJournal['total_gain']/optionsJournal['buyAmount'])*100
    instrumentOptionJrnlLayout = [
        dbc.Row(dbc.Col(
                    dbc.Button("Options Journal",id = 'btn-collapse1',n_clicks=0,color="primary", className="mr-1",style={'font-size':24,'width':"100x"},) )
            ),
        dbc.Row(style={'width': '100%', 'height': 10}
            ),
        dbc.Row(dbc.Collapse(dbc.Table( 
                    dash_table.DataTable(
                          id = 'InstrumentOptionsJrnl', 
                          columns=[
                              {"name":"Timestamp" , "id": "timestamp" ,'type': table_type(optionsJournal["timestamp"])},
                              {"name": "Symbol", "id": "symbol",'type': table_type(optionsJournal["symbol"])},
                              {"name": "Option Name", "id": "optionName",'type': table_type(optionsJournal["optionName"])},
                              {"name": "Option Type", "id": "optionType",'type': table_type(optionsJournal["optionType"])},
                              {"name": "Sell Qty", "id": "sellQty",'type': table_type(optionsJournal["sellQty"]),"format": Format(precision=3, scheme=Scheme.fixed, group=Group.yes, groups=[3])},
                              {"name": "Sell Price", "id": "sellPrice",'type': table_type(optionsJournal["sellPrice"]),"format": Format(precision=3, scheme=Scheme.fixed, group=Group.yes, groups=[3])},
                              {"name": "Avg Buy Price", "id": "avgBuyPrice",'type': table_type(optionsJournal["avgBuyPrice"]),"format": Format(precision=3, scheme=Scheme.fixed, group=Group.yes, groups=[3])},
                              {"name": "Profit/Loss per Contract", "id": "profit_loss/option",'type': table_type(optionsJournal[ "profit_loss/option"]),"format": Format(precision=3, scheme=Scheme.fixed, group=Group.yes, groups=[3])},
                              {"name": "Sell Amount", "id": "sellAmount",'type': table_type(optionsJournal["sellAmount"]),"format": Format(precision=3, scheme=Scheme.fixed, group=Group.yes, groups=[3])},
                              {"name": "Buy Amount", "id": "buyAmount" ,'type': table_type(optionsJournal["buyAmount"]),"format": Format(precision=3, scheme=Scheme.fixed, group=Group.yes, groups=[3])},
                              {"name": "Total Gain", "id": "total_gain",'type': table_type(optionsJournal['total_gain']),"format": Format(precision=3, scheme=Scheme.fixed, group=Group.yes, groups=[3])},
                              {"name": "Percentage Gain %%", "id": "gainPercent",'type':'numeric',"format": Format(precision=4, scheme=Scheme.fixed,)}
                              ],
                          style_cell={'minWidth': '110px','width':'110px' ,'maxWidth': '110px','whiteSpace': 'normal','height': 'auto','border': '1px solid grey'},
                          style_table={'border': '1px solid grey','height': 'auto','overflowY': 'auto'},
                          page_size = 50,
                          fixed_rows = {'headers':True},
                          style_header={'fontWeight': 'bold','backgroundColor': 'rgb(230, 230, 230)',},
                          sort_action='native', 
                          filter_action="native",
                          sort_mode="multi",
                          virtualization=True,
                      ),
                    style={'width': '100%'}
                    ),
                id='collapse1',is_open=True)),
        dbc.Row(style={'width': '100%', 'height': 10}
            ),]
    
    
    @app.callback(
        Output("collapse1", "is_open"),
        [Input("btn-collapse1", "n_clicks")],
        [State("collapse1", "is_open")],
        )
    def toggle_collapse1(n, is_open):
        if n:
            return not is_open
        return is_open
    
    
    @app.callback(
        Output('InstrumentOptionsJrnl', 'data'),
        Output('optionjrnl','style'),
        Input('select-in', 'value'),
        Input('instrument-date', 'start_date'),
        Input('instrument-date', 'end_date')
        )
    def tabledata1(value,start_date,end_date):
        if value is None: return [None,{'display':'none'}]
        oj = optionsJournal[optionsJournal["symbol"]==value].copy()
        if start_date is not None:
            oj = oj[oj["timestamp"].dt.date >= datetime.strptime(start_date,"%Y-%m-%d").date()]
        if end_date is not None:
            oj = oj[oj["timestamp"].dt.date <= datetime.strptime(end_date,"%Y-%m-%d").date()]
        oj = oj.to_dict('records')
        hideDiv = {'display':'block'}
        if len(oj) == 0:
            hideDiv = {'display':'none'}
            
        #Will add bublle chart here
        return [oj, hideDiv]
       
    
    ## This method will only work if there is option journal and stocks journal for given stock else it will hide whole block
    @app.callback(Output('listgroup', 'children'),
        Input('InstrumentStocksJrnl', 'derived_virtual_data'),
        Input('InstrumentOptionsJrnl', 'derived_virtual_data')
         )
    def getlistgroup(rows1,rows2):
        df_s = pd.DataFrame(rows1).copy()
        df_o = pd.DataFrame(rows2).copy()
        if len(df_s) <=0 or len(df_o) <=0:
            return [None] 
        index = ['$$ Total Sell','$$ Total Buy','$$ Total Gain', '$$ Total Loss','$$ Net Gain', '$$ Avg Gain',
                     '%% Net Profit/Loss','%% Win Rate','Profit rate', 'P/L: Profit Factor']
        tableBody =[]
        for  i in zip(index,getList(df_s),getList(df_o)):
            tableBody.append(html.Tr([
                html.Td(i[0],style={'font-size':18,'textAlign':'left'}), 
                html.Td(i[1],style={'textAlign':'right'}),
                html.Td(i[2],style={'textAlign':'right'})
                ]))
        table = [html.Thead(html.Tr([html.Th(""), html.Th("Stocks Overview"), html.Th("Options Overview")],style={'font-size':22,'textAlign':'center'}))]+[html.Tbody(tableBody)]
        
        df_s = df_s.rename(columns={'stockName':'Name'})
        df_s['Type'] = "Stock"
        df_o = df_o.rename(columns={'optionName':'Name'})
        df_o['Type'] = "Option"
        df = pd.concat([df_s[["Name","sellQty","sellPrice","avgBuyPrice","sellAmount","buyAmount","total_gain","Type"]],
                        df_o[["Name","sellQty","sellPrice","avgBuyPrice","sellAmount","buyAmount","total_gain","Type"]]])
        df['gainPercent'] = ((df['total_gain']/df['buyAmount']).round(2) * 100).astype(float)
        
        
        fig = px.scatter(df, size=df["total_gain"].apply(lambda x: round((abs(x))*(1/3),2) if x else 0), y="gainPercent",x="buyAmount",facet_row='Type',log_x=True,height = 685,width = 800,
                         color="total_gain",hover_name="Name",color_continuous_scale=["red","green"],color_continuous_midpoint =0, hover_data = ["sellQty","avgBuyPrice","sellPrice","sellAmount",],
                         labels={'gainPercent':'%% Percentage Gain','size':'Size: Sqrt(abs(Total Gain))','total_gain':'$$ Total Gain','buyAmount':'$$ Invested (Buy Amount)',
                                     "sellQty":"Quantity","avgBuyPrice":"Avg Buy Price","sellPrice": "Sell Price","sellAmount":"Sell Amount",'Type':'Instrument Type'}, size_max=30  )#log_x=True, size_max=60)
        fig.update_layout(title={'text':'Four Dimension Bubble Chart <br>Invested - Percentage Gain - Total Gain - Instrument Type',
                                'font': {'size': 18},
                                'xanchor':'center',
                                'x': 0.45, 'y':0.96
                                })
        fig.update_xaxes(zeroline=True, zerolinewidth=2, zerolinecolor='black')
        fig.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor='black')
        returnLayout = [dbc.Row([
                    dbc.Col([
                            dbc.Row(style={'height':5}),
                            dbc.Row(dbc.Table(table,bordered= True,size='sm',#className='table-dark ',
                                                  style={ 'width': '100%',}),style={"width":'100%'} )
                        ],width = 5),
                    dbc.Col(dcc.Graph(figure = fig,style={'whiteSpace':'pre'}),width=7,style={'whiteSpace':'pre'})
                    ]),
                dbc.Row(style={"width":'100%', 'height' :30}) ]
        
        return returnLayout
       

except:
    optionsJournal = None








try:
    optionsOrderBook = pd.read_csv("./data/options_orderbook.csv")
    optionsOrderBook['timestamp'] = pd.to_datetime(optionsOrderBook['timestamp'])
    optionsOrderBook[["pricePerContract","quantity"]]= optionsOrderBook[["pricePerContract","quantity"]].round(decimals=2)
    instrumentOptionsOrderBk = [
        dbc.Row(dbc.Col(
                    dbc.Button("Options Order Book",id = 'btn-collapse3',n_clicks=0,color="primary", className="mr-1", style={'font-size':24,'width':"100x"},) )
            ),
        dbc.Row(style={'width': '100%', 'height': 10}
            ),
        dbc.Row(dbc.Collapse(dbc.Table( 
                    dash_table.DataTable(
                          id = 'InstrumentOptionsOrderBook',
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
                        style_table={'border': '1px solid grey', 'height': 'auto','overflowY': 'auto'},
                        fixed_rows = {'headers':True},
                        style_header={'fontWeight': 'bold','backgroundColor': 'rgb(230, 230, 230)',},
                        sort_action='native', 
                        filter_action="native",
                        sort_mode="multi",
                        virtualization=True,
                      ),
                    style={'width': '100%'}
                    ),
                id='collapse3',is_open=True)),
        dbc.Row(style={'width': '100%', 'height': 10}
            ),]
    @app.callback(
        Output("collapse3", "is_open"),
        [Input("btn-collapse3", "n_clicks")],
        [State("collapse3", "is_open")],
        )
    def toggle_collapse3(n, is_open):
        if n:
            return not is_open
        return is_open
    
    @app.callback(
        Output('InstrumentOptionsOrderBook', 'data'),
        Output('optionbk','style'),
        Input('select-in', 'value'),
        Input('instrument-date', 'start_date'),
        Input('instrument-date', 'end_date')
        )
    def tabledata3(value,start_date,end_date):
        if value is None: return [None,{'display':'none'}]
        optnb = optionsOrderBook[optionsOrderBook["symbol"]==value].copy()
        if start_date is not None:
            optnb = optnb[optnb["timestamp"].dt.date >= datetime.strptime(start_date,"%Y-%m-%d").date()]
        if end_date is not None:
            optnb = optnb[optnb["timestamp"].dt.date <= datetime.strptime(end_date,"%Y-%m-%d").date()]
        optnb = optnb.to_dict('records')
        hideDiv = {'display':'block'}
        if len(optnb) == 0:
            hideDiv = {'display':'none'}
        return [optnb, hideDiv]
except:
    optionsOrderBook = None



orderBook = pd.read_csv("./data/order_book.csv")
orderBook['timestamp'] = pd.to_datetime(orderBook['timestamp'])
orderBook[["fees","price"]]=orderBook[["fees","price"]].round(decimals=2)
instrumentOrderBk = [
        dbc.Row(dbc.Col(
                    dbc.Button("Order Book",id = 'btn-collapse4', n_clicks=0,color="primary", className="mr-1",style={'font-size':24,'width':"100x"},) )
            ),
        dbc.Row(style={'width': '100%', 'height': 10}
            ),
        dbc.Row(dbc.Collapse(dbc.Table(
                    dash_table.DataTable(
                        id='InstrumentOrderBook', 
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
                        style_cell={'minWidth': '100px', 'maxWidth': '125px','whiteSpace': 'normal',
                                    'border': '1px solid grey','height': 'auto'},
                        page_size = 50,
                        style_table={'border': '1px solid grey','hieght':'auto','overflowY': 'auto'},
                        fixed_rows = {'headers':True},
                        style_header={'fontWeight': 'bold', 'backgroundColor': 'rgb(230, 230, 230)',},
                        sort_action='native', 
                        filter_action="native",
                        sort_mode="multi",
                        
                        virtualization=True,
                    ),style={'width': '100%'}),
                id='collapse4',is_open=True))
         ]
@app.callback(
    Output("collapse4", "is_open"),
    [Input("btn-collapse4", "n_clicks")],
    [State("collapse4", "is_open")],
    )
def toggle_collapse4(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output('InstrumentOrderBook', 'data'),
    Input('select-in', 'value'),
    Input('instrument-date', 'start_date'),
    Input('instrument-date', 'end_date')
    )
def tabledata4(value,start_date,end_date):
    if value is None: return [None]
    ob = orderBook[orderBook["symbol"]==value].copy()
    if start_date is not None:
        ob = ob[ob["timestamp"].dt.date >= datetime.strptime(start_date,"%Y-%m-%d").date()]
    if end_date is not None:
        ob = ob[ob["timestamp"].dt.date <= datetime.strptime(end_date,"%Y-%m-%d").date()]
    ob = ob.to_dict('records')
    return ob
        


layout4 = html.Div(children=[
        dbc.Row(
            style={
                'width': '100%', 'height': 25
                }
            ),    
        dbc.Row([
                dbc.Col(html.Div(dbc.Select(
                                  id="select-in",options=[ {"label": f"{i.symbol:<5}  :  {i.name:<26}", "value": i.symbol} for i in orderBook[['symbol','name']].drop_duplicates().sort_values(by=['symbol']).itertuples()],
                                  placeholder="Select a Instrument from the list.....",className = "form-select",persistence=True,persistence_type = 'memory',),className="form-group"),
                        width = {'size':5.75,'offset':1},style={'padding': '11px 0px 0px 0px'}
                    ),
                dbc.Col(
                    dcc.DatePickerRange(
                                    id='instrument-date',
                                    min_date_allowed = min(orderBook['timestamp']).date(),
                                    max_date_allowed= max(orderBook['timestamp']).date(),
                                    display_format='MM/DD/YYYY',
                                    with_portal  = True, number_of_months_shown = 4,
                                    start_date_placeholder_text='MM/DD/YYYY', day_size=36,
                                    clearable=True, persistence=True, persistence_type = 'memory',
                        ),style={'width':'100%','padding': '0px 0px 0px 50px',"textAlign":"center"},
                    width = {'size':4,'offset':2}),
                ]),
        dbc.Row(style={'width': '100%', 'height': 20}
            ),
        html.Div(id = "select-out",children=[])
        ], style={'padding': '0px 20px 25px 20px'})


@app.callback(
    Output('select-out', 'children'),
    Input('select-in', 'value')
)
def blankLayout(value):
    if (value is None)or(value == "None"): return None
    else:
        if (optionsJournal is None) or (stocksJournal is None) :
            instrumentLayout =[]
            
        else:
            instrumentLayout =[html.Div(id='listgroup')]
            
        instrumentLayout.append(html.Div(id = 'optionjrnl',children =  None if optionsJournal is None else instrumentOptionJrnlLayout))
        instrumentLayout.append(html.Div(id = 'stcksjrnl',children = None if stocksJournal is None else instrumentStocksJrnlLayout))
        instrumentLayout.append(html.Div(id = 'optionbk',children = None if optionsOrderBook is None else instrumentOptionsOrderBk))
        instrumentLayout.append(html.Div(id = 'ordrbk',children = instrumentOrderBk))
        return instrumentLayout 


     


def getList(dff):
    rtrnList = []
    totalsell = dff.sellAmount.sum().round(2)
    rtrnList.append(dbc.ListGroupItem(totalsell, style={'font-size':16}, color = 'info'))
    
    totalbuy = dff.buyAmount.sum().round(2)
    rtrnList.append(dbc.ListGroupItem(totalbuy,style={'font-size':16},color = 'info'))
    
    # avgsell = round(dff.sellAmount.mean(),2)
    # rtrnList.append(dbc.ListGroupItem(avgsell,color = 'info'))
    
    # avgbuy = round(dff.buyAmount.mean(),2) 
    # rtrnList.append(dbc.ListGroupItem(avgbuy,color = 'info'))
    
    totalgain = round(dff.total_gain[dff.total_gain>=0].sum(),2) 
    rtrnList.append(dbc.ListGroupItem(totalgain,style={'font-size':16},color='success'))
    
    totalloss = round(dff.total_gain[dff.total_gain<0].sum(),2)
    rtrnList.append(dbc.ListGroupItem(totalloss,style={'font-size':16},color='danger'))
    
    avgprofit = round(dff.total_gain[dff.total_gain>=0].mean(),2) 
    avgprofit = 0 if str(avgprofit) == 'nan' else avgprofit
    #rtrnList.append(dbc.ListGroupItem(avgprofit,color='success'))
    
    avgloss = round(dff.total_gain[dff.total_gain<0].mean(),2) 
    avgloss = 0 if str(avgloss) == 'nan' else avgloss
    #rtrnList.append(dbc.ListGroupItem(avgloss,color='danger'))
    
    netgain = round(dff.total_gain.sum(),2)
    rtrnList.append(dbc.ListGroupItem(netgain,style={'font-size':16},color = "success" if (netgain)>0 else "danger"))
    
    
    avggain = round(dff.total_gain.mean(),2)
    rtrnList.append(dbc.ListGroupItem(avggain, style={'font-size':16},color="success" if (avggain)>0 else "danger"))
    
    percentgain = round((netgain/totalbuy)*100,2) 
    rtrnList.append(dbc.ListGroupItem(percentgain,style={'font-size':16},color="success" if  percentgain > 0 else "danger"))
    
    winingtrade = len(dff.total_gain[dff.total_gain>=0])
    winrate = round((winingtrade/len(dff))*100,2)
    rtrnList.append(dbc.ListGroupItem(winrate,style={'font-size':16}, color = "success" if (winrate)>51 else "danger"))
    
    profitrate = round((totalgain/(totalgain + abs(totalloss)))*100,2) if (totalgain + abs(totalloss)) != 0 else 0
    rtrnList.append(dbc.ListGroupItem(profitrate,style={'font-size':16},color="success" if (profitrate)>51 else "danger"))
    
    profitfactor = round(totalgain/abs(totalloss),2) if totalloss != 0 else 'N/A'
    rtrnList.append(dbc.ListGroupItem(profitfactor,style={'font-size':16},color="success" if (profitfactor != 'N/A') and (profitfactor)>1.25  else "danger"))
    
    # profitibility = round((winrate*avgprofit -((100-winrate)*abs(avgloss)))/100,2) if avgloss != 0 else 'N/A'
    # rtrnList.append(dbc.ListGroupItem(profitibility,color="success" if (profitibility != 'N/A') and (profitibility)>0  else "danger"))
    
        
    return rtrnList

