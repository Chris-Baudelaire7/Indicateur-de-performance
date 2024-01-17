import dash_bootstrap_components as dbc  
import dash_mantine_components as dmc  
from dash import Dash, dcc, html

from callback import *
from apps.navbar import navbar
from apps.header import header


font_awesome = "https://use.fontawesome.com/releases/v5.10.2/css/all.css"
meta_tags=[{"name": "viewport", "content": "width=device-width"}]
external_stylesheets = [font_awesome, meta_tags, dbc.themes.CYBORG]
all_months = ["Janvier","Fevrier","Mars","Avril","Mai","Juin","Juillet","Aout","Septembre","Octobre","Novembre","Décembre"]


app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "KPI's dashboard finance"
server = app.server

def div_card_func(card, graph_card):
    div_card = html.Div(className="col-6 col-md-4 col-lg-4 col-xl-2 my-3 my-xl-0", children=[
        html.Div(className="CardBody number-accident common-style-div", children=[
            html.Div(id=card),
            dcc.Graph(
                id=graph_card, config=dict(displayModeBar=False), className="d-none d-md-flex")
        ])
    ])

    return div_card

cards = html.Div(className="row mx-auto mt-4 mb-4 cartes container-fluid", children=[
        
    div_card_func("card1", "graph-card1"),
    div_card_func("card2", "graph-card2"),
    div_card_func("card3", "graph-card3"),
    div_card_func("card4", "graph-card4"),
    div_card_func("card5", "graph-card5"),
    div_card_func("card6", "graph-card6"),
        
])

buttons_graph = html.Div(className="d-flex justify-content-end", children=[
    dmc.SegmentedControl(
            id="type-graph",
            value="area",
            radius="xs",
            data=[
                {"value": "bar", "label": "Barres"},
                {"value": "area", "label": "Lignes"},
            ],
        ),
])

dve2 = html.Div(className="row d-flex align-items-center mx-auto mt-4 mb-4 container-fluid", children=[
        html.Div(className="col-lg-7", children=[
                html.Div(className="p-3 common-style-div", children=[
                    html.H5("Ventes vs Objectifs", className="text-black"),
                    html.Label("Type de graphe", className="text-end"),
                    buttons_graph,
                    dcc.Graph(
                        id="sales_vs_target",
                        config={'displayModeBar': False},
                        figure={}
                    )
                ])  
        ]),
        
        html.Div(className="col-lg-5", children=[
            html.Div(className="row my-4 my-xl-0", children=[
                
                html.Div(className="col-md-6 col-lg-12 col-xl-6 mb-4 mb-md-0", children=[
                    html.Div(className="common-style-div", children=[
                        html.Div(id="avg_sales_customers"),
                        dcc.Graph(
                            id="avg_sales_customers_graph",
                            config={'displayModeBar': False},
                            figure={}
                        )
                    ])  
                ]),
                
                html.Div(className="col-md-6 col-lg-12 col-xl-6 mt-0 mt-lg-4 mt-xl-0", children=[
                    html.Div(className="common-style-div", children=[
                        html.Div(id="avg_ticket_sales"),
                        dcc.Graph(
                            id="avg_ticket_sales_graph",
                            config={'displayModeBar': False},
                            figure={}
                        )
                    ])  
                ]),
            ]),
            
            html.Div(className="row mt-3", children=[
                html.Div(className="col-12", children=[
                    html.Div(className="p-3 common-style-div", children=[
                        html.H5("Croissance mensuelle des ventes", className="text-black"),
                        dcc.Graph(
                            id="growth_graph",
                            config={'displayModeBar': False},
                            figure={}
                        )
                    ])  
                ]),
            ])
        ]),
    ])

dve3 = html.Div(className="row mx-auto mt-4 mb-4 container-fluid", children=[
        html.Div(className="col-xl-5", children=[
            
            html.Div(className="row", children=[
                html.Div(className="col-md-6", children=[
                    html.Div(className="p-3 common-style-div", children=[
                        html.H5("Diagrammes entonoir de vente", className="text-black"),
                        dcc.Graph(
                            id="Diagrammes_entonoir",
                            config={'displayModeBar': False},
                            figure={}
                        )
                    ])  
                ]),
                
                html.Div(className="col-md-6 mt-4 mt-md-0", children=[
                    html.Div(className="p-3 common-style-div", children=[
                        html.H5("Total revenus et cible", className="text-black"),
                        dcc.Graph(
                            id="revenues_target",
                            config={'displayModeBar': False},
                            figure={}
                        )
                    ])  
                ]),
            ]),
            
        ]),
        
        html.Div(className="col-xl-7 w-80 w-xl-100 mt-4 mt-xl-0", children=[
            html.Div(className="row", children=[
                html.Div(className="col-md-6 col-lg-4", children=[
                    html.Div(className="p-3 common-style-div d-flex flex-column justify-content-center align-items-center", children=[
                        html.H5("Bénéfice des ventes", className="text-black"),
                        dcc.Graph(
                            id="sales_profit",
                            config={'displayModeBar': False},
                            figure={}
                        ), 
                    ])  
                ]), 
                
                html.Div(className="col-md-6 col-lg-4 mt-4 mt-md-0", children=[
                    html.Div(className="p-3 common-style-div d-flex flex-column justify-content-center align-items-center", children=[
                        html.H5("Objectif mensuel", className="text-black"),
                        dcc.Graph(
                            id="monthly_goal",
                            config={'displayModeBar': False},
                            figure={}
                        ),
                    ])  
                ]),
                
                html.Div(className="col-md-12 col-lg-4 mt-4 mt-lg-0", children=[
                    html.Div(className="p-3 common-style-div d-flex flex-column justify-content-center align-items-center", children=[
                        html.H5("Objectif Annuel Cumulé",
                                className="text-black"),
                        dcc.Graph(
                            id="YTD_goal",
                            config={'displayModeBar': False},
                            figure={}
                        ),     
                    ])  
                ]),
            ]),
        ]),
    ])


app.layout = html.Div(id="main-app", className="main-app", children=[
    navbar, header, cards, dve2, dve3
])

app.run_server(debug=False)
