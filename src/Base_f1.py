# On import les packages
from dash import Dash, html, dash_table, dcc
import pandas as pd
import plotly.express as px
import numpy as np

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

grouped_df_birth = merged_df_birth.groupby('Nom').agg({
    'longitude_birth': 'first',  # Utilisez 'first' pour obtenir le premier valeur non nulle.
    'latitude_birth': 'first',   # Utilisez 'first' pour obtenir le premier valeur non nulle.
}).reset_index()


# Fusionnez les données de décès avec les données de naissance en utilisant la colonne "Nom" comme clé
merged_df = merged_df_death.merge(grouped_df_birth[['Nom', 'longitude_birth', 'latitude_birth']], on='Nom', how='left')
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
app = Dash(__name__, suppress_callback_exceptions=True, assets_folder='../assets')

# App layout
def Accueil_layout():
    return html.Div([
        html.Title("Goco Project"),
        html.H1("STATISTIQUES SUR LES DONNEES DE DECES")
    ])

def page1_layout():
    return html.Div([
        html.Div(
            html.H1("Tableau df",
                    style = {"font-family" : "verdana"}),
            style = { "background-color" : "antiquewhite"}),
        dash_table.DataTable(data=df.to_dict('records'), page_size=10),

        html.Div(
            html.H1("Tableau df_merged",
                    style = {"font-family" : "verdana"}),
            style = { "background-color" : "antiquewhite"}),
        dash_table.DataTable(data=merged_df.to_dict('records'), page_size=10),
    ])