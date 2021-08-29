#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 19:14:45 2021

@author: Robinhood-trading-journal
"""
# -*- coding: utf-8 -*-

import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
from dash_table.Format import Format, Group, Scheme
import pandas as pd
from app import table_type

try:
    optionsPortfolio = pd.read_csv("./data/options_portfolio.csv")
except:
    optionsPortfolio = None

try:
    stocksPortfolio = pd.read_csv("./data/stocks_portfolio.csv")
    lastdate = pd.to_datetime(stocksPortfolio['quote_time']).max().date()
    
    
    
    figPie = px.pie(stocksPortfolio, values="Total Investment", names='symbol',
                    labels={'symbol':'STOCK Symbol ','unrealized_gain':'Unrealized Gain '}, 
                    color = "unrealized_gain", height = 500,width = 500, template="plotly_white",
                    color_discrete_sequence= ['rgb(248,54,68)'if i <0 else'rgb(77,175,74)' for i in stocksPortfolio.unrealized_gain])
    figPie.update_layout(title={'text':'Pie-Chart of Portfolio Holdings as of ' + str(lastdate),
                                'font': {'size': 15}},title_x=0.12,title_y=0.95)
    figPie.update_traces(textposition='inside',textinfo = 'percent+label',showlegend = False,
                                  marker=dict(line=dict(color='black', width=0.5)))
    figPie.add_annotation(x=-0.15, y=1.05,xref="paper", yref="paper",showarrow = False,font=dict(size =12),
                                text="This graph shows which investment can affect your poftfolio highly" )
    
    
    
    figBar = px.bar(stocksPortfolio,y='unrealized_gain',x = 'symbol',text = ((stocksPortfolio['unrealized_gain']/stocksPortfolio['Total Investment'])*100).round(2).astype(str) +'%',
                    hover_data=['quote_time', 'quote','average_buy_price'],height = 350,width=1400, labels = {'unrealized_gain' : 'Unrealized Gain'},
                    color = "Total Investment", color_continuous_scale='dense',
                    )
    figBar.update_layout(title={'text':"Investment's Unrealized Gain Bar-Chart as of " + str(lastdate),
                                'font': {'size': 22}},title_x=0.025,title_y=0.97)
    figBar.update_layout(uniformtext_minsize=10, uniformtext_mode='hide',xaxis_tickangle=75)
    figBar.update_xaxes(title=None)
    
    
    
    portfolioTable = dash_table.DataTable(
                    id='datatable-interactivity-1', 
                    columns =[
                        {"name":"Market", "id":"market", "type":table_type(stocksPortfolio['market'])},
                        {"name":"Updated Time", "id":"updated_at", "type":table_type(stocksPortfolio['updated_at'])},
                        {"name":"Name", "id":"market", "type":table_type(stocksPortfolio['market'])},
                        {"name":"Symbol", "id":"symbol","type":table_type(stocksPortfolio['symbol'])},
                        {"name":"Quote Time", "id":"quote_time", "type":table_type(stocksPortfolio['quote_time'])},
                        {"name":"Quote", "id":"quote", "type":table_type(stocksPortfolio['quote']),"format": Format(precision=3, scheme=Scheme.fixed, group=Group.yes, groups=[3])},
                        {"name":"Avg Buy Price", "id":"average_buy_price", "type":table_type(stocksPortfolio['average_buy_price']),"format": Format(precision=3, scheme=Scheme.fixed, group=Group.yes, groups=[3])},
                        {"name":"Qty", "id":"quantity", "type":table_type(stocksPortfolio['quantity']),"format": Format(precision=4, scheme=Scheme.fixed, group=Group.yes, groups=[3])},
                        {"name":"Unrealized Gain", "id":"unrealized_gain", "type":table_type(stocksPortfolio['unrealized_gain']),"format": Format(precision=3, scheme=Scheme.fixed, group=Group.yes, groups=[3])},
                        {"name":"Total Investment", "id":"Total Investment", "type":table_type(stocksPortfolio['Total Investment']),"format": Format(precision=3, scheme=Scheme.fixed, group=Group.yes, groups=[3])}
                        ],
                    data = stocksPortfolio.to_dict('records'),
                    # tooltip_data=[
                    #         {
                    #             column: {'value': f'{row.items()}', 'type': 'markdown'}
                    #             for column, value in row.items()
                    #         } for row in stocksPortfolio.to_dict('records')
                    #     ],
                    # css=[{
                    #         'selector': '.dash-table-tooltip',
                    #         'rule': 'background-color: grey ; font-family: monospace; font-size : 18px ;text-align: center ; border:2px solid black'
                    #     }],
                    style_cell={'minWidth': '140px', 'maxWidth': '145px','whiteSpace': 'normal','height': 'auto'},
                    style_header={'fontWeight': 'bold','backgroundColor': 'rgb(230, 230, 230)',},
                    fixed_rows = {'headers':True},
                    sort_action='native',
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
            return f"Holdings : {investedOptions[0]} \nInvested : {investedOptions[1]}"
    
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
                    style_header={'fontWeight': 'bold','backgroundColor': 'rgb(230, 230, 230)',},
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
                            style={ 'width': '100%', 'height': 20}
                            ),]
            return tableReturn
    
    
    
    layout =html.Div(children=[
            dbc.Row(
                style={
                    'width': '100%', 'height': 25
                    }
                ),    
            dbc.Row(
                dbc.Col(
                    html.H1("Portfolio Overview", style={"textAlign":"center",'font-size':38,'width':"100x"}, 
                    ))
                ),
            dbc.Row(
                style={
                    'width': '100%', 'height': 10
                    }
                ),
            dbc.Row(
                dcc.Graph(figure=figBar),#style={'width':'100%'}
                ),
            dbc.Row([
                    dbc.Col(
                        dcc.Graph( figure=figPie),
                        width = {'size':'30%'} 
                        ),
                    dbc.Col(width = {'size':'10%'} 
                        ),
                    dbc.Col([dbc.CardDeck([dbc.Card([dbc.CardHeader("Stocks Portfolio's \nNet Worth",style = {'white-space':'pre'}),
                                                       dbc.CardBody(f"$ {investedStocks + net}", style={"textAlign":"center",'font-size':22})], color="success" if (net)>0 else "danger", inverse=True,),
                                          dbc.Card([dbc.CardHeader("$$ Unrealized Net"),
                                                       dbc.CardBody(f"$ {net}", style={"textAlign":"center",'font-size':22})], color="success" if net>0 else "danger" , inverse=True,),
                                          dbc.Card([dbc.CardHeader("Best Bet"),
                                                       dbc.CardBody(f"{round(bestBet.unrealized_gain,2)}",style={"textAlign":"center",'font-size':22})],id = 'best',color="success", inverse=True,),
                                          dbc.Card([dbc.CardHeader("Worst Bet"),
                                                       dbc.CardBody(f"{round(worstBet.unrealized_gain,2)}",style={"textAlign":"center",'font-size':22})],id = 'worst', color="danger", inverse=True,),
                                          ],style ={'padding': '50px 20px 20px 50px'}),
                             dbc.CardDeck([dbc.Card([dbc.CardHeader("Invested on Stocks"),
                                                       dbc.CardBody(f"$ {investedStocks}", style={"textAlign":"center",'font-size':22})], color="info", inverse=True,),
                                          dbc.Card([dbc.CardHeader("# Stock Holdings"),
                                                       dbc.CardBody(f"{stocksHolding}", style={"textAlign":"center",'font-size':22})], color="info", inverse=True,),
                                          dbc.Card([dbc.CardHeader("Total Unrealized"),
                                                       dbc.CardBody(f"PROFIT : $ {gain}   \nLOSS   : $ {loss}  ", style={"textAlign":"left",'font-size':16,'white-space':'pre'})], color="primary", inverse=True,),
                                          dbc.Card([dbc.CardHeader("Stock Options"),
                                                       dbc.CardBody(getoptioncard(),style={"textAlign":"left",'font-size':16,'white-space':'pre'})], color="primary", inverse=True,),
                                          dbc.Tooltip(f"Unrealized Gain : {round(bestBet.unrealized_gain,2)} \nSymbol : {bestBet.symbol} \nQuote : {bestBet.quote}"+
                                                          f"\nAvg Buy : {bestBet.average_buy_price} \nQty : {bestBet.quantity} \nTotal Invested : {bestBet['Total Investment']}",
                                                      target="best", style={'font-size':14,'white-space':'pre'},placement='left'),
                                          dbc.Tooltip(f"Unrealized Gain : {round(worstBet.unrealized_gain,2)} \nSymbol : {worstBet.symbol} \nQuote : {worstBet.quote}"+
                                                          f"\nAvg Buy : {worstBet.average_buy_price} \nQty : {worstBet.quantity} \nTotal Invested : {worstBet['Total Investment']}",
                                                      target="worst", style={'font-size':14,'white-space':'pre'},placement='left')
                                          ],style ={'padding': '30px 20px 1px 50px'})
                                     ], width ={'size':'60%'}),
                    
                    ]),
            dbc.Row(dbc.Table(display_option()),style={'width': '100%'}),
            dbc.Row(
                dbc.Col(
                    html.H2("Stocks Portfolio Sheet",
                            style={"textAlign":"center",'font-size':28},
                           )
                    ),
                    style={'width': '100%', 'height': 50}
                ),
               
            dbc.Row(
                dbc.Table(portfolioTable,bordered=True,hover=True),
                style={'width': '100%'}
                )
        ], style={'padding': '0px 20px 20px 20px','width': '100%'})

except FileNotFoundError:
    if optionsPortfolio is not None:
        layout =html.Div(children=[
            dbc.Row(
                style={
                    'width': '100%', 'height': 25
                    }
                ),    
            dbc.Row(
                dbc.Col(
                    html.H1("Portfolio Overview", style={"textAlign":"center",'font-size':38,'width':"100x"}, 
                    ))
                ),
            dbc.Row(
                style={
                    'width': '100%', 'height': 10
                    }
                ),
            dbc.Row(
                dbc.Col(
                    html.H2("Stock Options Portfolio Sheet",
                            style={"textAlign":"center",'font-size':28},
                           )
                    ),
                    style={'width': '100%', 'height': 50}
                ),
            dbc.Row(
                dash_table.DataTable(
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
                    style_header={'fontWeight': 'bold','backgroundColor': 'rgb(230, 230, 230)',},
                    sort_action='native', 
                    filter_action="native",
                    sort_mode="multi",
                ),
                    style={'width': '100%'} 
                ),
            dbc.Row(
                style={ 'width': '100%', 'height': 20}
                ),])
    else :
        layout =html.Div(children=[
            dbc.Row(
                style={
                    'width': '100%', 'height': 25
                    }
                ),    
            dbc.Row(
                dbc.Col(
                    html.H1("Portfolio Overview", style={"textAlign":"center",'font-size':38,'width':"100x"}, 
                    ))
                ),
            dbc.Row(
                style={
                    'width': '100%', 'height': 10
                    }
                ),
            dbc.Row(
                dbc.Col(
                    html.H2("There are no position to show in portfolio because Stocks Portfolio is empty as well as Stock Options Portfolio is empty.", style={"textAlign":"center",'font-size':24,'width':"100x"}, 
                    ))
                ),])


