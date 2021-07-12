#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  3 19:45:28 2021

@author: viraj
"""
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
from app import app
import dash_table
from Robin_hood import table_type


orderBook = pd.read_csv("orderBook.csv",index_col=0)
orderBook[["fees","price"]]=orderBook[["fees","price"]].round(decimals=2)
stocksJournal = pd.read_csv("orderJournal.csv")
stocksJournal['timestamp'] = pd.to_datetime(stocksJournal['timestamp'])


layout4 = html.Div(children=[
        dbc.Row(
            style={
                'width': '100%', 'height': 30
                }
            ),    
        dbc.Row(
                dbc.Col(html.Div(dbc.Select(
                                  id="select-in",options=[ {"label": f"{i.symbol:<5}  :  {i.name:<26}", "value": i.symbol} for i in orderBook[['symbol','name']].drop_duplicates().itertuples()],
                                  placeholder="Select a Instrument from the list.....",className = "form-select"),className="form-group"),
                        width = {'size':5.75,'offset':4}
                        )
                ),
        html.Div(id = 'select-out')
            
            
        ], style={'padding': '0px 20px 5px 20px'})


@app.callback(
    Output(component_id='select-out', component_property='children'),
    Input('select-in', 'value')
)
def selectOutLayout(value):
    ordrbk = orderBook[orderBook["symbol"]==value].copy()
    if value is None: return None
    return_layout = [
        dbc.Row(style={'width': '100%', 'height': 30}
            ),
        dbc.Row(dbc.Col(
                    html.H1("Stock Journal", style={'font-size':32,'width':"100x"},) )
            ),
        dbc.Row(style={'width': '100%', 'height': 10}
            ),
        dbc.Row( html.Div(
                        dash_table.DataTable(
                                id='instrumnet-table-8', 
                                columns=[{"name": i, "id": i,'type': table_type(stocksJournal[i])} for i in stocksJournal.columns],
                                data = stocksJournal[stocksJournal["stock"]==value].to_dict('records'),#need to change stock to symbol later
                                style_cell={'minWidth': '118px','width':'118px' ,'maxWidth': '118px','whiteSpace': 'normal','height': 'auto','border': '1px solid grey'},
                                style_table={'border': '1px solid grey'},
                                page_size = 25,
                                fixed_rows = {'headers':True},
                                style_header={'fontWeight': 'bold'},
                                sort_action='native', 
                                filter_action="native",
                                sort_mode="multi",
                                virtualization=True,
                    )), style={'width': '100%'}
            ),
        dbc.Row(style={'width': '100%', 'height': 30}
            ),
        dbc.Row(dbc.Col(
                    html.H1("Order Book", style={'font-size':32,'width':"100x"},) )
            ),
        dbc.Row(style={'width': '100%', 'height': 10}
            ),
        dbc.Row( html.Div(
                        dash_table.DataTable(
                                id='instrumnet-table-7', 
                                columns=[{"name": i, "id": i,'type': table_type(ordrbk[i])} for i in ordrbk.columns],
                                data = ordrbk.to_dict('records'),
                                style_cell={'minWidth': '95px', 'maxWidth': '132px','whiteSpace': 'normal','height': 'auto','border': '1px solid grey'},
                                page_size = 20,
                                style_table={'overflowY': 'auto','border': '1px solid black'},
                                fixed_rows = {'headers':True},
                                style_header={'fontWeight': 'bold'},
                                sort_action='native', 
                                filter_action="native",
                                sort_mode="multi",
                                virtualization=True,
                    )), style={'width': '100%'}
            )
        
        ]
    
    return return_layout



