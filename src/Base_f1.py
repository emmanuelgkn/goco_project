# On import les packages
from dash import Dash, html, dash_table, dcc
import pandas as pd
import plotly.express as px
import numpy as np
import dash_daq as daq
import dash_bootstrap_components as dbc


# On lit le jeu de données des décès en France ligne par ligne
lines = []
with open("data/deces-2023-m08.txt", "r") as file:
    lines = file.readlines()

# On charge le jeu de données pour pouvoir connaître la position géographique des villes en France
positions_geo = pd.read_csv('data/communes-departement-region.csv', usecols=[0, 1, 5, 6])


# On lit le jeu de données des positions des pays étrangers ligne par ligne
with open("data/positions-pays-étrangers.txt", "r") as file2:
    country_data = file2.readlines()

# On ajoute un 0 dans le cas où les codes on seulement 4 chiffres
positions_geo['code_commune_INSEE'] = positions_geo['code_commune_INSEE'].str.zfill(5)


# On initialise les listes vides pour chaque colonne du tableau
names = []
gender = []
dob = []
birthplace_code_list = []
birthplace = []
birthplace_details = []
year_list = []
dod = []
deathplace_code = []
death_cert_number = []
noms = []
prenoms = []
Age = []
same_places = []
deathplace = []

# Créez un dictionnaire pour stocker les correspondances deathplace_code_text -> birthplace_text
deathplace_mapping = {}

# Boucle pour extraire les données et trouver les correspondances
for line in lines:
    name = line[0:80].strip()
    nom, prenom = name.split('*')
    prenom = prenom.strip('/')
    gender_code = line[80:81]
    date_year = line[81:85]
    date_month = line[85:87]
    date_day = line[87:89]
    birthplace_code = line[89:94].strip()
    birthplace_text = line[94:124].strip()
    birthplace_details_text = line[124:154].strip()
    date_of_death_year = line[154:158]
    date_of_death_month = line[158:160]
    date_of_death_day = line[160:162]
    deathplace_code_text = line[162:167].strip()
    death_cert_number_text = line[167:176].strip()
    age = int(date_of_death_year) - int(date_year)

    # On doit convertir le code du genre en string
    if gender_code == '1':
        gender_text = "Masculin"
    elif gender_code == '2':
        gender_text = "Féminin"
    else:
        gender_text = "Inconnu"

    if birthplace_details_text == '':
        birthplace_details_text = "FRANCE"

    if deathplace_code_text == birthplace_code:
        new_place = (deathplace_code_text, birthplace_text)
        if new_place not in same_places:
            same_places.append(new_place)

        # Stockez la correspondance dans le dictionnaire
        deathplace_mapping[deathplace_code_text] = birthplace_text

    names.append(name)
    gender.append(gender_text)
    year_list.append(date_year)
    dob.append(date_day + "/" + date_month + "/" + date_year)
    birthplace_code_list.append(birthplace_code)
    birthplace.append(birthplace_text)
    birthplace_details.append(birthplace_details_text)
    dod.append(date_of_death_day + "/" + date_of_death_month + "/" + date_of_death_year)
    deathplace_code.append(deathplace_code_text)
    death_cert_number.append(death_cert_number_text)
    noms.append(nom)
    prenoms.append(prenom)
    Age.append(age)

# Boucle principale pour le traitement des lignes
for line in lines:
    deathplace_code_text = line[162:167].strip()
    deathplace_value = deathplace_mapping.get(deathplace_code_text, "NULL")
    deathplace.append(deathplace_value)

# Créez le tableau à partir des listes créées
data = {
    "Nom": noms,
    "Prenom(s)": prenoms,
    "Sex": gender,
    "Year": year_list,
    "Date of Birth": dob,
    "Age": Age,
    "Birthplace Code": birthplace_code_list,
    "Birthplace": birthplace,
    "Birthplace Details": birthplace_details,
    "Date of Death": dod,
    "Deathplace Code": deathplace_code,
    "Death Certificate Number": death_cert_number,
    "Death Place": deathplace,
}

# Créez le DataFrame avec pandas
df = pd.DataFrame(data)


# On crée un DataFrame avec toute l'information ensemble pour pouvoir comparer les Villes avec leur position géographique
# Realizar la fusión para las coordenadas de muerte
positions_geo.drop_duplicates(inplace=True)
merged_df_death = df.merge(positions_geo, left_on='Deathplace Code', right_on='code_commune_INSEE', how='left')
merged_df_death = merged_df_death.rename(columns={'longitude': 'longitude_death', 'latitude': 'latitude_death'})


merged_df_birth = df.merge(positions_geo, left_on='Birthplace Code', right_on='code_commune_INSEE', how='left')
merged_df_birth = merged_df_birth.rename(columns={'longitude': 'longitude_birth', 'latitude': 'latitude_birth'})

# Fusionnez les données de décès avec les données de naissance en utilisant la colonne "Nom" comme clé
merged_df = merged_df_death.merge(merged_df_birth[['longitude_birth', 'latitude_birth']], left_index=True, right_index=True, how='left')
merged_df.loc[merged_df['Birthplace Details'] != 'FRANCE', ['latitude_birth', 'longitude_birth']] = np.nan

country_coordinates = {}

for line in country_data:
    parts = line.strip().split()
    if len(parts) == 3:
        country = parts[0].replace('*', ' ')
        latitude, longitude = parts[1], parts[2]
        country_coordinates[country] = (latitude, longitude)

def update_coordinates(row):
    country = row['Birthplace Details']
    if country in country_coordinates:
        latitude, longitude = country_coordinates[country]
        row['latitude_birth'] = latitude
        row['longitude_birth'] = longitude
    return row

merged_df = merged_df.apply(update_coordinates, axis=1)
merged_df['density'] = 1

# Initialisez l'application Dash
app = Dash(__name__, suppress_callback_exceptions=True, assets_folder='../assets', external_stylesheets=[dbc.themes.DARKLY])

theme = {
    'dark': True,
    'detail': '#007439',
    'primary': '#00EA64',
    'secondary': '#6E6E6E',
}


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
                html.Button(html.A("Visiter", className="button",href="/page8"))
            ]),
            html.Div(className='col colr22', children=[
                html.A(html.Div(className='card graph1'),href="http://127.0.0.1:8080/page8"),
                html.A(html.Div(className='card graph2'),href="http://127.0.0.1:8080/page7"),
                # html.Div(className='card graph3'),
                # html.Div(className='card graph4'),
                
            ])
        ])
    ]) 

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

def page1_layout():
    return html.Div(className='corpslambda',children=[
        html.H1("Tableau df"),
        dash_table.DataTable(data=df.to_dict('records'), page_size=10, style_data={
                'color': '#e0e0e0',
                'backgroundColor': 'rgb(50, 50, 50)',
                'fontWeight': 'bold',
            },
            style_cell={'padding': '5px'},
            style_header={
                'color': '#e0e0e0',
                'backgroundColor': 'rgb(30, 30, 30)',
                'fontWeight': 'bold',
            },),

        html.H1("Tableau df_merged"),
        dash_table.DataTable(data=merged_df.to_dict('records'), page_size=10, style_data={
                'color': '#e0e0e0',
                'backgroundColor': 'rgb(50, 50, 50)',
                'fontWeight': 'bold',
            },
            style_cell={'padding': '5px'},
            style_header={
                'color': '#e0e0e0',
                'backgroundColor': 'rgb(30, 30, 30)',
                'fontWeight': 'bold',
            },),
    ])