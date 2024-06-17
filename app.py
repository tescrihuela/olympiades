import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd


# Input files
scores_file = './data/scores.csv'
scores_equipes_file = './data/scores_equipes.csv'
reglement_md = './pages/reglement.md'
mentions_legales_md = './pages/mentions_legales.md'

location = '/olympiades'
df_classement_individuel = pd.read_csv(scores_file)#.drop('Genre', axis=1)
df_classement_equipes = pd.read_csv(scores_equipes_file)

# Initialisation de l'application Dash
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = dash.Dash(__name__, url_base_pathname=f"{location}/", external_stylesheets=[dbc.themes.SANDSTONE, dbc_css, dbc.icons.BOOTSTRAP])
server = app.server

# Création de la mise en page
app.layout = dbc.Container(className='dbc dbc-ag-grid', fluid = True, children=[
    dcc.Location(id="url", refresh=False),
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink(" Accueil", href=f"{location}/", className="bi bi-house")),
            dbc.NavItem(dbc.NavLink(" Règlement", href=f"{location}/reglement", className="bi bi-book")),
            dbc.NavItem(dbc.NavLink(" Épreuves", href=f"{location}/epreuves", className="bi bi-card-checklist")),
            dbc.NavItem(dbc.NavLink(" Classement individuel", href=f"{location}/classement_individuel", className="bi bi-person")),
            dbc.NavItem(dbc.NavLink(" Classement par équipes", href=f"{location}/classement_par_equipe", className="bi bi-trophy")),
            dbc.NavItem(dbc.NavLink(" Mentions légales", href=f"{location}/mentions_legales", className="bi bi-journal")),
        ],
        brand = "Olympiades du Cerema",
        brand_href = f"{location}/",
        fluid = True,
        links_left = True,
        sticky = 'top',
        color="primary",
        dark=True
    ),
    dbc.Container(id='content', className="mb-4", fluid=True) 
])

