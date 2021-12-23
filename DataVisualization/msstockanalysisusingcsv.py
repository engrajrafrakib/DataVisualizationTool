#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from pathlib import Path
import pandas as pd
import plotly.express as px
from DataVisualization.index import *

# create TestProject_Folder to keep required files
tp_folder_location = str(Path.home()) + "\\Documents\\"
tp_folder = tp_folder_location + "TestProject_Folder"
if not os.path.exists(tp_folder):
    os.makedirs(tp_folder)
else:
    pass

tp_dataset_folder = tp_folder + "\\dataset"
if not os.path.exists(tp_dataset_folder):
    os.makedirs(tp_dataset_folder)
else:
    pass

data = pd.read_csv(tp_dataset_folder + "\\Microsoft_Stock_Modified.csv")
data['Year'] = pd.to_datetime(data['Date'], format='%d-%m-%Y').dt.strftime('%Y')
data = data.groupby(['Year'])['Volume'].sum().reset_index()
total_ms_volume = data['Volume'].sum()
range_value = data['Volume'].nlargest(2).sum()
fig = px.bar(
    data_frame=data,
    x="Year",
    y="Volume",
    orientation="v",
    text='Volume',
    hover_data={"Year":True,
                "Volume":True
                },
    hover_name='Volume',
    labels={"Volume":"Volume", "Year":"Stock Year"},
    title="Microsoft Stock Overview (Total Volume: " + str(total_ms_volume) + ")<br>(Note: Click on a bar to see more details of that specific Year in the 2nd chart.)",
    template="plotly_white",     # 'plotly_white', 'plotly_dark', 'presentation', 'xgridoff', 'ygridoff', 'gridon', 'none'
    #log_x=True
)
fig.update_traces(textposition="outside", showlegend=False, overwrite=False)

page_1_layout = html.Div([
    html.Div(
        children=dcc.Graph(
            id="ms_chart", config={"displayModeBar": False, 'scrollZoom': True},
            figure=fig,
        ),
        className="card",
        style={'height': '20%', 'width': '100%', 'display': 'inline-block', 'float': 'left', 'color': '#17B897'}
    ),
    html.Div(
        children=dcc.Graph(
            id="monthly_stock",
            config={"displayModeBar": False, 'scrollZoom': True},
            figure={
                'layout':{'title':'Year Specific Stock',
                          'xaxis':{'title':'Month', 'type':'category'},
                          'yaxis':{'title':'Volume'}
                          }
            },
        ),
        className="card",
        style={'height': '20%', 'width': '100%', 'display': 'inline-block', 'float': 'left', 'color': '#17B897', 'text-alignment':'left'}
    )
])



@app.callback(
    [Output(component_id='ms_chart', component_property='figure'), Output(component_id='monthly_stock', component_property='figure')],
    [Input(component_id='ms_chart', component_property='clickData')]
)
def update_ms_chart(clickData):
    data = pd.read_csv(tp_dataset_folder + "\\Microsoft_Stock_Modified.csv")
    data['Year'] = pd.to_datetime(data['Date'], format='%d-%m-%Y').dt.strftime('%Y')
    data = data.groupby(['Year'])['Volume'].sum().reset_index()
    total_ms_volume = data['Volume'].sum()
    fig = px.bar(
        data_frame=data,
        x="Year",
        y="Volume",
        orientation="v",
        text='Volume',
        hover_data={"Year": True,
                    "Volume": True
                    },
        hover_name='Volume',
        labels={"Volume": "Volume", "Year": "Stock Year"},
        title="Microsoft Stock Overview (Total Volume: " + str(total_ms_volume) + ")<br>(Note: Click on a bar to see more details of that specific Year in the 2nd chart.)",
        template="plotly_white"
    )
    fig.update_traces(textposition="outside", showlegend=False, overwrite=False)

    data_2 = pd.read_csv(tp_dataset_folder + "\\Microsoft_Stock_Modified.csv")
    data_2['Year'] = pd.to_datetime(data_2['Date'], format='%d-%m-%Y').dt.strftime('%Y')
    data_2['MonthYear'] = pd.to_datetime(data_2['Date'], format='%d-%m-%Y').dt.strftime('%m-%Y')
    if clickData is not None:
        hoverData_df = pd.DataFrame(clickData['points'])
        year_filter = hoverData_df['x'].values[0]
    else:
        year_filter = '2015'
    mask = (data_2.Year == year_filter)
    filtered_data = data_2.loc[mask, :]

    filtered_data = filtered_data.groupby(['MonthYear'])['Volume'].sum().reset_index()
    total_my_volume = filtered_data['Volume'].sum()
    fig_2 = px.bar(
        data_frame=filtered_data,
        x="MonthYear",
        y="Volume",
        orientation="v",
        text='Volume',
        hover_data={"MonthYear": True,
                    "Volume": True
                    },
        hover_name='Volume',
        labels={"Volume": "Volume", "MonthYear": "Stock MonthYear"},
        title="Monthly Stock (Total Volume: " + str(total_my_volume) + ")",
        template="plotly_white"
    )
    fig_2.update_traces(textposition="outside", showlegend=False, overwrite=False)

    return fig, fig_2