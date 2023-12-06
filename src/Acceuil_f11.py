# On import les packages
from dash import html, dcc
from Deplacements_f10 import *

# App layout
def Accueil_layout():
    return html.Div(className='corpsacceuil',children=[
        html.H1(className='h1acc', children=["STATISTIQUES SUR LES DONNEES DE DECES"]),
        html.Div(className='row row0',children=[
            dcc.Markdown(className="text-acceuil",children=['''
                            Bienvenue sur notre plateforme dédiée à l'analyse approfondie des données de décès. Avez-vous envie de connaître où les gens de votre ville ou pays se déplacent? 
                            Voulez-vous savoir d'où vient votre prénom ou nom famille? Ou encore connaître des statistiques très intéressantes? Ce site est alors fait pour vous!
                            Explorez les tendances et les schémas, analysez et comprenez les dynamiques des décès de manière accessible et enrichissante grâce à nos outils interactifs et visuels. 
                        ''']),

        ]),
        html.Div(className='row row1',children=[

            html.Div(className='col', children=[
                html.H1(className='h',children=["Cartes"]),
                html.P("Nous avons fait plusieurs cartes interactives pour visualiser les mouvements de population, le nombre de morts et les origines d'un prénom ou d'un nom famille", className="text-acceuil"),
                html.Button(html.A("Visiter", className="button",href="/CarteMouvements"))
            ]),

            html.Div(className='col', children=[
                html.A(html.Div(className='card card1'),href="/CarteMouvements"),
                html.A(html.Div(className='card card2'),href="/CarteDeces"),
                html.A(html.Div(className='card card3'),href="/CarteMouvements"),
                html.A(html.Div(className='card card4'),href="/MesOrigines"),
                
            ]),

        ]),
        html.Div(className='row row2',children=[
            html.Div(className='col colr21', children=[
                html.H1(className='h',children=["Graphiques"]),
                html.P("Nous avons fait plusieurs graphiques pour représenter l'âge de la population et aussi la distance moyenne parcourue", className="text-acceuil"),
                html.Button(html.A("Visiter", className="button",href="/GraphesAge"))
            ]),

            
            html.Br(),
            
            html.Div(className='col colr22', children=[

                html.A(html.Div(className='card graph1'),href="/GraphesAge"),
                html.A(html.Div(className='card graph2'),href="/DistanceParcourue"),
                
            ])
        ])
    ]) 