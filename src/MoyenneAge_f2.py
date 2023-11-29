from dash import Dash, html, dash_table, dcc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from Base_f1 import *

# Dans ce fichier on ne fait que les calculs de graphiques, l'affichage ce fait dans Page8_layout() dans PyramideAge_f8

df_moyenne = df.copy()
df_moyenne['Date of Birth'] = pd.to_datetime(df_moyenne['Date of Birth'], format='%d/%m/%Y', errors='coerce')
# On crée une nouvelle colonne 'Year of Birth' avec l'année de naissance
df_moyenne['Year of Birth'] = df_moyenne['Date of Birth'].dt.year.fillna(-1).astype('int')

fig_HF = px.histogram(df, 
                      x='Sex', 
                      y='Age', 
                      histfunc='avg',
                      color='Sex',  # On a utilisé l'argument color pour spécifier la couleur des barres en fonction du genre
                      color_discrete_map={'Masculin': 'lightblue', 'Féminin': 'crimson'},
                      title = 'Espérance de vie moyenne en fonction du genre')

fig_HF.update_traces(marker_color=None, selector={'name': 'Masculin'})
fig_HF.update_layout(
    xaxis_title='Genre',
    yaxis_title='Âge moyen',
    plot_bgcolor= '#292A30',
    paper_bgcolor= '#292A30',
    font_color='#e0e0e0'
)

fig_esperance = make_subplots(specs=[[{"secondary_y": True}]])

fig_esperance.add_trace(go.Scatter(x=df_esp['Year'], y=df_esp['Esperance Hommes'], mode='lines+markers', name='Hommes'), secondary_y=False,)

fig_esperance.add_trace(go.Scatter(x=df_esp['Year'], y=df_esp['Esperance Femmes'], mode='lines+markers', name='Femmes'), secondary_y=False,)

fig_esperance.add_trace(go.Scatter(x=df_esp['Year'], y=df_esp['Mortalité infantile'], mode='lines+markers', name='Taux mortalité infantile en %'), secondary_y=True,)

fig_esperance.update_yaxes(title_text="Espérance de vie", secondary_y=False)
fig_esperance.update_yaxes(title_text="Taux mortalité infantile en %", secondary_y=True)

fig_esperance.update_layout(
    title_text='Espérance de vie en fonction du genre et taux de mortalité infantile en pourcentage selon l\'année',
    xaxis_title='Année',
    plot_bgcolor='#292A30',
    paper_bgcolor='#292A30',
    font_color='#e0e0e0'
)