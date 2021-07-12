#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  3 18:06:27 2021

@author: viraj
"""
import dash
from datetime import datetime,timezone,timedelta 
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash_table
import pandas as pd
from Robin_hood import table_type
from app import app

stocks_Journal = pd.read_csv("orderJournal.csv")
stocks_Journal['timestamp'] = pd.to_datetime(stocks_Journal['timestamp'])



layout2 = html.Div(children=[
        dbc.Row( style={ 'width': '100%', 'height': 30 }
            ),    
        
        dbc.Row( dbc.Col( html.H1("Stocks Journal",
                                  style={"textAlign":"center",'font-size':38,'width':"100x"},
                            ))
            ),
        
        dbc.Row( style={ 'width': '100%', 'height': 20 }
            ),
        dbc.Row( html.H4("Select dates from date range or predefined date range for date filter.",style={'font-size':18,'padding': '0px 20px 0px 20px'})
            ,style={ 'width': '100%'}
            ),
        
        dbc.Row([
            dcc.DatePickerRange(
                id='my-date-picker-range',
                min_date_allowed = min(stocks_Journal['timestamp']).date(),
                max_date_allowed= max(stocks_Journal['timestamp']).date(),
                display_format='MM/DD/YYYY',
                with_portal  = True,
                day_size=44,
                clearable=True,
                
                style = {'width':'27%',"textAlign":"center",'padding': '3px 0px 0px 0px'},
                
                ),
            dbc.Button("Clear",id='clear', color="primary", className="mr-1",n_clicks = 0,style = {'width':'8%',"textAlign":"center"}),
            dbc.Button("Today",id= 'today', color="primary",className="mr-1",n_clicks = 0,style = {'width':'8%',"textAlign":"center"}),
            dbc.Button("This Week",id = 'week', color="primary", className="mr-1",n_clicks = 0,style = {'width':'10%',"textAlign":"center"}),
            dbc.Button("This Month",id = 'month', color="primary", className="mr-1",n_clicks = 0,style = {'width':'10%',"textAlign":"center"}),
            dbc.Button("This Quarter",id='quarter', color="primary", className="mr-1",n_clicks = 0,style = {'width':'11%',"textAlign":"center"}),
            dbc.Button("This Year",id='year', color="primary", className="mr-1",n_clicks = 0,style = {'width':'10%',"textAlign":"center"}),
            dbc.DropdownMenu([
                dbc.DropdownMenuItem("Quarter 1 : Jan/01 - Mar/31",id='quarter1', className="mr-1",n_clicks = 0, disabled= True if datetime.today().month<3 else False),
                dbc.DropdownMenuItem("Quarter 2 : Apr/01 - May/31",id='quarter2', className="mr-1",n_clicks = 0, disabled= True if datetime.today().month<5 else False),
                dbc.DropdownMenuItem("Quarter 3 : Jun/01 - Aug/31",id='quarter3', className="mr-1",n_clicks = 0, disabled= True if datetime.today().month<8 else False),
                dbc.DropdownMenuItem("Quarter 4 : Sep/01 - Dec/31",id='quarter4', className="mr-1",n_clicks = 0, disabled= True if datetime.today().month!=1 else False),
                ],label='Previous Quarters',color='primary',className = 'btn btn-primary',style = {'width':'13%',"textAlign":"center"}, right =True ),
            dbc.Tooltip("Clicking will clear all date filters, even if there is date in date range selector. Hence all date filter needs to apply again",target="clear",
                                style={'font-size':18},placement='left'),
            ],style={'padding': '5px 0px 0px 10px'}
            ),
        dbc.Row([dbc.CardDeck([
                                dbc.Card([dbc.CardHeader("Net Profit or Loss"),
                                             dbc.CardBody(id='netgain', style={"textAlign":"center",'font-size':22})], color="primary", inverse=True,),
                                dbc.Card([dbc.CardHeader("Average Gain per Transaction"),
                                             dbc.CardBody(id='avggain', style={"textAlign":"center",'font-size':22})], color="danger", inverse=True,),
                                dbc.Card([dbc.CardHeader("Total Amount of Stocks Sold"),
                                                   dbc.CardBody(id='totalsell', style={"textAlign":"center",'font-size':22})], color="info", inverse=True,),
                                dbc.Card([dbc.CardHeader("Total Amount of Stocks Bought"),
                                             dbc.CardBody(id='totalbuy', style={"textAlign":"center",'font-size':22})], color="success", inverse=True,),
                                dbc.Card([dbc.CardHeader("Average Sell per Transaction"),
                                                   dbc.CardBody(id='avgsell', style={"textAlign":"center",'font-size':22})], color="secondary", inverse=True,),
                                dbc.Card([dbc.CardHeader("Average Buy per Transaction"),
                                             dbc.CardBody(id='avgbuy', style={"textAlign":"center",'font-size':22})], color="danger", inverse=True,),
                                      ],style ={'padding': '50px 50px 20px 50px'}),
            ]),
        dbc.Row( style={ 'width': '100%', 'height': 30 }
            ),
        dbc.Row(html.Div( 
                    dash_table.DataTable(
                                id = 'stocksJournalTable', 
                                columns=[{"name": i, "id": i,'type': table_type(stocks_Journal[i])} for i in stocks_Journal.columns],
                                style_cell={'minWidth': '118px','width':'118px' ,'maxWidth': '118px','whiteSpace': 'normal','height': 'auto','border': '1px solid grey'},
                                style_table={'border': '1px solid grey'},
                                page_size = 25,
                                #fixed_rows = {'headers':True},
                                style_header={'fontWeight': 'bold'},
                                sort_action='native', 
                                filter_action="native",
                                sort_mode="multi",
                                #virtualization=True,
                            ),
                          style={'width': '100%'}
            )),
        
], style={'padding': '0px 20px 5px 20px'})


@app.callback(
    Output('stocksJournalTable', 'data'),
    Input('clear', 'n_clicks'),
    Input('today', 'n_clicks'),
    Input('week', 'n_clicks'),
    Input('month', 'n_clicks'),
    Input('quarter', 'n_clicks'),
    Input('year', 'n_clicks'),
    Input('quarter1', 'n_clicks'),
    Input('quarter2', 'n_clicks'),
    Input('quarter3', 'n_clicks'),
    Input('quarter4', 'n_clicks'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')
)
def journalLayout(clear, today, week, month, quarter, year, quarter1, quarter2, quarter3, quarter4,start_date, end_date ):
    ctx= dash.callback_context
    if not ctx.triggered:
        buttonId = 'No clicks yet'
    else:
        buttonId = ctx.triggered[0]['prop_id'].split('.')[0]
    
    toDay = datetime.now(tz=timezone.utc).date()
    stocksJournal = DataFrameByButtons(stocks_Journal,buttonId, toDay)
    
    if start_date is not None:
        stocksJournal = stocksJournal[stocksJournal["timestamp"].dt.date >= datetime.strptime(start_date,"%Y-%m-%d").date()]
    if end_date is not None:
        stocksJournal = stocksJournal[stocksJournal["timestamp"].dt.date <= datetime.strptime(end_date,"%Y-%m-%d").date()]
    
    
    return stocksJournal.to_dict('records')


#Define Methods
def DataFrameByButtons(Journal,button_id,day):
    if button_id == 'today':
        returnDf = Journal[Journal["timestamp"].dt.date == day]
    elif button_id == 'week':
        returnDf = Journal[Journal["timestamp"].dt.date >=(day-timedelta(days=day.weekday()+1)) ]
    elif button_id == 'month':
        returnDf = Journal[Journal["timestamp"].dt.date >= day.replace(day=1)]
    elif button_id == 'year':
        returnDf = Journal[Journal["timestamp"].dt.date >= day.replace(month=1,day=1)]
    elif button_id[:7]=='quarter':
        if button_id=='quarter':
            if day.month in range(1,4):
                button_id += "1"
            elif day.month in range(4,6):
                button_id += "2"
            elif day.month in range(6,9):
                button_id += "3"
            else:
                returnDf = Journal[Journal["timestamp"].dt.date.between(datetime(day.year, 9, 1).date(),datetime(day.year, 12, 31).date())]
        if button_id=='quarter1':
            returnDf = Journal[Journal["timestamp"].dt.date.between(datetime(day.year, 1, 1).date(),datetime(day.year, 4, 1).date())]
        elif button_id=='quarter2':
            returnDf = Journal[Journal["timestamp"].dt.date.between(datetime(day.year, 4, 1).date(),datetime(day.year, 6, 1).date())]
        elif button_id=='quarter3':
            returnDf = Journal[Journal["timestamp"].dt.date.between(datetime(day.year, 6, 1).date(),datetime(day.year, 9, 1).date())]
        elif button_id=='quarter4':
            returnDf = Journal[Journal["timestamp"].dt.date.between(datetime(day.year-1, 9, 1).date(),datetime(day.year, 1, 1).date())]
    else:
        returnDf = Journal
    
    return returnDf.copy()


@app.callback(
    Output('totalsell', 'children'),
    Output('totalbuy', 'children'),
    Output('avgsell', 'children'),
    Output('avgbuy', 'children'),
    Output('netgain', 'children'),
    Output('avggain','children'),
    Input('stocksJournalTable', 'derived_virtual_data'))
def update_cards(rows):
    dff =  stocks_Journal if (rows is None) else pd.DataFrame(rows)
    totalsell = dff.sellAmount.sum().round(2) if len(dff) >0 else 0
    totalbuy = dff.buyAmount.sum().round(2) if len(dff) >0 else 0
    avgsell = round(dff.sellAmount.mean(),2) if len(dff) >0 else 0
    avgbuy = round(dff.buyAmount.mean(),2) if len(dff) >0 else 0
    netgain = round(dff.total_gain.sum(),2) if len(dff) >0 else 0
    avggain = round(dff.total_gain.mean(),2) if len(dff) >0 else 0
    return totalsell,totalbuy, avgsell, avgbuy, netgain, avggain