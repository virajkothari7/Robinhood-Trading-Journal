#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 17:26:21 2021

@author: Robinhood-trading-journal
"""

import dash
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY], suppress_callback_exceptions=True,
                    meta_tags=[{'name': 'viewport','content': "width=device-width, initial-scale=1.0"}] )

server = app.server


def table_type(df_column):
    # Note - this only works with Pandas >= 1.0.0
    if isinstance(df_column.dtype, pd.DatetimeTZDtype):
        return 'datetime'
    elif (isinstance(df_column.dtype, pd.StringDtype) or
            isinstance(df_column.dtype, pd.BooleanDtype) or
            isinstance(df_column.dtype, pd.CategoricalDtype) or
            isinstance(df_column.dtype, pd.PeriodDtype)):
        return 'text'
    elif (isinstance(df_column.dtype, pd.SparseDtype) or
            isinstance(df_column.dtype, pd.IntervalDtype) or
            isinstance(df_column.dtype, pd.Int8Dtype) or
            isinstance(df_column.dtype, pd.Int16Dtype) or
            isinstance(df_column.dtype, pd.Int32Dtype) or
            isinstance(df_column.dtype, pd.Int64Dtype) or
            (df_column.dtype == np.float_)):
        return 'numeric'
    else:
        return 'any'