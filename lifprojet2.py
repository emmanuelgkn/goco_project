from dash import Dash, html, dash_table, dcc
import pandas as pd
import plotly.express as px

from lifprojet import *


def page2_layout():
    return html.Div([
    html.Div(
<<<<<<< HEAD
            html.H1("Histograme",
                    style = {"font-family" : "verdana"}),
=======
        html.H1("Histograme",
                style = {"font-family" : "verdana"}),
>>>>>>> origin/Jofrix98
            style = { "background-color" : "antiquewhite"}),
    dcc.Graph(figure=px.histogram(df, x='Sex', y='Age', histfunc='avg'),
              style = {'width' : 500}, id="my-graph")
    # Autres composants pour la page 1
])

layout2 = app.layout