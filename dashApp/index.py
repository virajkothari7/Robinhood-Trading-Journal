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
                dbc.NavLink('Instrument View',style={'font-size':26},href='/instrument',className="nav-link active"),
                dbc.NavLink('Stocks Journal',style={'font-size':32},href='/journal/stocks',className="nav-link active"),
                dbc.NavLink('Portfolio Overview',style={'font-size':40,},href='/',className = "nav-link active"),
                dbc.NavLink('Options Journal',style={'font-size':32},href='/journal/options',className="nav-link active"),
                dbc.DropdownMenu(children =[
                                        dbc.DropdownMenuItem("Options", href="/orderbook/options",style={'font-size':26,'width': '100%','textAlign':'right', 'height': 50},className = "navbar navbar-expand-lg navbar-dark bg-primary"),
                                        #dbc.DropdownMenuItem(divider=True),
                                        dbc.DropdownMenuItem("Stocks", href="/orderbook/stocks",style={'font-size':26,'width': '100%','textAlign':'right', 'height': 50},className ="navbar navbar-expand-lg navbar-dark bg-primary"),
                                        #dbc.DropdownMenuItem(divider=True),
                                        dbc.DropdownMenuItem("Pending Orders", href="/orderbook/pending",style={'font-size':26,'width': '100%','textAlign':'right', 'height': 50},className = "navbar navbar-expand-lg navbar-dark bg-primary")],
                                    label='Orderbook',in_navbar =True, nav=True, caret=False, right = True,
                                    style={'font-size':27},
                                    className ="nav-item navbar-dark dropdown" ),
                ],  className = "navbar navbar-expand-lg navbar-dark bg-primary",
                style={'width': '100%', 'height': 115}
                )]),
    html.Div(id='page-content', children=[])
    ])

app.layout = homelayout


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        return layout.layout
    elif pathname == '/orderbook/stocks':
        return layout1.stockslayout
    elif pathname == '/orderbook/options':
        return layout1.optionslayout
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