# Callback pour afficher le contenu de l'onglet sélectionné
@app.callback(Output('content', 'children'), [Input('url', 'pathname')])
def display_tab_content(pathname):
    if pathname == f'{location}/':
        return html.Div(children = [
            html.Br(),
            dbc.Alert("⚠️ Attention, ne pas se référer aux dates de l'affiche concernant la piscine et le sprint/lancer de poids. Les épreuves de piscine auront lieu les jeudi 06/06 et 13/06 ; et les sessions de sprint/lancer de poids auront donc lieu les mardi 04/06 et 11/06.", color="warning", style={"width": "fit-content", "margin": "auto", 'color': 'black'}, id="alert-fade"),
            html.Br(),
            html.Img(src='assets/static/affiche.jpg', style={'width': '40em', 'height': 'auto', 'display': 'block', 'margin': 'auto'}),
        ])
    elif pathname == f'{location}/epreuves':
        return html.Div(children = [
            dcc.Markdown(
"""
### Principe des épreuves

Les épreuves, au nombre de 6, sont à proximité immédiate du site : 

![alt text](/olympiades/assets/static/sites.png)

[Sites des épreuves](https://www.geoportail.gouv.fr/carte?c=1.044246406507031,49.39501357297797&z=16&l0=ORTHOIMAGERY.ORTHOPHOTOS::GEOPORTAIL:OGC:WMTS(1)&d1=5143413(0.5)&d2=5143414(1)&permalink=yes)

"""
            ),
            dbc.Row(
                [
                    dbc.Col(dbc.Card([
                        dbc.CardHeader(html.H5("Cross")),
                        dbc.CardBody([
                            dcc.Markdown(
"""
Le cross est une épreuve individuelle de course à pied, d’une distance de 5 km environ. Un temps de parcours sera attribué à chaque participant (chronométrage à l’arrivée).
Le parcours correspond à **deux tours de forêt du Chêne à Leu**. 

Ce parcours est encore en phase de concertation et peut évoluer. Les participants seront invités à bien prendre connaissance du parcours en amont de la course. En effet, même si une signalétique sera mise en place, des points d’attention sont à relever (détails à venir).

**L’épreuve de Cross aura lieu le mardi 21/05**. Une session de rattrapage est prévue le jeudi 30/05.

**L’horaire de départ est fixé à 12h20**. Les participants devront se présenter pour émarger au moins 10 minutes avant le départ.  Un échauffement collectif sera proposé dès 12h et le départ sera groupé.
Une bouteille d’eau et une tenue adaptée pour une course en forêt sont fortement recommandés.
""",
                                className="card-text",
                            ),
                        ])], 
                        color="primary", outline = True)
                    ),
                    dbc.Col(dbc.Card([
                        dbc.CardHeader(html.H5("Pétanque")),
                        dbc.CardBody([
                            dcc.Markdown(
"""
L’épreuve de pétanque est une épreuve individuelle de précision qui se décompose en deux sous-épreuves : 
* Pointé : un cercle d’1 mètre de diamètre sera tracé au sol. Placé à 8 mètres du cercle, l’objectif est de placer la boule de pétanque dans le cercle (15 essais). Après chaque lancé, la boule est récupérée par le concurrent (on ne laisse pas les boules déjà lancées dans le cercle). Le tracé fait partie du cercle.
* Tiré : un cercle sera disposé de la même manière. L’objectif est de tirer une boule de pétanque située au milieu du cercle (15 essais).  Pour que le point soit validé, la boule visée doit sortir du cercle.

Un score sur 30 sera alors attribué au joueur.

**Cette épreuve se déroulera le jeudi 23/05 , à côté du terrain de foot/basket dans la forêt du Chêne à Leu.**

Un  créneau de rattrapage est prévu le mardi 28/05.

**L’épreuve commencera à 12h**, jusqu’à 13h/13h30 en fonction du nombre de participants. 
""",
                                className="card-text",
                            ),
                        ])], 
                        color="secondary", outline = True)
                    ),                    
                    dbc.Col(dbc.Card([
                        dbc.CardHeader(html.H5("Ballons")),
                        dbc.CardBody([
                            dcc.Markdown(
"""
L’épreuve de ballons est une épreuve individuelle de précision mêlant basket et football : 
* Basket : le joueur effectue 15 lancers francs depuis la ligne des lancers francs.
* Football : le joueur tire 15 pénaltys depuis le point de pénalty. Il n’y a pas de gardien. L’objectif est de tirer dans un des 4 coins de la cage, matérialisés par des cordes. Il est interdit de marquer plus de 4 buts dans un coin. Par exemple, si le Joueur 1 marque 4/6 tirs en bas à droite, puis 4/4 tirs en bas à gauche, il doit alors marquer ses 5 derniers pénaltys en haut à gauche et en haut à droite.

Un score sur 30 sera attribué au joueur.

**Cette épreuve aura lieu le jeudi 23/05**, en même temps que celle de pétanque (12h - 13h/13h30), sur le terrain de foot/basket dans la forêt du Chêne à Leu. Le créneau de rattrapage est également le même : jeudi 28/05. 
""",
                                className="card-text",
                            ),
                        ])], 
                        color="info", outline = True)
                    ),                    
                ],
                className="mb-4",
            ),
            dbc.Row(
                [
                    dbc.Col(dbc.Card([
                        dbc.CardHeader(html.H5("Sprint")),
                        dbc.CardBody([
                            dcc.Markdown(
"""
L’épreuve de sprint est une épreuve individuelle de course à pied sur 100 mètres. La distance sera matérialisée par une ligne de départ et une ligne d’arrivée. Un temps sera attribué à chaque participant (chronométrage à l’arrivée). Deux essais seront possibles, la meilleure performance sera conservée. Les départs se feront par groupe de 2 personnes (par affinité ou niveau).

**Cette épreuve se déroulera sur la piste d’éclairage du Cerema NC, le mardi 04/06.**
Une session de rattrapage est prévue le mardi 11/06.
**Les départs seront donnés à partir de 12h20.** Un échauffement collectif sera proposé dès 12h.
""",
                                className="card-text",
                            ),
                        ])], 
                        color="success", outline = True)
                    ),
                    dbc.Col(dbc.Card([
                        dbc.CardHeader(html.H5("Lancer de poids")),
                        dbc.CardBody([
                            dcc.Markdown(
"""
L’épreuve de lancer de poids (5kg pour les hommes, et 3kg pour les femmes) est une épreuve individuelle de lancer. Une ligne au sol marquera la limite de lancer, la distance sera alors calculée par rapport à un point central et unique sur cette ligne.  Tout essai conduisant au franchissement même partiel de cette ligne (pied, genou, …) rendra l’essai nul et sera comptabilisé. Trois essais seront possibles, la meilleure performance sera conservée. 

**Cette épreuve aura lieu en parallèle de celle de sprint : le mardi 04/06 à proximité de la piste d’éclairage.** Elle démarrera en revanche dès 12h.
De même, la session de rattrapage sera le mardi 11/06.
""",
                                className="card-text",
                            ),
                        ])], 
                        color="warning", outline = True)
                    ),                    
                    dbc.Col(dbc.Card([
                        dbc.CardHeader(html.H5("Natation")),
                        dbc.CardBody([
                            dcc.Markdown(
"""
L’épreuve de natation est individuelle et consistera en un 100 mètres, correspondant à 4 longueurs de bassin. Un temps de parcours sera attribué à chaque participant (chronométrage à l’arrivée). Deux brasses seront imposées sur ces 4 longueurs. C'est-à-dire 2 longueurs brasses + 2 longueurs crawl, ou 3 longueurs brasses + 1 longueur crawl, 4 longueurs brasses (l’ordre n’ayant pas d’importance). Le départ se fera en plongeon ou dans l’eau.

**Cette épreuve aura lieu à la piscine Camille Muffat (en attente de confirmation finale), le jeudi 06/06 et le jeudi 13/06 (rattrapage).** Le début est prévu pour 12h.
Les participants devront se munir d’une tenue adaptée à la réglementation de la piscine.
""",
                                className="card-text",
                            ),
                        ])], 
                        color="danger", outline = True)
                    ),                    
                ],
                className="mb-4",
            ),
            dbc.Row(
                [
                    dbc.Col(dbc.Card([
                        dbc.CardHeader(html.H5("Relais")),
                        dbc.CardBody([
                            dcc.Markdown(
"""
La dernière épreuve de ces olympiades sera la seule et unique par équipe : un relais 4x400 mètres. Chaque relais consistera en une ligne droite de 200m, suivi d’un virage et du retour sur 200m. Tous les relais seront ainsi passés dans la même zone.

**Il se déroulera sur la piste d’éclairage, le mardi 18/06.**
Le départ sera donné à 12h30.

Afin de finir en beauté, les déguisements sont fortement conseillés sur le relais 🙂
Le relais sera suivi d’un pot offert par l’ASCE, et de la remise des lots et récompenses ! 
""",
                                className = 'card-text',
                            ),
                        ])],
                        color = 'dark', outline = True)
                    ),

                ],
                className="mb-4",
            ),
        ])
    elif pathname == f'{location}/classement_individuel':
        sorted_df = df_classement_individuel.sort_values(by='Score Total', ascending=False)
        return dbc.Container(fluid=True, children=[
            html.Br(),
            dbc.Alert("⚠️ Des coquilles peuvent subsister malgré la rigueur absolue des organisateurs. Merci de vérifier que vos performances sont correctement renseignées, et que vous appartenez à la bonne équipe :)", color="warning", style={"width": "fit-content", "margin": "auto", 'color': 'black'}, id="alert-fade"),
            html.Br(),
            dash_table.DataTable(
                id='datatable',
                columns=[{'name': col, 'id': col} for col in sorted_df.columns],
                style_header={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                },
                style_data_conditional=
                [
                    {
                        'if': {'column_id': col},
                        'fontWeight': 'bold'
                    } for col in ['Participant', 'Score Total']
                ] + [
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(240, 240, 240)'

                    }
                ] + [
                    {
                        'if': {'column_id': col},
                        'textAlign': 'left'
                    } for col in ['Participant', 'Genre', 'Équipe']
                ] + [
                    {
                        'if': {'column_id': col},
                        'textAlign': 'center'
                    } for col in ["Cross", "Natation", "Sprint", "Poids", "Pétanque", "Ballons", "Score Cross", "Score Natation", "Score Sprint", "Score Poids", "Score Pétanque", "Score Ballons", "Score Total"]
                ] + [
                    {
                        'if': {'column_id': col},
                        'backgroundColor': '#FAE5D3',
                    } for col in ['Score Total']

                ] + [
                    {
                        'if': {'row_index': 0},
                        'backgroundColor': 'rgb(255, 215, 0)'

                    }

                ] + [
                    {
                        'if': {'row_index': 1},
                        'backgroundColor': 'rgb(192, 192, 192)'

                    }

                ] + [
                    {
                        'if': {'row_index': 2},
                        'backgroundColor': 'rgb(205, 127, 50)'

                    }
                ],
                data=sorted_df.to_dict('records'),
                sort_action='native',
                filter_action='native',
                filter_options={'case':'insensitive'},        
                page_action="native",
                style_table={'overflowX': 'auto'}
            )
        ])
    elif pathname == f'{location}/classement_par_equipe':
        sorted_df_classement_equipes = df_classement_equipes.sort_values(by='Score Total', ascending=False)
        return html.Div(children=[
            html.Br(),
            dbc.Alert("⚠️ Des coquilles peuvent subsister malgré la rigueur absolue des organisateurs. Merci de vérifier que vos performances sont correctement renseignées, et que vous appartenez à la bonne équipe :)", color="warning", style={"width": "fit-content", "margin": "auto", 'color': 'black'}, id="alert-fade"),
            html.Br(),
            dash_table.DataTable(
                id='datatable',
                columns=[{'name': col, 'id': col} for col in sorted_df_classement_equipes.columns],
                style_data_conditional=
                [
                    {
                        'if': {'column_id': col},
                        'fontWeight': 'bold'
                    } for col in ['Équipe', 'Score Total']
                ] + [
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(240, 240, 240)'

                    }
                ] + [
                    {
                        'if': {'column_id': col},
                        'textAlign': 'left'
                    } for col in ['Équipe']

                ] + [
                    {
                        'if': {'row_index': 0},
                        'backgroundColor': 'rgb(255, 215, 0)'

                    }

                ] + [
                    {
                        'if': {'row_index': 1},
                        'backgroundColor': 'rgb(192, 192, 192)'

                    }

                ] + [
                    {
                        'if': {'row_index': 2},
                        'backgroundColor': 'rgb(205, 127, 50)'

                    }
                ],
                data=sorted_df_classement_equipes.to_dict('records'),
                sort_action='native',
                filter_action='native',
                filter_options={'case':'insensitive'},
                page_action="native",
                style_table={'overflowX': 'auto'}
            )
        ])
    elif pathname == f'{location}/reglement':
        return html.Div(children=[
            dcc.Markdown(open(reglement_md, 'r', encoding='utf8').read()),
        ])
    elif pathname == f'{location}/mentions_legales':
        return html.Div(children=[
            html.Br(),
            dcc.Markdown(open(mentions_legales_md, 'r', encoding='utf8').read()),
        ])

# Lancement de l'application
if __name__ == '__main__':
    app.run_server(threaded=True)
