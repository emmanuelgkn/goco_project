from Distance_f7 import *
import matplotlib.pyplot as plt

df_pyramid = merged_df.copy()

def page8_layout():
    return html.Div(children=[
    html.Div(
        html.H1("Pyramide Age",
            style = {"font-family" : "verdana"}),
        style = { "background-color" : "antiquewhite"}),
    dcc.Markdown(className = "manu",children = """
    Ce graphe représente pour la l'age moyenne le nombre d'hommes et femmes en France.
    """),
    
    dcc.Graph(id='graph-pyramid',figure = fig)])

'''
@app.callback(
    Output('graph-pyramid', 'figure')
)
def update_graph():
    fig = plt.figure(figsize=(15, 10))
    plt.bahr(y=df_pyramid['Age'])
    return fig
'''