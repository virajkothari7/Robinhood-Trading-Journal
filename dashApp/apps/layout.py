#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 19:14:45 2021

@author: viraj
"""
# -*- coding: utf-8 -*-

import plotly.express as px
from datetime import datetime 
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash_table
import plotly.figure_factory as ff
import pandas as pd
from Robin_hood import table_type
from app import app
import os

stocksPortfolio = pd.read_csv("stocks_portfolio.csv",index_col=0)
optionsPortfolio = pd.read_csv("options_portfolio.csv",index_col=0)



figPie = px.pie(stocksPortfolio, values="Total Investment", names='symbol',
                labels={'symbol':'STOCK Symbol ','unrealized_gain':'Unrealized Gain '}, 
                color = "unrealized_gain", height = 475,width = 475, template="plotly_white",
                color_discrete_sequence= ['rgb(248,54,68)'if i <0 else'rgb(77,175,74)' for i in stocksPortfolio.unrealized_gain])

figPie.update_layout(title={'text':'Pie-Chart of Portfolio Holdings as of ' + str(datetime.today().date()),
                            'font': {'size': 15}},title_x=0.12,title_y=0.95)

figPie.update_traces(textposition='inside',textinfo = 'percent+label',showlegend = False,
                              marker=dict(line=dict(color='black', width=0.5)))

figPie.add_annotation(x=-0.15, y=1.05,xref="paper", yref="paper",showarrow = False,font=dict(size =12),
                            text="This graph shows which investment can affect your poftfolio highly" )



figBar = px.bar(stocksPortfolio,y='unrealized_gain',x = 'symbol',text = ((stocksPortfolio['unrealized_gain']/stocksPortfolio['Total Investment'])*100).round(2).astype(str) +'%',
                hover_data=['quote_time', 'quote','average_buy_price'],height = 350,width = 1400,labels = {'unrealized_gain' : 'Unrealized Gain'},
                color = "Total Investment", color_continuous_scale='dense',
                )
figBar.update_layout(title={'text':"Investment's Unrealized Gain Bar-Chart as of " + str(datetime.today().date()),
                            'font': {'size': 22}},title_x=0.025,title_y=0.97)
figBar.update_layout(uniformtext_minsize=10, uniformtext_mode='hide',xaxis_tickangle=75)
figBar.update_xaxes(title=None)



portfolioTable = dash_table.DataTable(
                id='datatable-interactivity-1', 
                columns=[{"name": i, "id": i,'type': table_type(stocksPortfolio[i])} for i in stocksPortfolio.columns],
                data = stocksPortfolio.to_dict('records'),
                # tooltip_data=[
                #         {
                #             column: {'value': f'{value}', 'type': 'markdown'}
                #             for column, value in row.items()
                #         } for row in stocksPortfolio.to_dict('records')
                #     ],
                # css=[{
                #         'selector': '.dash-table-tooltip',
                #         'rule': 'background-color: white ; font-family: monospace; font-size : 18px ;text-align: center ; border:2px solid Tomato'
                #     }],
                style_cell={'minWidth': '105px', 'maxWidth': '175px','whiteSpace': 'normal','height': 'auto'},
                style_header={'fontWeight': 'bold'},
                sort_action='native',
                style_table={'height': '700px', 'overflowY': 'auto'},
                fixed_rows = {'headers':True},
                filter_action="native",
                sort_mode="multi",
            )




investedStocks = stocksPortfolio['Total Investment'].sum().round(2)
gain = stocksPortfolio[stocksPortfolio['unrealized_gain']>=0]['unrealized_gain'].sum().round(2)
loss = stocksPortfolio[stocksPortfolio['unrealized_gain']<0]['unrealized_gain'].sum().round(2)
net = stocksPortfolio['unrealized_gain'].sum().round(2)

stocksHolding = stocksPortfolio['symbol'].size
bestBet = stocksPortfolio.iloc[stocksPortfolio['unrealized_gain'].idxmax()]
worstBet = stocksPortfolio.iloc[stocksPortfolio['unrealized_gain'].idxmin()]


def getoptioncard():
    if optionsPortfolio is None :
        return None
    else:
        investedOptions = [optionsPortfolio['optionName'].size ,optionsPortfolio['Total Investment'].sum().round(2)]
        return f"Holdings : {investedOptions[0]} Invested : {investedOptions[1]}"

def display_option():
    if optionsPortfolio is None :
        return
    else:
        optionsPortfolioTable = dash_table.DataTable(
                id='datatable-interactivity-2', 
                columns=[{"name": "Chain Symbol", "id": 'chain_symbol','type': table_type(optionsPortfolio['chain_symbol'])},
                         {"name": "Option Name", "id": 'optionName','type': table_type(optionsPortfolio['optionName'])} ,
                         {"name": "Avg Buy Price", "id": 'average_buy_price','type': table_type(optionsPortfolio['average_buy_price'])} ,
                         {"name": "Qty", "id": 'quantity','type': table_type(optionsPortfolio['quantity'])} ,
                         {"name": "Strike Price", "id": 'strikePrice','type': table_type(optionsPortfolio['strikePrice'])} ,
                         {"name": "Option Type", "id": 'optionType','type': table_type(optionsPortfolio['optionType'])} ,
                         {"name": "Exp Date", "id": 'expDate','type': table_type(optionsPortfolio['expDate'])} ,
                         {"name": "State", "id": 'state','type': table_type(optionsPortfolio['state'])} ,
                         {"name": "Type", "id": 'type','type': table_type(optionsPortfolio['type'])} ,
                         {"name": "Total Invested", "id": 'Total Investment','type': table_type(optionsPortfolio['Total Investment'])} ,
                         ],
                data = optionsPortfolio.to_dict('records'),
                style_cell={'minWidth': '130px', 'maxWidth': '170px','whiteSpace': 'normal','height': 'auto'},
                style_table={'overflowY': 'auto'},
                style_header={'fontWeight': 'bold'},
                sort_action='native', 
                filter_action="native",
                sort_mode="multi",
            )

        tableReturn =[dbc.Row(
                        dbc.Col(
                            html.H2("Stock Options Portfolio Sheet",
                                    style={"textAlign":"center",'font-size':28},
                                   )
                            ),
                            style={'width': '100%', 'height': 50}
                        ),
                    dbc.Row(html.Div(optionsPortfolioTable),
                            style={'width': '100%'} 
                        ),
                    dbc.Row(
                        style={ 'width': '100%', 'height': 35}
                        ),]
        return tableReturn



layout =html.Div(children=[
        dbc.Row(
            style={
                'width': '100%', 'height': 35
                }
            ),    
        dbc.Row(
            dbc.Col(
                html.H1("Portfolio Overview", style={"textAlign":"center",'font-size':38,'width':"100x"}, 
                ))
            ),
        dbc.Row(
            style={
                'width': '100%', 'height': 25
                }
            ),
        dbc.Row(
            dcc.Graph(figure=figBar)
            ),
        dbc.Row([
                dbc.Col(
                    dcc.Graph( figure=figPie),
                    width = {'size':'30%'} 
                    ),
                dbc.Col(width = {'size':'10%'} 
                    ),
                dbc.Col([dbc.CardDeck([dbc.Card([dbc.CardHeader("Invested on Stocks"),
                                                   dbc.CardBody(f"$ {investedStocks}", style={"textAlign":"center",'font-size':22})], color="info", inverse=True,),
                                      dbc.Card([dbc.CardHeader("Total Unrealized Profit"),
                                                   dbc.CardBody(f"$ {gain}", style={"textAlign":"center",'font-size':22})], color="success", inverse=True,),
                                      dbc.Card([dbc.CardHeader("Total Unrealized Loss"),
                                                   dbc.CardBody(f"$ {loss}", style={"textAlign":"center",'font-size':22})], color="danger", inverse=True,),
                                      dbc.Card([dbc.CardHeader("$$ Unrealized Net"),
                                                   dbc.CardBody(f"$ {net}", style={"textAlign":"center",'font-size':22})], color="secondary", inverse=True,),
                                      ],style ={'padding': '50px 50px 20px 70px'}),
                         dbc.CardDeck([dbc.Card([dbc.CardHeader("# Stock Holdings"),
                                                   dbc.CardBody(f"{stocksHolding}", style={"textAlign":"center",'font-size':22})], color="info", inverse=True,),
                                      dbc.Card([dbc.CardHeader("Best Bet"),
                                                   dbc.CardBody(f"{round(bestBet.unrealized_gain,2)}",style={"textAlign":"center",'font-size':22})],id = 'best',color="success", inverse=True,),
                                      dbc.Card([dbc.CardHeader("Worst Bet"),
                                                   dbc.CardBody(f"{round(worstBet.unrealized_gain,2)}",style={"textAlign":"center",'font-size':22})],id = 'worst', color="danger", inverse=True,),
                                      dbc.Card([dbc.CardHeader("Stock Options"),
                                                   dbc.CardBody(getoptioncard(),style={"textAlign":"left",'font-size':16})], color="primary", inverse=True,),
                                      dbc.Tooltip(f"Unrealized Gain : {round(bestBet.unrealized_gain,2)} \nSymbol : {bestBet.symbol} \nQuote : {bestBet.quote}"+
                                                      f"\nAvg Buy : {bestBet.average_buy_price} \nQty : {bestBet.quantity} \nTotal Invested : {bestBet['Total Investment']}",
                                                  target="best", style={'font-size':14,'white-space':'pre'},placement='left'),
                                      dbc.Tooltip(f"Unrealized Gain : {round(worstBet.unrealized_gain,2)} \nSymbol : {worstBet.symbol} \nQuote : {worstBet.quote}"+
                                                      f"\nAvg Buy : {worstBet.average_buy_price} \nQty : {worstBet.quantity} \nTotal Invested : {worstBet['Total Investment']}",
                                                  target="worst", style={'font-size':14,'white-space':'pre'},placement='left')
                                      ],style ={'padding': '20px 50px 0px 70px'})
                                 ], width ={'size':'50%'}),
                
                ]),
        html.Div(display_option()),
        dbc.Row(
            dbc.Col(
                html.H2("Stocks Portfolio Sheet",
                        style={"textAlign":"center",'font-size':28},
                       )
                ),
                style={'width': '100%', 'height': 50}
            ),
           
        dbc.Row(
            html.Div(portfolioTable),
            style={'width': '100%'}
            )
    ], style={'padding': '0px 20px 20px 20px'})




