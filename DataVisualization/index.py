#!/usr/bin/python
# -*- coding: utf-8 -*-
from dash import dcc, html
from dash.dependencies import Output, Input

# connection with the main app.py file
from DataVisualization.app import app

# connection with the main app.py file
from DataVisualization import msstockanalysisusingcsv
from dash_auth import BasicAuth
from users.dat_users import *


auth = BasicAuth(app, registered_users)

tabs_styles = {
    'height': '40px'
}
tab_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'padding': '5px',
    'fontWeight': 'bold',
    'backgroundColor': '#92D596'

}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': 'black', #119DFF
    'color': 'white',
    'padding': '5px'
}

app.layout = html.Div([
    html.Div(
        children=[
            html.H1(children="Data Analysis & Visualization")
        ],
        className="header",
    ),
    dcc.Tabs(id="menubar", value='/davi/microsoftstockanalysis', children=[
        dcc.Tab(label='Microsoft Stock', value='/dat/microsoftstockanalysis', style=tab_style, selected_style=tab_selected_style)
    ], style=tabs_styles),
    html.Div(id='menubar_content')
])


@app.callback(Output('menubar_content', 'children'),
              Input('menubar', 'value'))
def main_page(tab):
    if tab == '/davi/microsoftstockanalysis':
        return msstockanalysisusingcsv.page_1_layout
    else:
        return msstockanalysisusingcsv.page_1_layout
