from MesOrigines_f9 import *


df_vide = pd.DataFrame()

carte = go.Figure(go.Scattermapbox())

carte.update_layout(
     margin ={'l':0,'t':0,'b':0,'r':0},
     mapbox = {
         'center': {'lon': 10, 'lat': 10},
         'style': "carto-positron",
         'center': {'lon': 2, 'lat': 47},
         'zoom': 5},
         paper_bgcolor= '#292A30',
         font_color='#e0e0e0'
 )

def page10_layout():

    #Affichage titre et sous-titre
    return html.Div(className='corpslambda', children=[
    html.H1("Déplacements", style={"font-family": "verdana"}),
    dcc.Markdown(className="manu", children="""Cette carte représente les déplacements en France."""),
        html.Div([
            dcc.Graph(figure=carte,style={"width": "100%", "height": "80vh"})
        ],
         style={"width": "100vw", "height": "100%"}),
])