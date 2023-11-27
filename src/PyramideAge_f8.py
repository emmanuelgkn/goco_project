from Distance_f7 import *
import matplotlib.pyplot as plt

# Initialisation de listes vides pour les colonnes du nouveau DataFrame
age_groups = []
male_counts = []
female_counts = []
female_left = []
female_width = []
male_left = []
male_width = []

# Définition des tranches d'âge
age_intervals = [(0, 4), (5, 9), (10, 14), (15, 19), (20, 24), (25, 29), (30, 34), (35, 39),
                (40, 44), (45, 49), (50, 54), (55, 59), (60, 64), (65, 69), (70, 74), (75, 79),
                (80, 84), (85, 89), (90, 94), (95, 99), (100, 104), (105, 109), (110, 114)]

# Calcul des informations pour chaque tranche d'âge
for interval in age_intervals:
    lower_bound, upper_bound = interval
    age_groups.append(f"{lower_bound}-{upper_bound}")
    male_count = len(merged_df[(merged_df['Age'] >= lower_bound) & (merged_df['Age'] <= upper_bound) & (merged_df['Sex'] == 'Masculin')])
    female_count = len(merged_df[(merged_df['Age'] >= lower_bound) & (merged_df['Age'] <= upper_bound) & (merged_df['Sex'] == 'Féminin')])
    male_counts.append(male_count)
    female_counts.append(female_count)

# Création du DataFrame avec les listes créées
df_pyramid = pd.DataFrame({
    'Age': age_groups,
    'Male': male_counts,
    'Female': female_counts,
})

df_pyramid["Female_Left"] = 0
df_pyramid["Female_Width"] = df_pyramid["Female"]

df_pyramid["Male_Left"] = -df_pyramid["Male"]
df_pyramid["Male_Width"] = df_pyramid["Male"]
# Vérification du DataFrame

# Inverser l'ordre des colonnes pour afficher les hommes d'abord
df_pyramid = df_pyramid[['Age', 'Male', 'Female', 'Male_Left', 'Male_Width', 'Female_Left', 'Female_Width']]

fig_pyramide = go.Figure()
fig_pyramide.add_trace(go.Bar(y=df_pyramid["Age"], x=df_pyramid["Male_Width"], base=-df_pyramid["Male_Width"],
                     orientation='h', name='Male', text=df_pyramid["Male"],
                     hoverinfo='text', marker=dict(color="#4682b4")))
fig_pyramide.add_trace(go.Bar(y=df_pyramid["Age"], x=df_pyramid["Female_Width"], base=0, orientation='h',
                     name='Female', text=df_pyramid["Female"],
                     hoverinfo='text', marker=dict(color="#ee7a87")))

fig_pyramide.update_layout(barmode='stack',
                  title="Carte population France",
                  xaxis_title="Pourcentage (%)",
                  yaxis_title="Tranche d'âge",
                  plot_bgcolor= '#292A30',
                  paper_bgcolor= '#292A30',
                  font_color='#e0e0e0'
                )


def page8_layout():
    return html.Div(className='corpslambda',children=[
    html.H1("Graphiques"),
    html.Br(),
    dcc.Markdown(className="manu", children="""
    Cette page comporte 3 graphes:  
        - Le Graphique représentant la moyenne d'age des hommes et des femmes  
        - Le Graphique représentant l'ésperance de vie en fonction de l'année et du genre  
        - La Pyramide d'age de la population en france
    """),
    html.Br(),
    dcc.Graph(figure = fig_HF),
    dcc.Graph(figure = fig_esperance),
    dcc.Graph(figure = fig_pyramide),
])