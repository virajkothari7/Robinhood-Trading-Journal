#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  3 19:45:19 2021

@author: Robinhood-trading-journal
"""
import dash
from datetime import datetime,timezone,timedelta 
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_table
from dash_table.Format import Format, Group, Scheme, Symbol
import pandas as pd
from app import app, table_type
import plotly.express as px


try:
    options_Journal = pd.read_csv("./data/options_journal.csv")
    options_Journal['timestamp'] = pd.to_datetime(options_Journal['timestamp'])
    options_Journal['gainPercent'] = (options_Journal['total_gain']/options_Journal['buyAmount'])*100
        
    
    
    layout3 = html.Div(children=#[dcc.Store(id='memory'),
        [
            dbc.Row( style={ 'width': '100%', 'height': 15 }
                ),    
            
            dbc.Row( dbc.Col( html.H1("Options Journal",
                                      style={"textAlign":"center",'font-size':38,'width':"100x"},
                                ))
                ),
            
            dbc.Row( style={ 'width': '100%', 'height': 10 }
                ),
            dbc.Row( html.H4("Select dates from date range or predefined date range for date filter.",style={'font-size':18,'padding': '0px 20px 0px 20px'})
                ,style={ 'width': '100%'}
                ),
            
            dbc.Row([
                dcc.DatePickerRange(
                    id='option-date-picker-range',
                    min_date_allowed = min(options_Journal['timestamp']).date(),
                    max_date_allowed= max(options_Journal['timestamp']).date(),
                    display_format='MM/DD/YYYY',
                    number_of_months_shown = 4,
                    with_portal  = True,
                    day_size=44, initial_visible_month = min(options_Journal['timestamp']).date() + (max(options_Journal['timestamp']).date()- min(options_Journal['timestamp']).date())/2,
                    clearable=True,persistence=True,persistence_type = 'memory',
                    
                    style = {'width':'27%',"textAlign":"center",'padding': '3px 0px 0px 0px'},
                    
                    ),
                dbc.Button("Clear",id='o_clear', color="primary", className="mr-1",n_clicks = 0,style = {'width':'8%',"textAlign":"center"}),
                dbc.Button("Today",id= 'o_today', color="primary",className="mr-1",n_clicks = 0,style = {'width':'8%',"textAlign":"center"}),
                dbc.Button("This Week",id = 'o_week', color="primary", className="mr-1",n_clicks = 0,style = {'width':'10%',"textAlign":"center"}),
                dbc.Button("This Month",id = 'o_month', color="primary", className="mr-1",n_clicks = 0,style = {'width':'10%',"textAlign":"center"}),
                dbc.Button("This Quarter",id='o_quarter', color="primary", className="mr-1",n_clicks = 0,style = {'width':'11%',"textAlign":"center"}),
                dbc.Button("This Year",id='o_year', color="primary", className="mr-1",n_clicks = 0,style = {'width':'10%',"textAlign":"center"}),
                dbc.DropdownMenu([
                    dbc.DropdownMenuItem("Quarter 1 : Jan/01 - Mar/31",id='o_quarter1', className="mr-1",n_clicks = 0, disabled= True if datetime.today().month<=3 else False),
                    dbc.DropdownMenuItem("Quarter 2 : Apr/01 - May/31",id='o_quarter2', className="mr-1",n_clicks = 0, disabled= True if datetime.today().month<=5 else False),
                    dbc.DropdownMenuItem("Quarter 3 : Jun/01 - Aug/31",id='o_quarter3', className="mr-1",n_clicks = 0, disabled= True if datetime.today().month<=8 else False),
                    dbc.DropdownMenuItem("Quarter 4 : Sep/01 - Dec/31",id='o_quarter4', className="mr-1",n_clicks = 0, disabled= True if datetime.today().month!=1 else False),
                    ],label='Previous Quarters',color='primary',className = 'btn btn-primary',style = {'width':'13%',"textAlign":"center"}, right =True ),
                dbc.Tooltip("Clicking will clear all pre-defined date filters, if there is date in date range selector dataframe will obey date range.",target="o_clear",
                                    style={'font-size':18},placement='left'),
                ],style={'padding': '5px 0px 0px 10px','width':'100%' }
                ),
            dbc.Row(dbc.Col(dbc.Collapse(dbc.CardDeck([dbc.Card([dbc.CardHeader("$$ Biggest Winner"),
                                                      dbc.CardBody(id='o_winner', style={"textAlign":"center",'font-size':18})], color="success", inverse=True,),
                                        dbc.Card([dbc.CardHeader("$$ Biggest Loser"),
                                                      dbc.CardBody(id='o_loser', style={"textAlign":"center",'font-size':18})], color="danger", inverse=True,),
                                        dbc.Card([dbc.CardHeader("$$ Average Win"),
                                                      dbc.CardBody(id='o_avgprofit', style={"textAlign":"center",'font-size':18})], color="success", inverse=True,),
                                        dbc.Card([dbc.CardHeader("$$ Average Loss"),
                                                      dbc.CardBody(id='o_avgloss', style={"textAlign":"center",'font-size':18})], color="danger", inverse=True,),
                                        dbc.Card([dbc.CardHeader("$$ Average Sell per Transaction"),
                                                    dbc.CardBody(id='o_avgsell', style={"textAlign":"center",'font-size':18})], color="info", inverse=True,),
                                        dbc.Card([dbc.CardHeader("$$ Average Buy per Transaction"),
                                                    dbc.CardBody(id='o_avgbuy', style={"textAlign":"center",'font-size':18})], color="info", inverse=True,),
                                            ],style ={'padding': '20px 15px 0px 15px'}),
                                         id='o_collapse-row',is_open=False),style ={'width': '100%',})),
            dbc.Row(dbc.CardDeck([dbc.Card([dbc.CardHeader("$$ Net Profit/Loss"),
                                                dbc.CardBody(id='o_netgain', style={"textAlign":"center",'font-size':18})],id='o_netgaincard', inverse=True,),
                                        dbc.Card([dbc.CardHeader("$$ Average Gain per Transaction"),
                                                    dbc.CardBody(id='o_avggain', style={"textAlign":"center",'font-size':18})], id="o_avggaincard", inverse=True,),
                                        dbc.Card([dbc.CardHeader("$$ Total Gross Profit"),
                                                      dbc.CardBody(id='o_totalgain', style={"textAlign":"center",'font-size':18})], color='success', inverse=True,),
                                        dbc.Card([dbc.CardHeader("$$ Total Gross Loss"),
                                                      dbc.CardBody(id='o_totalloss', style={"textAlign":"center",'font-size':18})], color="danger", inverse=True,),
                                        dbc.Card([dbc.CardHeader("$$ Total Stock Options Sold "),
                                                    dbc.CardBody(id='o_totalsell', style={"textAlign":"center",'font-size':18})], color="info", inverse=True,),
                                        dbc.Card([dbc.CardHeader("$$ Total Stock Options Bought"),
                                                    dbc.CardBody(id='o_totalbuy', style={"textAlign":"center",'font-size':18})], color="info", inverse=True,),
                                              ],style ={'width': '100%','padding': '20px 0px 10px 30px'})),
            dbc.Row(dbc.CardDeck([dbc.Card([dbc.CardHeader("%% Net Profit/Loss"),
                                                      dbc.CardBody(id='o_percentavggain', style={"textAlign":"center",'white-space':'pre','font-size':18})], id="o_percentavggaincard", inverse=True,),
                                    dbc.Card([dbc.CardHeader("% Win Rate"),
                                                  dbc.CardBody(id='o_winrate', style={"textAlign":"center",'font-size':18})],id='o_winratecard', inverse=True,),
                                    dbc.Card([dbc.CardHeader("% Profit Rate"),
                                                  dbc.CardBody(id='o_profitrate', style={"textAlign":"center",'font-size':18})], id="o_profitratecard", inverse=True,),
                                    dbc.Card([dbc.CardHeader("P/L: Profit Factor"),
                                                  dbc.CardBody(id='o_profitfactor', style={"textAlign":"center",'font-size':18})], id="o_profitfactorcard", inverse=True,),
                                    dbc.Card([dbc.CardHeader("$$ APPT : Average Profitability / Trade"),
                                                  dbc.CardBody(id='o_profitibility', style={"textAlign":"center",'font-size':18})], id="o_profitibilitycard", inverse=True,),
                                    dbc.Card(dbc.CardBody([html.P("Click to show or hide Detailed View",style={'font-size':15},),
                                                           dbc.Button( id='o_card-collapse',n_clicks = 0 ,style={"textAlign":"center",'width':'100%','font-size':18,'white-space':'pre'},color="primary")],style={"textAlign":"center"}),color='secondary'),
                                    dbc.Tooltip("This can also identified as Expected Profit Target or Expected Value",target="o_profitibilitycard",
                                                style={'font-size':18},placement='top'),             
                                    ],style ={'width': '100%','padding': '10px 0px 5px 30px'})),
            dbc.Row( style={ 'width': '100%', 'height': 10 }
                ),
            dbc.Row([
                dbc.Col([
                    dbc.Row(html.H4("\n         Select Inputs for Bar-Chart\n",style={"white-space":"pre",'font-size':22,'width':"100x",'height':65},),style={"textAlign":"center"}),
                    dbc.Row([html.A("Select X-Axis:",style={"textAlign":"center","font-size":16}),
                             dbc.Select(id="o_x-select", persistence = True, persistence_type='memory',
                                        options= [{"label":"Row","value":"row"},
                                                  {"label":"Date (Day)" , "value": "date"},
                                                  {"label":"Date (Month)" , "value": "month"},
                                                  {"label":"Symbol" , "value": "symbol"} ], value = 'row' ),
                             ],style={'height':100}),
                    dbc.Row([html.A("Select Y-Axis:",style={"textAlign":"center","font-size":16}),
                             dbc.Select(id="o_y-select",persistence = True, persistence_type='memory',
                                        options= [ {"label":"Total Gain","value":"total_gain"},
                                                  {"label":"Percentage  Gain" , "value": "gainPercent"},
                                                  {"label":"Buy Amount" , "value": "buyAmount"},
                                                  {"label":"Sell Amount" , "value": "sellAmount"},
                                                  {"label":"Quantity" , "value": "sellQty"}
                                                  ], value = 'total_gain'),
                             ],style={'height':100}),
                    # dbc.Row([html.A("Symbol Groups",style={"textAlign":"center","font-size":16}),
                    #          dbc.Select(id="x-select",persistence = True, persistence_type='memory',
                    #                     options= [ {"label":"Total Gain","value":"total_gain"},
                    #                               {"label":"Percentage  Gain" , "value": "gainPercent"},
                    #                               {"label":"Buy Amount" , "value": "buyAmount"},
                    #                               {"label":"Sell Amount" , "value": "sellAmount"},
                    #                               {"label":"Quantity" , "value": "sellQty"}
                    #                               ], value = 'total_gain'),
                    #          ],style={'height':70}),
                    
                    ],width=3),
                dbc.Col(
                    dcc.Graph(id='options-barchart'),
                    width=9),
                ],style={ 'width': '100%', 'height': 350 }),
            dbc.Row( style={ 'width': '100%', 'height': 20 }
                ),
            dbc.Row(html.Div( 
                        dash_table.DataTable(
                                    id = 'optionsJournalTable', 
                                    columns=[
                                        {"name":"Timestamp" , "id": "timestamp" ,'type': table_type(options_Journal["timestamp"])},
                                        {"name": "Symbol", "id": "symbol",'type': table_type(options_Journal["symbol"])},
                                        {"name": "Option Name", "id": "optionName",'type': table_type(options_Journal["optionName"])},
                                        {"name": "Option Type", "id": "optionType",'type': table_type(options_Journal["optionType"])},
                                        {"name": "Sell Qty", "id": "sellQty",'type': table_type(options_Journal["sellQty"]),"format": Format(precision=3, scheme=Scheme.fixed, group=Group.yes, groups=[3])},
                                        {"name": "Sell Price", "id": "sellPrice",'type': table_type(options_Journal["sellPrice"]),"format": Format(precision=3, scheme=Scheme.fixed, group=Group.yes, groups=[3])},
                                        {"name": "Avg Buy Price", "id": "avgBuyPrice",'type': table_type(options_Journal["avgBuyPrice"]),"format": Format(precision=3, scheme=Scheme.fixed, group=Group.yes, groups=[3])},
                                        {"name": "Profit/Loss per Contract", "id": "profit_loss/option",'type': table_type(options_Journal[ "profit_loss/option"]),"format": Format(precision=3, scheme=Scheme.fixed, group=Group.yes, groups=[3])},
                                        {"name": "Sell Amount", "id": "sellAmount",'type': table_type(options_Journal["sellAmount"]),"format": Format(precision=3, scheme=Scheme.fixed, group=Group.yes, groups=[3])},
                                        {"name": "Buy Amount", "id": "buyAmount" ,'type': table_type(options_Journal["buyAmount"]),"format": Format(precision=3, scheme=Scheme.fixed, group=Group.yes, groups=[3])},
                                        {"name": "Total Gain", "id": "total_gain",'type': table_type(options_Journal['total_gain']),"format": Format(precision=3, scheme=Scheme.fixed, group=Group.yes, groups=[3])},
                                        {"name": "Percentage Gain %%", "id": "gainPercent",'type':'numeric',"format": Format(precision=2,symbol=Symbol.yes, symbol_suffix=' %', scheme=Scheme.fixed,)}
                                        ],
                                    style_cell={'minWidth': '110px','width':'110px' ,'maxWidth': '110px','whiteSpace': 'normal','height': 'auto','border': '1px solid grey'},
                                    style_table={'border': '1px solid grey'},
                                    style_data_conditional=[
                                            {
                                                'if': {
                                                    'filter_query': '{total_gain} lt 0',
                                                    'column_id':['total_gain','gainPercent'], #Commenting this will color whole row istead of a column  
                                                },
                                                'backgroundColor': '#FF4136',
                                                'color': 'white'
                                            },
                                            {
                                                'if': {
                                                    'filter_query': '{total_gain} ge 0',
                                                    'column_id':['total_gain','gainPercent'], #Commenting this will color whole row istead of a column  
                                                },
                                                'backgroundColor': 'green',
                                                'color': 'white'
                                            },
                                            ],
                                    page_size = 50,
                                    fixed_rows = {'headers':True},
                                    style_header={'fontWeight': 'bold','backgroundColor': 'rgb(230, 230, 230)',},
                                    sort_action='native', 
                                    filter_action="native",
                                    sort_mode="multi",persistence=True,persistence_type = 'memory',
                                    #virtualization=True,
                                ),
                              style={'width': '100%'}
                )),
            
    ], style={'padding': '0px 20px 5px 20px'})
    
    
     
    @app.callback(
        Output("options-barchart","figure"),
        Input("o_x-select","value"),
        Input("o_y-select","value"),
        Input('optionsJournalTable', 'derived_virtual_data'),
        )
    def stock_barChart(X,Y,rows):
        dff = options_Journal.copy() if (rows is None) else pd.DataFrame(rows)
        label = {"row":"Row","date":"Date (Day)","month":"Date (Month)","symbol":"Symbol",
                 "total_gain":"Total Gain","gainPercent":"Percentage  Gain" ,
                "buyAmount":"Buy Amount" , "sellAmount":"Sell Amount" ,"sellQty":"Quantity"  }
                                                  
        if len(dff) <=5:
            return  px.bar(y=None,x=None, height = 300,width=1050,)
                    
        dff['timestamp'] = pd.to_datetime(dff['timestamp'])
        dff['date'] = dff['timestamp'].dt.date
        dff = dff.round(2)
            
        if X =="date" or X == "month" or X=="symbol":
            dff['month'] = dff['timestamp'].dt.strftime('%b %Y')#[ f"{str(i[0])[-2:]} - {i[1]}" for i in zip(dff['timestamp'].dt.year ,dff['timestamp'].dt.month)]
            dff = dff.groupby([X])[["sellQty","sellAmount","buyAmount","total_gain"]].sum().round(2)
            dff['gainPercent'] = ((dff['total_gain'] /dff['buyAmount'])*100).round(2)
            dff = dff.reset_index()
            if X=='month':
                dff['sortmonth'] = pd.to_datetime(dff['month'])
                dff = dff.sort_values('sortmonth',ascending =False).drop('sortmonth',axis=1)
        
        Labels= {'gainPercent':'%% Percentage<br> Gain ','symbol':'Symbol ','total_gain':'$$ Total Gain ','buyAmount':'$$ Buy Amount ',
                 "sellQty":"Quantity","sellAmount":"$$ Sell Amount ",'date':'Date ',"month":"Month ","timestamp":"Timestamp " ,
                 "avgBuyPrice":"Avg Buying Price ","sellPrice":"Selling Price ","optionName": "Name ","profit_loss/option":"P&L per Option "}
        if X == "date" : 
            day = datetime.now().date()
            f_day = str(day-timedelta(days=50))
            day=str(day)
            figBar = px.bar(dff, y=Y,x=None if X == 'row' else X, height = 370,width=1050,text=Y,
                        hover_data=list(dff.columns),labels = Labels,hover_name = X,template="plotly_white",
                        color = Y,color_continuous_midpoint =0, color_continuous_scale=["red","green"])
            figBar.update_layout(title={'text':f"Bar Plot for {label[X]} over {label[Y]}"},title_x=0.075,title_y=0.925)
            figBar.update_xaxes(title=None,tickangle= 45,nticks= 50)
            figBar.update_yaxes(zeroline=True,zerolinewidth=2, zerolinecolor='Black')
            
            ## I am not able to figure out on how to handel visible range here
            figBar.update_xaxes(autorange="reversed",)
            figBar.update_xaxes(range=[day,f_day])
            return figBar
        
        figBar = px.bar(dff, y=Y,x=None if X == 'row' else X, height = 370,width=1050,text=Y,template="plotly_white",
                        hover_data=list(dff.columns),labels = Labels,hover_name= dff.index if X == 'row' else X,
                        color = Y,color_continuous_midpoint =0, color_continuous_scale=["red","green"])
        figBar.update_layout(title={'text':f"Bar Plot for {label[X]} over {label[Y]}"},title_x=0.075,title_y=0.925)
        figBar.update_xaxes(title=None,tickangle= 45,nticks= 25)
        figBar.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor='Black')
        
        if X == "row" or X=="month": figBar.update_xaxes( type="category")
        
        return figBar


    @app.callback(
        Output("o_collapse-row","is_open"),
        Output("o_card-collapse","children"),
        [Input("o_card-collapse", "n_clicks")],
        [State("o_collapse-row", "is_open")])
    def collapseMathod(n,is_open):
        if n:
            if is_open:
                return (not is_open), 'Expand +'
            return (not is_open), 'Compress -'
        return is_open, 'Expand +'
    
    
    @app.callback(
        Output('optionsJournalTable', 'data'),
        Input('o_clear', 'n_clicks'),
        Input('o_today', 'n_clicks'),
        Input('o_week', 'n_clicks'),
        Input('o_month', 'n_clicks'),
        Input('o_quarter', 'n_clicks'),
        Input('o_year', 'n_clicks'),
        Input('o_quarter1', 'n_clicks'),
        Input('o_quarter2', 'n_clicks'),
        Input('o_quarter3', 'n_clicks'),
        Input('o_quarter4', 'n_clicks'),
        Input('option-date-picker-range', 'start_date'),
        Input('option-date-picker-range', 'end_date')
    )
    def journalLayout(o_clear, o_today, o_week, o_month, o_quarter, o_year, o_quarter1, o_quarter2, o_quarter3, o_quarter4,start_date, end_date ):
        ctx= dash.callback_context
        if not ctx.triggered:
            buttonId = 'No clicks yet'
        else:
            buttonId = ctx.triggered[0]['prop_id'].split('.')[0]
        
        toDay = datetime.now(tz=timezone.utc).date()
        optionsJournal = DataFrameByButtons(options_Journal,buttonId, toDay)
        
        if start_date is not None:
            optionsJournal = optionsJournal[optionsJournal["timestamp"].dt.date >= datetime.strptime(start_date,"%Y-%m-%d").date()]
        if end_date is not None:
            optionsJournal = optionsJournal[optionsJournal["timestamp"].dt.date <= datetime.strptime(end_date,"%Y-%m-%d").date()]
        
        
        return optionsJournal.to_dict('records')
    
    
    #Define Methods
    def DataFrameByButtons(Journal,button_id,day):
        if button_id == 'o_today':
            returnDf = Journal[Journal["timestamp"].dt.date == day]
        elif button_id == 'o_week':
            returnDf = Journal[Journal["timestamp"].dt.date >=(day-timedelta(days=day.weekday()+1)) ]
        elif button_id == 'o_month':
            returnDf = Journal[Journal["timestamp"].dt.date >= day.replace(day=1)]
        elif button_id == 'o_year':
            returnDf = Journal[Journal["timestamp"].dt.date >= day.replace(month=1,day=1)]
        elif button_id[:9]=='o_quarter':
            if button_id=='o_quarter':
                if day.month in range(1,4):
                    button_id += "1"
                elif day.month in range(4,6):
                    button_id += "2"
                elif day.month in range(6,9):
                    button_id += "3"
                else:
                    returnDf = Journal[Journal["timestamp"].dt.date.between(datetime(day.year, 9, 1).date(),datetime(day.year, 12, 31).date())]
            if button_id=='o_quarter1':
                returnDf = Journal[Journal["timestamp"].dt.date.between(datetime(day.year, 1, 1).date(),datetime(day.year, 4, 1).date())]
            elif button_id=='o_quarter2':
                returnDf = Journal[Journal["timestamp"].dt.date.between(datetime(day.year, 4, 1).date(),datetime(day.year, 6, 1).date())]
            elif button_id=='o_quarter3':
                returnDf = Journal[Journal["timestamp"].dt.date.between(datetime(day.year, 6, 1).date(),datetime(day.year, 9, 1).date())]
            elif button_id=='o_quarter4':
                returnDf = Journal[Journal["timestamp"].dt.date.between(datetime(day.year-1, 9, 1).date(),datetime(day.year, 1, 1).date())]
        else:
            returnDf = Journal
        
        return returnDf.copy()
    
    
    
    @app.callback(
        Output('o_totalsell', 'children'),
        Output('o_totalbuy', 'children'),
        Output('o_avgsell', 'children'),
        Output('o_avgbuy', 'children'),
        Output('o_netgain', 'children'),
        Output('o_avggain','children'),
        Output('o_totalgain','children'),
        Output('o_totalloss','children'),
        Output('o_avgprofit','children'),
        Output('o_avgloss','children'),
        Output('o_winner','children'),
        Output('o_loser','children'),
        Output('o_winrate','children'),
        Output('o_profitrate','children'),
        Output('o_profitfactor','children'),
        Output('o_profitibility','children'),
        Output('o_percentavggain','children'),
        Output('o_netgaincard', 'color'),
        Output('o_avggaincard','color'),
        Output('o_winratecard','color'),
        Output('o_profitratecard','color'),
        Output('o_profitfactorcard','color'),
        Output('o_profitibilitycard','color'),
        Output('o_percentavggaincard','color'),
        Input('optionsJournalTable', 'derived_virtual_data'))
    def update_cards(rows):
        dff =  options_Journal if (rows is None) else pd.DataFrame(rows)
        if len(dff) <=0:
            return [0]*17 +["danger"]*7
        totalsell = dff.sellAmount.sum().round(2)
        totalbuy = dff.buyAmount.sum().round(2) 
        avgsell = round(dff.sellAmount.mean(),2)
        avgbuy = round(dff.buyAmount.mean(),2) 
        netgain = round(dff.total_gain.sum(),2) 
        avggain = round(dff.total_gain.mean(),2)
        totalgain = round(dff.total_gain[dff.total_gain>=0].sum(),2) 
        totalloss = round(dff.total_gain[dff.total_gain<0].sum(),2) 
        avgprofit = round(dff.total_gain[dff.total_gain>=0].mean(),2) 
        avgprofit = 0 if str(avgprofit) == 'nan' else avgprofit
        avgloss = round(dff.total_gain[dff.total_gain<0].mean(),2) 
        avgloss = 0 if str(avgloss) == 'nan' else avgloss
        winner = round(dff.iloc[dff.total_gain.idxmax()].total_gain,2)
        loser = round(dff.iloc[dff.total_gain.idxmin()].total_gain,2)
        loser = loser if loser < 0 else None
        winingtrade = len(dff.total_gain[dff.total_gain>=0])
        winrate = round((winingtrade/len(dff))*100,2)
        profitrate = round((totalgain/(totalgain + abs(totalloss)))*100,2) if (totalgain + abs(totalloss)) != 0 else 0
        profitfactor = round(totalgain/abs(totalloss),2) if totalloss != 0 else None
        profitibility = round((winrate*avgprofit -((100-winrate)*abs(avgloss)))/100,2) if avgloss != 0 else None
        percentavggain = round((netgain/totalbuy)*100,2) 
        
        #Card Colors
        netgain_color = "success" if (netgain)>0 else "danger"
        avggain_color = "success" if (avggain)>0 else "danger"
        winratecard = "success" if (winrate)>51 else "danger"#Card Color
        profitratecard = "success" if (profitrate)>51 else "danger"
        profitfactorcard = "success" if (profitfactor is not None) and (profitfactor)>1.25  else "danger"
        profitibilitycard = "success" if (profitibility is not None) and (profitibility)>0  else "danger"
        percentavggaincard = "success" if  percentavggain > 0 else "danger"
        return [totalsell,totalbuy, avgsell, avgbuy, netgain, avggain, totalgain, totalloss, avgprofit,
                avgloss, winner,loser, f"{winrate} %", f"{profitrate} %", profitfactor, profitibility, f"{percentavggain} %",
                netgain_color, avggain_color, winratecard, profitratecard, profitfactorcard, profitibilitycard,  percentavggaincard ]

except FileNotFoundError:
    layout3 = None


