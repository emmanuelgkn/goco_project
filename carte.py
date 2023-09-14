# On import les packages
from dash import Dash, html, dash_table, dcc
import pandas as pd
import plotly.express as px

# Importez le module dash.dependencies pour gérer les callbacks
from dash.dependencies import Input, Output

# On lit le jeu de données ligne par ligne
lines = []
with open("./deces-2023-m08.txt", "r") as file:
    lines = file.readlines()

# On initialise les listes vides pour chaque colonne du tableau
names = []
gender = []
dob = []
birthplace_code_list = []
birthplace = []
birthplace_details = []
dod = []
deathplace_code = []
death_cert_number = []
noms = []
prenoms = []
Age = []

#je fais un teste la

# On fait une itération sur chaque ligne pour extraire les données selon la position et la longueur du format de la base
# On utilse stip() pour effacer les espaces en blanc au début et à la fin

for line in lines:
    name = line[0:80].strip()
    nom, prenom = name.split('*')
    prenom = prenom.strip('/')
    gender_code = line[80:81]  # On garde le code du genre (1 = Masculin, 2= Féminin)
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
        gender_text = "Inconnu"  # Au cas où ce ne serait pas spécifié

    if birthplace_details_text == '':
        birthplace_details_text = "FRANCE"
        

    # On fait un append de l'information de la ligne qu'on a traité à la liste du tableau
    names.append(name)
    gender.append(gender_text)
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

# On crée le tableau à partir des listes qu'on a créé
data = {
    "Nom": noms,
    "Prenom(s)": prenoms,
    "Sex": gender,
    "Date of Birth": dob,
    "Age": Age,
    "Birthplace Code": birthplace_code_list,
    "Birthplace": birthplace,
    "Birthplace Details": birthplace_details,
    "Date of Death": dod,
    "Deathplace Code": deathplace_code,
    "Death Certificate Number": death_cert_number,
}

# On crée le DataFrame avec panda
df = pd.DataFrame(data)

# On fait un split pour séparer le prénom et le nom famille et on efface l'étoile qui est donnée par la base
#df[['Last Name', 'First Name']] = df['Name'].str.split('*', n=1, expand=True)

#df.drop(columns=['Name'], inplace=True)

# On passe c'est deux colonnes au début du tableau
#df = df[['First Name', 'Last Name'] + [col for col in df.columns if col not in ['First Name', 'Last Name']]]


birthplace_options = [{'label': city, 'value': city} for city in df['Birthplace'].unique()]
birthplace_options.sort(key=lambda x: x['label'])

# On initialise la app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.Div(children='My First App with Data', style={'color': 'red'}),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10),
    dcc.Graph(figure=px.histogram(df, x='Sex', y='Age', histfunc='avg'), style={'width': 500}),

    # Création ménu déroulant
    dcc.Dropdown(
        id='birthplace-dropdown',
        options=birthplace_options,
        placeholder="Sélectionnez une ville de naissance"
    ),

    # On affiche les noms et prénoms qui sont nés dans la ville selectionnée
    html.Div(id='selected-names')
])

# Définissez un callback pour mettre à jour les noms et prénoms en fonction de la ville sélectionnée
@app.callback(
    Output('selected-names', 'children'),
    Input('birthplace-dropdown', 'value')
)

def update_selected_names(selected_birthplace):

    # On filtre le DataFrame pour obtenir les noms et prénoms correspondants à la ville sélectionnée
    filtered_data = df[df['Birthplace'] == selected_birthplace]
    
    
    # On crée une liste de noms et prénoms à afficher
    names_to_display = [f"{row['Prenom(s)']} {row['Nom']} Naissance: {row['Birthplace Code']} Mort à: {row['Deathplace Code']}" for index, row in filtered_data.iterrows()]
    
    # On affiche tous les noms
    if len(names_to_display) > 0:
        return html.Ul([html.Li(name) for name in names_to_display])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)