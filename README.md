# goco_project
Dans le cadre de l'UE lifprojet nous avons créé un site web permettant de visuliser les différents apects d'un jeu de données portant principalement sur les décès enregistrés en france pour cela nous allons nous aider de différents outils tel que dash une librairie python ou encore Leafet sur javascript

LIENS IMPORTANTS:

1) Projet ---> http://cazabetremy.fr/wiki/doku.php?id=projet:sujets
2) Tutorial Dash ---> https://dash.plotly.com/tutorial
3) Creation carte ---> https://python-visualization.github.io/folium/latest/getting_started.html
4) Creation carte ---> https://leafletjs.com/
5) Base de données ---> https://www.data.gouv.fr/fr/datasets/fichier-des-personnes-decedees/#/resources
   Dessin d'enregistrement
Le fichier est fourni au format txt

Nom et Prénom - Longueur : 80 - Position : 1-80 - Type : Alphanumérique
La forme générale est NOM*PRENOMS

Sexe - Longueur : 1 - Position : 81 - Type : Numérique
1 = Masculin; 2 = féminin

Date de naissance - Longueur : 8 - Position : 82-89 - Type : Numérique
Forme : AAAAMMJJ - AAAA=0000 si année inconnue; MM=00 si mois inconnu; JJ=00 si jour inconnu

Code du lieu de naissance - Longueur : 5 - Position : 90-94 - Type : Alphanumérique
Code Officiel Géographique en vigueur au moment de la prise en compte du décès

Commune de naissance en clair - Longueur : 30 - Position : 95-124 - Type : Alphanumérique

DOM/TOM/COM/Pays de naissance en clair - Longueur : 30 - Position : 125-154 - Type : Alphanumérique

Date de décès - Longueur : 8 - Position : 155-162 - Type : Numérique
Forme : AAAAMMJJ - AAAA=0000 si année inconnue; MM=00 si mois inconnu; JJ=00 si jour inconnu

Code du lieu de décès - Longueur : 5 - Position : 163-167 - Type : Alphanumérique
Code Officiel Géographique en vigueur au moment de la prise en compte du décès

Numéro d'acte de décès - Longueur : 9 - Position : 168-176 - Type : Alphanumérique
NOTA : Certains enregistrements peuvent contenir en toute fin des caractères non significatifs. Il est donc important, pour lire correctement ce champ, de bien respecter sa longueur ou sa borne de fin.
