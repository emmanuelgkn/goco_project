from dash import Dash, html, dash_table, dcc
from dash.dependencies import Input, Output


from AboutUs_f12 import *

# Affiche de toute notre application Dash
app.layout = html.Div([
    html.Link(
        href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap",
        rel="stylesheet"
    ),
    dcc.Location(id='url', refresh=False),
    html.Nav(className="nave", children=[
        html.Ul(className="listacceuil", children=[
            html.Li(html.A("Home", href='/Accueil')),
            html.Li( children = [ "Stats",
                html.Ul([
                    html.Li(html.A("Carte mouvements", href="/CarteMouvements")),
                    html.Li(html.A("Top noms", href="/TopNoms")),
                    html.Li(html.A("Top villes décès", href="/TopVillesDeces")),
                    html.Li(html.A("Carte décès", href="/CarteDeces")),
                    html.Li(html.A("Distance parcourue", href="/DistanceParcourue")),
                    html.Li(html.A("Graphes âge", href="/GraphesAge")),
                    html.Li(html.A("Mes origines", href="/MesOrigines")),
                ])
            ]),
            html.Li(html.A("About us", href='/About'))
        ])
    ]),
    html.Div(id='page-content', className='corps wrapper'),
    html.Footer(
        html.Div(
            className="container",
            children=[
                html.Br(),
                html.A("Home", href='/Accueil', className = "linkFooter"),
                html.Span(" | "),
                html.A("About us", href='/About', className = "linkFooter"),
                html.H5("Réalisé par Emmanuel Gokana et Jofre Coll"),
                html.A(
                    html.Div(className="photoGithub"),
                    href = "https://github.com/emmanuelgkn/goco_project",
                )
            ], style={'flex': '0 0 auto'}  # Ajoutez ce style pour le positionnement du footer
        )
    )
])
 

# Callback pour mettre à jour la page en fonction de l'URL
@app.callback(Output('page-content', 'children'), Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/About':
        return pageA_layout()
    if pathname == '/CarteMouvements':
        return page3_layout()
    if pathname == '/TopNoms':
        return page4_layout()
    if pathname == '/TopVillesDeces':
        return page5_layout()
    if pathname == '/CarteDeces':
        return page6_layout()
    if pathname == '/DistanceParcourue':
        return page7_layout()
    if pathname == '/GraphesAge':
        return page8_layout()
    if pathname == '/MesOrigines':
        return page9_layout()
    if pathname == '/Accueil':
        return Accueil_layout()
    else:
        return Accueil_layout()
print('Site Utilisable')

if __name__ == '__main__':
    app.run_server(host='0.0.0.0',port=7744)