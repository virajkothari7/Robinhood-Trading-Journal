#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  3 19:45:19 2021

@author: viraj
"""
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


layout3 = html.Div(children=[
        dbc.Row(
            style={
                'width': '100%', 'height': 28
                }
            ),    
        dbc.Row(
                dbc.Col(
                    html.H1("Options Journal",
                        style={"textAlign":"center",'font-size':38,'width':"100x"},
                           ) )
            ),
        dbc.Row(
            style={
                'width': '100%', 'height': 15
                }
            ),
        
])