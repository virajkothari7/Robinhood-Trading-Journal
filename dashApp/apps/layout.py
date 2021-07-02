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


stocksPortfolio = pd.read_csv("dashApp/data/stocks_portfolio.csv",index_col=0)
optionsPortfolio = pd.read_csv("dashApp/data/options_portfolio.csv",index_col=0)


figPie = px.pie(stocksPortfolio, values="Total Investment", names='symbol',
                labels={'symbol':'STOCK Symbol ','unrealized_gain':'Unrealized Gain '}, 
                color = "unrealized_gain", height = 650,width = 650, template="plotly_white",
                color_discrete_sequence= ['rgb(248,54,68)'if i <0 else'rgb(77,175,74)' for i in stocksPortfolio.unrealized_gain])

figPie.update_layout(title={'text':'Investment Pie Chart as of ' + str(datetime.today().date()),
                            'font': {'size': 22}},title_x=0.2,title_y=0.95)

figPie.update_traces(textposition='inside',textinfo = 'percent+label',showlegend = False,
                              marker=dict(line=dict(color='black', width=0.5)))

figPie.add_annotation(x=-0.05, y=-0.05,xref="paper", yref="paper",showarrow = False,font=dict(size =16),
                            text="This graph shows which investment can affect your poftfolio highly" )



portfolioTable = dash_table.DataTable(
                id='datatable-interactivity-1', 
                columns=[{"name": i, "id": i,'type': table_type(stocksPortfolio[i])} for i in stocksPortfolio.columns],
                data = stocksPortfolio.to_dict('records'),
                style_cell={'minWidth': '120px', 'maxWidth': '175px','whiteSpace': 'normal','height': 'auto'},
                style_header={'fontWeight': 'bold'},
                sort_action='native',
                style_table={'height': '1500px', 'overflowY': 'auto'},
                fixed_rows = {'headers':True},
                filter_action="native",
                sort_mode="multi",
            )

optionsPortfolioTable = dash_table.DataTable(
                id='datatable-interactivity-2', 
                columns=[{"name": i, "id": i,'type': table_type(optionsPortfolio[i])} for i in optionsPortfolio.columns],
                data = optionsPortfolio.to_dict('records'),
                style_cell={'minWidth': '60px', 'maxWidth': '80px','whiteSpace': 'normal','height': 'auto'},
                style_table={'height': '560px', 'overflowY': 'auto'},
                style_header={'fontWeight': 'bold'},
                sort_action='native', 
                filter_action="native",
                sort_mode="multi",
            )


layout =html.Div(children=[
        dbc.Row(
            style={
                'width': '100%', 'height': 30
                }
            ),    
        dbc.Row(
                dbc.Col(
                    html.H1("Portfolio Overview",
                        style={"textAlign":"center",'font-size':48,'width':"100x"},
                           ) )
            ),
        dbc.Row(
            style={
                'width': '100%', 'height': 20
                }
            ),
        dbc.Row([
                dbc.Col(
                    dcc.Graph( figure=figPie),
                    width = {'size':"4.5px"} 
                    ),
                dbc.Col(
                    [
                    dbc.Row(
                        style={ 'width': '100%', 'height': 24}
                            ), 
                    dbc.Row(
                        dbc.Col(
                            html.H3("Stock Options Portfolio Sheet",
                                style={"textAlign":"center",'font-size':24,'width':"100x"},
                                   )    
                       )),
                    dbc.Row(
                        style={ 'width': '100%', 'height': 32}
                            ), 
                    dbc.Row(html.Div(optionsPortfolioTable),
                            style={'width': '100%'} )
                    ],
                    width={'size':6,'offset':"0.5px"}                    
                )
            ]),
        dbc.Row(
            style={
                'width': '100%', 'height': 25
                }
            ),
        dbc.Row(
            dbc.Col(
                html.H2("Stocks Portfolio Sheet",
                        style={"textAlign":"center",'font-size':36},
                       )
                ),
                style={'width': '100%', 'height': 70}
            ),
        dbc.Row(
            style={
                'width': '100%', 'height': 15
                }
            ),   
        dbc.Row(
            html.Div(portfolioTable),
            style={'width': '100%'}
            )
    ])




