import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import dcc, html
from dash_iconify import DashIconify

from data_preparation import *

all_months = ["Janvier", "Fevrier", "Mars", "Avril", "Mai", "Juin",
              "Juillet", "Aout", "Septembre", "Octobre", "Novembre", "Décembre"]


header = html.Div(className="header d-flex flex-column flex-md-row align-items-center justify-content-center justify-content-md-around", children=[

    html.Div(className="dashboard", children=[
        html.H2([DashIconify(icon="bxs:dashboard", inline=True), " ", "Tableau de bord de ventes"],
                className="text-black font-weight-bold d-inline"),
    ]),

    html.Div(className="div-select-month", children=[
        dbc.Label("Selectionner un mois", html_for="example-email-grid", class_name="label d-inline"),
        dmc.Tooltip(label="Bar de echerche", position="bottom", className="tooltipp", children=[
            dbc.Select(
                id="select-month",
                size="lg",
                options=[{"label": name, "value": month} for
                    name, month in zip(all_months, list(data.Months.unique()))],
                value="JUL",
                placeholder="",
                class_name="select-month dx-inline-block",
            )
        ])
    ])
])