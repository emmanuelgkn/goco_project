# On import les packages
from dash import html, dcc
from Deplacements_f10 import *

# App layout
def Accueil_layout():
    return html.Div(className='corpsacceuil',children=[
        html.H1(className='h1acc', children=["STATISTIQUES SUR LES DONNEES DE DECES"]),
        html.Div(className='row row0',children=[
            dcc.Markdown(className="text-acceuil",children=['''
                            Bienvenue sur notre plateforme dédiée à l'analyse approfondie des données de décès. Explorez les tendances et les schémas qui émergent de ces informations cruciales grâce à nos outils interactifs et visuels. 
                            Notre page d'accueil offre une vue complète et captivante de divers aspects liés aux décès, avec une interface conviviale pour une expérience utilisateur optimale.
                            Explorez, analysez et comprenez les dynamiques des décès de manière accessible et enrichissante.
                        ''']),

        ]),
        html.Div(className='row row1',children=[

            html.Div(className='col', children=[
                html.H1(className='h',children=["Cartes"]),
                html.P("Nous avons fait plusieurs cartes"),
                html.Button(html.A("Visiter", className="button",href="/page3"))
            ]),

            html.Div(className='col', children=[
                html.A(html.Div(className='card card1'),href="http://127.0.0.1:8080/page3"),
                html.A(html.Div(className='card card2'),href="http://127.0.0.1:8080/page6"),
                html.A(html.Div(className='card card3'),href="http://127.0.0.1:8080/page3"),
                html.A(html.Div(className='card card4'),href="http://127.0.0.1:8080/page9"),
                
            ]),

        ]),
        html.Div(className='row row2',children=[
            html.Div(className='col colr21', children=[
                html.H1(className='h',children=["Graphiques"]),
                html.P("Nous avons fait plusieurs Graphiques"),
                html.Button(html.A("Visiter", className="button",href="http://127.0.0.1:8080/page8"))
            ]),

            
            html.Br(),
            
            html.Div(className='col colr22', children=[

                html.A(html.Div(className='card graph1'),href="http://127.0.0.1:8080/page8"),
                html.A(html.Div(className='card graph2'),href="http://127.0.0.1:8080/page7"),
                # html.Div(className='card graph3'),
                # html.Div(className='card graph4'),
                
            ])
        ])
    ]) 