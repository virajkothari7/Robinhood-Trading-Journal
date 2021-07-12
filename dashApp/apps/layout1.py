import plotly.express as px
from datetime import datetime 
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash_table
import pandas as pd
from Robin_hood import table_type
from app import app


orderBook = pd.read_csv("orderBook.csv",index_col=0)
orderBook[["fees","price"]]=orderBook[["fees","price"]].round(decimals=2)

orderBookTable = dash_table.DataTable(
                id='datatable-interactivity-3', 
                columns=[{"name": i, "id": i,'type': table_type(orderBook[i])} for i in orderBook.columns],
                data = orderBook.to_dict('records'),
                style_cell={'minWidth': '95px', 'maxWidth': '132px','whiteSpace': 'normal','height': 'auto'},
                page_size = 50,
                style_table={'height': '480px', 'overflowY': 'auto'},
                fixed_rows = {'headers':True},
                style_header={'fontWeight': 'bold'},
                sort_action='native', 
                filter_action="native",
                sort_mode="multi",
                virtualization=True,
            )


optionslayout = html.Div(children=[
        dbc.Row(
            style={
                'width': '100%', 'height': 28
                }
            ),    
        dbc.Row(
                dbc.Col(
                    html.H1("Options Order Book",
                        style={"textAlign":"center",'font-size':38,'width':"100x"},
                           ) )
            ),
        dbc.Row(
            style={
                'width': '100%', 'height': 15
                }
            ),
        
])

stockslayout = html.Div(children=[
        dbc.Row(
            style={
                'width': '100%', 'height': 30 
                }
            ),    
        dbc.Row(
                dbc.Col(
                    html.H1("Stocks Order Book",
                        style={"textAlign":"center",'font-size':38,'width':"100x"},
                           ) )
            ),
        dbc.Row(
            style={
                'width': '100%', 'height': 15
                }
            ),
        dbc.Row(
            html.Div(orderBookTable),
            style={'width': '100%'}
            )
        
],style={'padding': '0px 20px 5px 20px'})
