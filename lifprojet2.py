from dash import Dash, html, dash_table, dcc
import pandas as pd
import plotly.express as px

from lifprojet import *
app = Dash(__name__)

app.layout = html.Div([
    html.H1("GRAPHIQUE"),
    dcc.Graph(figure=px.histogram(df, x='Sex', y='Age', histfunc='avg'),
              style = {'width' : 500}, id="my-graph")
    # Autres composants pour la page 1
])

layout2 = app.layout