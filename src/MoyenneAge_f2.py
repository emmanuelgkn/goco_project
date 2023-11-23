from dash import Dash, html, dash_table, dcc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from Base_f1 import *

df_moyenne = df.copy()
df_moyenne['Date of Birth'] = pd.to_datetime(df_moyenne['Date of Birth'], format='%d/%m/%Y', errors='coerce')
# Créez une nouvelle colonne 'Year of Birth' avec l'année de naissance
df_moyenne['Year of Birth'] = df_moyenne['Date of Birth'].dt.year.fillna(-1).astype('int')

fig_HF = px.histogram(df, 
                      x='Sex', 
                      y='Age', 
                      histfunc='avg',
                      color='Sex',  # Utilisez l'argument color pour spécifier la couleur des barres en fonction du genre
                      color_discrete_map={'Masculin': 'lightblue', 'Féminin': 'crimson'},
                      title = 'Esperence de vie moyenne en fonction du Genre')

fig_HF.update_traces(marker_color=None, selector={'name': 'Masculin'})
fig_HF.update_layout(
    xaxis_title='Genre',  # Renommez l'axe x
    yaxis_title='Âge moyen',
    plot_bgcolor= '#292A30',
    paper_bgcolor= '#292A30',
    font_color='#e0e0e0'
)


avg_age_by_year = df_moyenne.groupby('Year of Birth')['Age'].mean().reset_index()
scatter_trace = go.Scatter(x=avg_age_by_year['Year of Birth'], y=avg_age_by_year['Age'], mode='lines+markers')

# Créez le graphique avec les deux tracés
fig_moyenne = go.Figure(data=[scatter_trace])

# Mettez à jour la mise en page pour spécifier l'intervalle d'années sur l'axe des x
fig_moyenne.update_layout(
    title_text='Age moyen de mort en fonction de l\'année de décès',
    xaxis_title='Année de naissance',
    yaxis_title='Âge moyen',
    xaxis=dict(
        range=[1900, 2025],
        dtick=5
    ),
    plot_bgcolor= '#292A30',
    paper_bgcolor= '#292A30',
    font_color='#e0e0e0'
)

def page2_layout():
    return html.Div(className='corpslambda',children=[
    html.H1("Grapues"),
     html.Br(),
            dcc.Markdown(className="manu", children="""
                Ce graphe representent le nombre de morts dans les 4 villes plus grandes en France.
            """),
    html.Br(),
    dcc.Graph(figure=fig_HF),
    dcc.Graph(figure = fig_moyenne)
    # Autres composants pour la page 1
])





