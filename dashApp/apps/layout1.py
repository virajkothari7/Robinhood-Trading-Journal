import plotly.express as px
from datetime import datetime 
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash_table
import pandas as pd
from Robin_hood import table_type

orderBook = pd.read_csv("dashApp/data/orderBook.csv",index_col=0)


orderBookTable = dash_table.DataTable(
                id='datatable-interactivity-3', 
                columns=[{"name": i, "id": i,'type': table_type(orderBook[i])} for i in orderBook.columns],
                data = orderBook.to_dict('records'),
                style_cell={'minWidth': '100px', 'maxWidth': '135px','whiteSpace': 'normal','height': 'auto'},
                page_size = 10,
                style_header={'fontWeight': 'bold'},
                sort_action='native', 
                filter_action="native",
                sort_mode="multi",
                virtualization=True,
            )


layout1 = html.Div(children=[
        dbc.Row(
            style={
                'width': '100%', 'height': 30
                }
            ),    
        dbc.Row(
                dbc.Col(
                    html.H1("Stocks Order Book",
                        style={"textAlign":"center",'font-size':48,'width':"100x"},
                           ) )
            ),
        dbc.Row(
            style={
                'width': '100%', 'height': 20
                }
            ),
        dbc.Row(
            html.Div(orderBookTable),
            style={'width': '100%'}
            )
        
])