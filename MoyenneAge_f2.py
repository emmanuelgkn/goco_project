from dash import Dash, html, dash_table, dcc
import pandas as pd
import plotly.express as px

from Base_f1 import *


def page2_layout():
    return html.Div([
    html.Div(
        html.H1("Histograme",
                style = {"font-family" : "verdana"}),
            style = { "background-color" : "antiquewhite"}),
    dcc.Graph(figure=px.histogram(df, x='Sex', y='Age', histfunc='avg'),
              style = {'width' : 500}, id="my-graph")
    # Autres composants pour la page 1
])

layout2 = app.layout