#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  3 16:41:58 2021

@author: viraj
"""
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from app import app
from app import server

from apps import layout,layout1,layout2,layout3,layout4


homelayout = html.Div([
    html.Div([
            dcc.Location(id='url', refresh=True),
            dbc.Nav(children =[
                dbc.NavLink('Instrument View',style={'font-size':24,'fontWeight': '','width': '18%'},href='/instrument', className="nav-link active"),
                dbc.NavLink('Stocks Journal',style={'font-size':28,'width': '20%'},href='/journal/stocks', disabled = False if layout2.layout2 else True, className="nav-link active"),
                dbc.NavLink('Portfolio Overview',style={'font-size':34,'width': '25%'},href='/', className = "nav-link active"),
                dbc.NavLink('Options Journal',style={'font-size':28,'width': '20%'},href='/journal/options', disabled = False if layout3.layout3 else True, className="nav-link active"),
                dbc.DropdownMenu(children =[
                                        #dbc.DropdownMenuItem(divider=True),
                                        #dbc.DropdownMenuItem(divider=True),
                                        dbc.DropdownMenuItem("Pending Orders", href="/orderbook/pending", disabled = False if layout1.pendingOrderslayout else True, style={'font-size':26,'width': '100%','textAlign':'left', 'height': 50}),#className = "navbar navbar-expand-lg navbar-dark bg-primary"),
                                        dbc.DropdownMenuItem("Stocks", href="/orderbook/stocks", disabled = False if layout1.stockslayout else True, style={'font-size':26,'width': '100%','textAlign':'left', 'height': 50}),#className ="navbar navbar-expand-lg navbar-dark bg-primary"),
                                        dbc.DropdownMenuItem("Options", href="/orderbook/options", disabled = False if layout1.optionslayout else True, style={'font-size':26,'width': '100%','textAlign':'left', 'height': 50}),#className = "navbar navbar-expand-lg navbar-dark bg-primary"),
                                        ],
                                    label='Orderbook', in_navbar =True, nav=True, caret=False, right = True,
                                    style={'font-size':25,'width': '10%'},
                                    className ="nav-item navbar-dark bg-primary",color='primary' ),
                ],  className = "navbar navbar-expand-lg navbar-dark bg-primary",
                style={'width': '100%', 'height': 100}
                )], style={'width': '100%'}),
    html.Div(id='page-content', children=[])
    ],style={'width': '100%'})

app.layout = homelayout

# @app.callback(Output('p', 'children'),
#               Input('url', 'pathname'))
# def display_color(pathname):

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        return layout.layout
    elif pathname == '/orderbook/stocks':
        return layout1.stockslayout
    elif pathname == '/orderbook/options':
        return layout1.optionslayout
    elif pathname == '/orderbook/pending':
        return layout1.pendingOrderslayout 
    elif pathname == '/journal/stocks':
        return layout2.layout2
    elif pathname == '/journal/options':
        return layout3.layout3
    elif pathname == '/instrument':
        return layout4.layout4
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)






