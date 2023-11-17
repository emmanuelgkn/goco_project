from dash import Dash, html, dash_table, dcc
from dash.dependencies import Input, Output


from Deplacements_f10 import *

# Configuration de la barre de navigation
app.layout = html.Div([
    html.Link(
        href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap",
        rel="stylesheet"
    ),
    dcc.Location(id='url', refresh=False),
    html.Nav(className="nave", children=[
        html.Ul(className="listacceuil", children=[
            html.Li(html.A("Home", href='/Acceuil')),
            html.Li( children = [ "Stats",
                html.Ul([
                    html.Li(html.A("Carte", href="/page3")),
                    html.Li(html.A("Top Noms", href="/page4")),
                    html.Li(html.A("Lieu Deces", href="/page5")),
                    html.Li(html.A("Carte Deces", href="/page6")),
                    html.Li(html.A("Distance", href="/page7")),
                    html.Li(html.A("Graphes age", href="/page8")),
                    html.Li(html.A("Mes origines", href="/page9")),
                    html.Li(html.A("Déplacements", href="/page10"))
                ])
            ]),
            html.Li(html.A("About us", href='/About'))
        ])
    ]),
    html.Div(id='page-content', className='corps wrapper'),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Footer(
        html.Div(
            className="container",
            children=[
                html.Br(),
                html.A("Home", href='/Acceuil', className = "linkFooter"),
                html.Span(" | "),
                html.A("About us", href='/Acceuil', className = "linkFooter"),
                html.H5("Réalisé par Emmanuel Gokana et Jofre Coll"),
                html.A(
                    html.Div(className="photoGithub"),
                    href = "https://github.com/emmanuelgkn/goco_project",
                )
            ], style={'flex': '0 0 auto'}
        )
    )
])
 

# Callback pour mettre à jour la page en fonction de l'URL
@app.callback(Output('page-content', 'children'), Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/About':
        return pageA_layout()
    if pathname == '/page3':
        return page3_layout()
    if pathname == '/page4':
        return page4_layout()
    if pathname == '/page5':
        return page5_layout()
    if pathname == '/page6':
        return page6_layout()
    if pathname == '/page7':
        return page7_layout()
    if pathname == '/page8':
        return page8_layout()
    if pathname == '/page9':
        return page9_layout()
    if pathname == '/page10':
        return page10_layout()
    if pathname == '/Accueil':
        return Accueil_layout()
    else:
        return Accueil_layout()
print('Site Utilisable')
if __name__ == '__main__':
    app.run_server(debug=True, port = 8080)

