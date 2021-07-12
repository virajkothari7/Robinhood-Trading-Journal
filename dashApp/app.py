#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 17:26:21 2021

@author: viraj
"""

import dash
import dash_bootstrap_components as dbc


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY], suppress_callback_exceptions=True,
                    meta_tags=[{'name': 'viewport','content': "width=device-width, initial-scale=1.0"}] )

server = app.server
