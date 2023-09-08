# On import les packages
from dash import Dash, html, dash_table
import pandas as pd

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

# On fait une itération sur chaque ligne pour extraire les données selon la position et la longueur du format de la base
# On utilse stip() pour effacer les espaces en blanc au début et à la fin

for line in lines:
    name = line[0:80].strip() 
    gender_code = line[80:81]  # On garde le code du genre (1 = Masculin, 2= Féminin)
    date_year = line[81:85]
    date_month = line[85:87]
    date_day = line[87:89]
    birthplace_code = line[89:94].strip()
    birthplace_text = line[94:124].strip()
    birthplace_details_text = line[124:154].strip()
    date_of_death = line[154:162]
    deathplace_code_text = line[162:167].strip()
    death_cert_number_text = line[167:176].strip()

    # On doit convertir le code du genre en string
    if gender_code == '1':
        gender_text = "Masculin"
    elif gender_code == '2':
        gender_text = "Féminin"
    else:
        gender_text = "Inconnu"  # Au cas où ce ne serait pas spécifié

    # On fait un append de l'information de la ligne qu'on a traité à la liste du tableau
    names.append(name)
    gender.append(gender_text)
    dob.append(date_day + "/" + date_month + "/" + date_year)
    birthplace_code_list.append(birthplace_code)
    birthplace.append(birthplace_text)
    birthplace_details.append(birthplace_details_text)
    dod.append(date_of_death)
    deathplace_code.append(deathplace_code_text)
    death_cert_number.append(death_cert_number_text)

# On crée le tableau à partir des listes qu'on a créé
data = {
    "Name": names,
    "Sex": gender,
    "Date of Birth": dob,
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
df[['Last Name', 'First Name']] = df['Name'].str.split('*', n=1, expand=True)

df.drop(columns=['Name'], inplace=True)

# On passe c'est deux colonnes au début du tableau
df = df[['First Name', 'Last Name'] + [col for col in df.columns if col not in ['First Name', 'Last Name']]]

# On initialise la app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.Div(children='My First App with Data'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=100)
])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)