# On import les packages
from dash import html, dcc
from Acceuil_f11 import *

#Page About us
def pageA_layout():
    return html.Div(className='corpslambda',children=[
        html.H1(className='h1acc', children=["ABOUT US"]),
        dcc.Markdown(className="aboutus", dangerously_allow_html = True, children = ['''
        # Sujet
        Dans le cadre de l'UE lifprojet nous avons créé un site web permettant de visuliser les différents apects d'un  
        jeu de données portant principalement sur les décès enregistrés en france. Nous avons représenté ces données de  
        différentes façons tels que par des histogrammes, des cartes ou encore une pyramide d'age.
        <br>
        <br>                                                                             

        # Présentation personnelle
        Nous sommes [Gokana Emmannuel](https://github.com/emmanuelgkn) et [Jofre Coll Vila](https://github.com/Jofrix98), étudiants en Licence Informatique  
        à l'université [Claude Bernard Lyon 1](https://www.univ-lyon1.fr/).
        <br>
        <br>
                                                                                                                                                                  
        # Outils utilisés
        Pour atteindre cet objectif, nous avons opté pour une combinaison de technologies puissantes et flexibles, mettant  
         l'accent sur la simplicité du langage Python.
        <br>
        <br>
                                                                                     
        ### Python :  
        [Python](https://www.python.org/) est unangage de programmation polyvalent, offrant une facilité d'utilisation et  
        une flexibilité pour le traitement des données.
        <br>
        <br>
                                                                                     
        ### Dash (Framework de Python) :  
        Nous avons choisi le framework [Dash](https://dash.plotly.com/) pour créer des applications web interactives. Son utilisation simplifié  
        de Python nous a permis de concevoir des tableaux de bord dynamiques sans nécessiter  
        une expertise approfondie en développement web.
        <br>
        <br>
                                                                                     
        ### Matplotlib (Librairie de Visualisation en Python) :  
        [Matplotlib](https://matplotlib.org/) a été notre choix pour la création de graphiques et de visualisations. Cette librairie nous a permis de représenter  
        de manière claire et informative les tendances et les modèles présents  
        dans les données de décès.
        <br>
        <br>  
                                                                                                                                                                                                                                              
        ### CSS (Cascading Style Sheets) :  
        Nous avons utilisé CSS pour personnaliser l'aspect visuel de notre site. Cela nous a donné un contrôle total sur  
        la présentation, garantissant une expérience utilisateur agréable.
        <br>                                                                         
        <br>
                                                                                                                                 
    '''])
    ])