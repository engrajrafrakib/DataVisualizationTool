#!/usr/bin/python
# -*- coding: utf-8 -*-
import dash

app = dash.Dash(__name__, suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
app.title = "DaVi: Data Visualization!"
server = app.server