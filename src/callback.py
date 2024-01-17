import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback

from utils import *
from data_preparation import *



@callback(
    Output("card1", "children"),
    Output("graph-card1", "figure"),
    Input("select-month", "value")
)
def render_cards_content(month):
    if month is None:
        raise PreventUpdate
    
    df = data.copy()
    # Difference revenues between two month
    df["Revenues_difference"] = df.Revenues.diff(1)
    # Percentage change between two month
    df["pct_change"] = df.Revenues.pct_change() * 100
    df = df.copy().fillna(0)
    filter_by_month = df[df.Months == month]
    revenues = filter_by_month["Revenues"].iloc[0]
    revenues_difference = filter_by_month["Revenues_difference"].iloc[0]
    revenues_pct_change = filter_by_month["pct_change"].iloc[0]
    
    if revenues_difference > 0:
        color="green"
        style={"color":color, "font-size":"25px", "margin-left":"5px"}
        children_card1 = [
            html.Div(className="ml-3", children=[
                html.P("Revenues", className="text-black d-inline"), 
                html.Br(),
                html.P([DashIconify(icon="bx:dollar", width=10, inline=True, color="gray"), html.Span(f"{revenues:,.0f}", className="text-black"), html.Span("USD", style={"color":"#777", "font-size":"15px", "margin-left":"4px"})], className="solde"),
                dmc.Text([DashIconify(icon="bxs:up-arrow", width=15, inline=True, color=color), f"+{revenues_difference:,.0f}$", f" ({revenues_pct_change:,.0f}%)"], style={"color": color}),
                html.Span("Par rapport au mois précédent")
            ])
        ]
        
    if revenues_difference < 0:
        color="red"
        style={"color":color, "font-size":"25px", "margin-left":"5px"} #  
        children_card1 = [
            html.Div(className="ml-3", children=[
                html.P("Revenues", className="text-black d-inline"), #
                html.Br(),
                html.P([DashIconify(icon="bx:dollar", width=10, color="gray",), f"{revenues:,.0f}", html.Span("USD", style={"color":"#777", "font-size":"15px", "margin-left":"4px"})], className="solde"),
                dmc.Text([DashIconify(icon="bxs:down-arrow", width=15, inline=True, color=color), f"{revenues_difference:,.0f}$", " ", f"({revenues_pct_change:,.0f}%)"], style={"color": color}),
                html.Span("Par rapport au mois précédent")
            ])
        ]
        
    if revenues_difference == 0:
        style={"font-size":"35px", "margin-left":"5px"}
        color=None
        children_card1 = [
            html.Div(className="ml-3", children=[
                html.P("Revenues", className="text-black d-inline"), #
                html.Br(),
                html.P([DashIconify(icon="bx:dollar", width=10, color="gray"), f"{revenues:,.0f}", html.Span("USD", style={"color":"#777", "font-size":"15px", "margin-left":"4px"})], className="solde"),
                dmc.Text([f"{revenues_difference:,.0f}$", f" ({revenues_pct_change:,.0f}%)"], style={"color": color}),
                html.Span("Par rapport au mois précédent")
            ])
        ]
    
    linecolor="rgb(31, 149, 233)"
    fillcolor="rgba(122, 147, 236, 0.192)"
    fig = go.Figure(
        go.Scatter(
            x=df['Months'], y=df['Revenues'],    
            mode="lines+markers", line=dict(color=linecolor, width=1.6),
            hoverinfo="text", stackgroup=True, fillcolor=fillcolor,
            marker=dict(size=3.5, color="royalblue", symbol="square"),
            hovertext=
            "Mois: " + df['Months'].astype(str) + "<br>" +
            "Revenues: " + [f"${x:,.0f}" for x in df['Revenues']] + "<br>"
        )
    )
    
    fig.update_layout(
        height=60,
        hovermode="x",
        template="plotly_dark",
        margin=dict(autoexpand=True, l=0, r=0, b=0, t=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(
            showline=False,
            showticklabels=False,
            gridcolor="rgba(79, 79, 79, 0.113)",
            showgrid=True,
            linecolor = 'white',
            linewidth = 1,
            tickfont = dict(
                family = 'Arial',
                size = 12,
                color = 'white') 
        ),
        yaxis=dict(
            showticklabels=False,
            showline=False,
            showgrid=False
        ),
        hoverlabel=dict(
            bgcolor="white",
            bordercolor="rgba(0,0,0,0)",
            font=dict(
                color="black",
                size=11,
                family="serif"
            )
        )
    )
             
    return children_card1, fig

# -------------------

@callback(
    Output("card2", "children"),
    Output("graph-card2", "figure"),
    Input("select-month", "value")
)
def render_cards_content(month):
    if month is None:
        raise PreventUpdate
    
    df = data.copy()
    # Profit
    df["Profit"] = df["Revenues"] - df["Total Cost (Sales & Marketing)"]
    # Difference profit between two months
    df["Profit_difference"] = df["Profit"].diff()
    # Percentage change between two Months
    df["Profit_pct_difference"] = df["Profit"].pct_change() * 100
    df = df.copy().fillna(0)
    filter_month = df[df.Months == month]
    profit = filter_month["Profit"].iloc[0]
    profit_difference = filter_month["Profit_difference"].iloc[0]
    profit_pct_change = filter_month["Profit_pct_difference"].iloc[0]
    
    if profit_difference > 0:
        color="green"
        style={"color":color, "font-size":"25px", "margin-left":"5px"}
        children_card1 = [
            html.Div(className="ml-3", children=[
                html.P("Profit", className="text-black d-inline"), 
                html.Br(),
                html.P([DashIconify(icon="bx:dollar", width=10, color="gray"), html.Span(f"{profit:,.0f}", className="text-black"), html.Span("USD", style={"color":"#777", "font-size":"15px", "margin-left":"4px"})], className="solde"),
                dmc.Text([DashIconify(icon="bxs:up-arrow", width=15, inline=True, color=color), f"+{profit_difference:,.0f}$", f" ({profit_pct_change:,.0f}%)"], style={"color": color}),
                html.Span("Par rapport au mois précédent")
            ])
        ]
        
    if profit_difference < 0:
        color="red"
        style={"color":color, "font-size":"25px", "margin-left":"5px"} #  
        children_card1 = [
            html.Div(className="ml-3", children=[
                html.P("Profit", className="text-black d-inline"), #
                html.Br(),
                html.P([DashIconify(icon="bx:dollar", width=10, color="gray"), f"{profit:,.0f}", html.Span("USD", style={"color":"#777", "font-size":"15px", "margin-left":"4px"})], className="solde"),
                dmc.Text([DashIconify(icon="bxs:down-arrow", width=15, inline=True, color=color), f"{profit_difference:,.0f}$", " ", f"({profit_pct_change:,.0f}%)"], style={"color": color}),
                html.Span("Par rapport au mois précédent")
            ])
        ]
        
    if profit_difference == 0:
        style={"font-size":"35px", "margin-left":"5px"}
        color=None
        children_card1 = [
            html.Div(className="ml-3", children=[
                html.P("Profit", className="text-black d-inline"), #
                html.Br(),
                html.P([DashIconify(icon="bx:dollar", width=10, color="gray"), f"{profit:,.0f}", html.Span("USD", style={"color":"#777", "font-size":"15px", "margin-left":"4px"})], className="solde"),
                dmc.Text([f"{profit_difference:,.0f}$", f" ({profit_pct_change:,.0f}%)"], style={"color": color}),
                html.Span("Par rapport au mois précédent")
            ])
        ]
    
    linecolor="rgb(31, 149, 233)"
    fillcolor="rgba(122, 147, 236, 0.192)"
    fig = go.Figure(
        go.Scatter(
            x=df['Months'], y=df['Profit'],    
            mode="lines+markers", line=dict(color=linecolor, width=1.6),
            hoverinfo="text", marker=dict(size=3.5, symbol="square"), fillcolor=fillcolor,
            stackgroup=True,
            hovertext=
            "Mois: " + df['Months'].astype(str) + "<br>" +
            "Profit: " + [f"${x:,.0f}" for x in df['Profit']] + "<br>"
        )
    )
    
    fig.update_layout(**update_layout)
             
    return children_card1, fig

# ------------

@callback(
    Output("card3", "children"),
    Output("graph-card3", "figure"),
    Input("select-month", "value")
)
def render_cards_content(month):
    if month is None:
        raise PreventUpdate
    
    df = data.copy()
    # Calculate difference between two months
    df['Orders_Difference'] = df['Orders Placed'].diff()
    # Calculate percentage change difference between two months
    df['Orders_pct_Difference'] = (df['Orders Placed'].pct_change()) * 100
    df['Orders_Difference'] = df['Orders_Difference'].fillna(0)
    filter_month = df[df['Months'] == month]
    orders_placed = filter_month['Orders Placed'].iloc[0]
    orders_difference = filter_month['Orders_Difference'].iloc[0]
    orders_pct_change = filter_month['Orders_pct_Difference'].iloc[0]
    
    if orders_difference > 0:
        color="green"
        style={"color":color, "font-size":"25px", "margin-left":"5px"}
        children_card1 = [
            html.Div(className="ml-3", children=[
                html.P("Commandes", className="text-black d-inline"), 
                html.Br(),
                html.P([DashIconify(icon="bx:dollar", width=10, color="gray"), html.Span(f"{orders_placed:,.0f}", className="text-black"), html.Span("USD", style={"color":"#777", "font-size":"15px", "margin-left":"4px"})], className="solde"),
                dmc.Text([DashIconify(icon="bxs:up-arrow", width=15, inline=True, color=color), f"+{orders_difference:,.0f}$", f" ({orders_pct_change:,.0f}%)"], style={"color": color}),
                html.Span("Par rapport au mois précédent")
            ])
        ]
        
    if orders_difference < 0:
        color="red"
        style={"color":color, "font-size":"25px", "margin-left":"5px"} #  
        children_card1 = [
            html.Div(className="ml-3", children=[
                html.P("Commandes", className="text-black d-inline"), #
                html.Br(),
                html.P([DashIconify(icon="bx:dollar", width=10, color="gray"), f"{orders_placed:,.0f}", html.Span("USD", style={"color":"#777", "font-size":"15px", "margin-left":"4px"})], className="solde"),
                dmc.Text([DashIconify(icon="bxs:down-arrow", width=15, inline=True, color=color), f"{orders_difference:,.0f}$", " ", f"({orders_pct_change:,.0f}%)"], style={"color": color}),
                html.Span("Par rapport au mois précédent")
            ])
        ]
        
    if orders_difference == 0:
        style={"font-size":"35px", "margin-left":"5px"}
        color=None
        children_card1 = [
            html.Div(className="ml-3", children=[
                html.P("Commandes", className="text-black d-inline"), #
                html.Br(),
                html.P([DashIconify(icon="bx:dollar", width=10, color="gray"), f"{orders_placed:,.0f}", html.Span("USD", style={"color":"#777", "font-size":"15px", "margin-left":"4px"})], className="solde"),
                dmc.Text([f"{orders_difference:,.0f}$", f" ({orders_pct_change:,.0f}%)"], style={"color": color}),
                html.Span("Par rapport au mois précédent")
            ])
        ]
    
    linecolor="rgb(31, 149, 233)"
    fillcolor="rgba(122, 147, 236, 0.192)"
    fig = go.Figure(
        go.Scatter(
            x=df['Months'], y=df['Orders Placed'],    
            mode="lines+markers", line=dict(color=linecolor, width=1.6),
            hoverinfo="text", marker=dict(size=3.5, symbol="square"), fillcolor=fillcolor,
            stackgroup=True,
            hovertext=
            "Mois: " + df['Months'].astype(str) + "<br>" +
            "Commandes passées: " + [f"${x:,.0f}" for x in df['Orders Placed']] + "<br>"
        )
    )
    
    fig.update_layout(**update_layout)
             
    return children_card1, fig

# ------------

@callback(
    Output("card4", "children"),
    Output("graph-card4", "figure"),
    Input("select-month", "value")
)
def render_cards_content(month):
    if month is None:
        raise PreventUpdate
    
    df = data.copy()
    # Calculate difference between two months
    df['Customers_Difference'] = df['Customers'].diff()
    # Calculate percentage change difference between two months
    df['Customers_pct_Difference'] = (df['Customers'].pct_change()) * 100
    df['Customers_Difference'] = df['Customers_Difference'].fillna(0)
    filter_month = df[df['Months'] == month]
    customers = filter_month['Customers'].iloc[0]
    Customers_difference = filter_month['Customers_Difference'].iloc[0]
    Customers_pct_change = filter_month['Customers_pct_Difference'].iloc[0]
    
    if Customers_difference > 0:
        color="green"
        style={"color":color, "font-size":"25px", "margin-left":"5px"}
        children_card1 = [
            html.Div(className="ml-3", children=[
                html.P("Clients", className="text-black d-inline"), 
                html.Br(),
                html.P([DashIconify(icon="bx:dollar", width=10, color="gray"), html.Span(f"{customers:,.0f}", className="text-black"), html.Span("USD", style={"color":"#777", "font-size":"15px", "margin-left":"4px"})], className="solde"),
                dmc.Text([DashIconify(icon="bxs:up-arrow", width=15, inline=True, color=color), f"+{Customers_difference:,.0f}$", f" ({Customers_pct_change:,.0f}%)"], style={"color": color}),
                html.Span("Par rapport au mois précédent")
            ])
        ]
        
    if Customers_difference < 0:
        color="red"
        style={"color":color, "font-size":"25px", "margin-left":"5px"} #  
        children_card1 = [
            html.Div(className="ml-3", children=[
                html.P("Clients", className="text-black d-inline"), #
                html.Br(),
                html.P([DashIconify(icon="bx:dollar", width=10, color="gray"), f"{customers:,.0f}", html.Span("USD", style={"color":"#777", "font-size":"15px", "margin-left":"4px"})], className="solde"),
                dmc.Text([DashIconify(icon="bxs:down-arrow", width=15, inline=True, color=color), f"{Customers_difference:,.0f}$", " ", f"({Customers_pct_change:,.0f}%)"], style={"color": color}),
                html.Span("Par rapport au mois précédent")
            ])
        ]
        
    if Customers_difference == 0:
        style={"font-size":"35px", "margin-left":"5px"}
        color=None
        children_card1 = [
            html.Div(className="ml-3", children=[
                html.P("Clients", className="text-black d-inline"), #
                html.Br(),
                html.P([DashIconify(icon="bx:dollar", width=10, color="gray"), f"{customers:,.0f}", html.Span("USD", style={"color":"#777", "font-size":"15px", "margin-left":"4px"})], className="solde"),
                dmc.Text([f"{Customers_difference:,.0f}$", f" ({Customers_pct_change:,.0f}%)"], style={"color": color}),
                html.Span("Par rapport au mois précédent")
                
            ])
        ]
        
    linecolor="rgb(31, 149, 233)"
    fillcolor="rgba(122, 147, 236, 0.192)"
    fig = go.Figure(
        go.Scatter(
            x=df['Months'], y=df['Customers'],    
            mode="lines+markers", line=dict(color=linecolor, width=1.6),
            hoverinfo="text", marker=dict(size=3.5, symbol="square"), fillcolor=fillcolor,
            stackgroup=True,
            hovertext=
            "Mois: " + df['Months'].astype(str) + "<br>" +
            "Clients: " + [f"${x:,.0f}" for x in df['Customers']] + "<br>"
        )
    )
    
    fig.update_layout(**update_layout)
             
    return children_card1, fig

# ------------

@callback(
    Output("card5", "children"),
    Output("graph-card5", "figure"),
    Input("select-month", "value")
)
def render_cards_content(month):
    if month is None:
        raise PreventUpdate
    
    df = data.copy()
    # Calculate difference between two months
    df['Items_Difference'] = df['Purchased Items'].diff()
    # Calculate percentage change difference between two months
    df['Items_pct_Difference'] = (df['Purchased Items'].pct_change()) * 100
    df['Items_Difference'] = df['Items_Difference'].fillna(0)
    filter_month = df[df['Months'] == month]
    items = filter_month['Purchased Items'].iloc[0]
    items_difference = filter_month['Items_Difference'].iloc[0]
    items_pct_change = filter_month['Items_pct_Difference'].iloc[0]
    
    if items_difference > 0:
        color="green"
        style={"color":color, "font-size":"25px", "margin-left":"5px"}
        children_card1 = [
            html.Div(className="ml-3", children=[
                html.P("Articles achetés", className="text-black d-inline"), 
                html.Br(),
                html.P([DashIconify(icon="bx:dollar", width=10, color="gray"), html.Span(f"{items:,.0f}", className="text-black"), html.Span("USD", style={"color":"#777", "font-size":"15px", "margin-left":"4px"})], className="solde"),
                dmc.Text([DashIconify(icon="bxs:up-arrow", width=15, inline=True, color=color), f"+{items_difference:,.0f}$", f" ({items_pct_change:,.0f}%)"], style={"color": color}),
                html.Span("Par rapport au mois précédent")
            ])
        ]
        
    if items_difference < 0:
        color="red"
        style={"color":color, "font-size":"25px", "margin-left":"5px"} #  
        children_card1 = [
            html.Div(className="ml-3", children=[
                html.P("Articles achetés", className="text-black d-inline"), #
                html.Br(),
                html.P([DashIconify(icon="bx:dollar", width=10, color="gray"), f"{items:,.0f}", html.Span("USD", style={"color":"#777", "font-size":"15px", "margin-left":"4px"})], className="solde"),
                dmc.Text([DashIconify(icon="bxs:down-arrow", width=15, inline=True, color=color), f"{items_difference:,.0f}$", " ", f"({items_pct_change:,.0f}%)"], style={"color": color}),
                html.Span("Par rapport au mois précédent")
            ])
        ]
        
    if items_difference == 0:
        style={"font-size":"35px", "margin-left":"5px"}
        color=None
        children_card1 = [
            html.Div(className="ml-3", children=[
                html.P("Clients", className="text-black d-inline"), #
                html.Br(),
                html.P([DashIconify(icon="bx:dollar", width=10, color="gray"), f"{items:,.0f}", html.Span("USD", style={"color":"#777", "font-size":"15px", "margin-left":"4px"})], className="solde"),
                dmc.Text([f"{items_difference:,.0f}$", f" ({items_pct_change:,.0f}%)"], style={"color": color}),
                html.Span("Par rapport au mois précédent")
                
            ])
        ]
    
    linecolor="rgb(31, 149, 233)"
    fillcolor="rgba(122, 147, 236, 0.192)"
    fig = go.Figure(
        go.Scatter(
            x=df['Months'], y=df['Purchased Items'],    
            mode="lines+markers", line=dict(color=linecolor, width=1.6),
            hoverinfo="text", marker=dict(size=3.5, symbol="square"), fillcolor=fillcolor,
            stackgroup=True,
            hovertext=
            "Mois: " + df['Months'].astype(str) + "<br>" +
            "Articles achetés: " + [f"${x:,.0f}" for x in df['Purchased Items']] + "<br>"
        )
    )
    
    fig.update_layout(**update_layout)
             
    return children_card1, fig


# ------------

@callback(
    Output("card6", "children"),
    Output("graph-card6", "figure"),
    Input("select-month", "value")
)
def render_cards_content(month):
    if month is None:
        raise PreventUpdate
    
    df = data.copy()
    # Calculate sales
    df['Sales'] = df['Orders Placed']
    # Calculate conversion rate
    df['Conversion Rate'] = ((df['Sales']) / (df['Inquiries'])) * 100
    # Calculate difference between two months
    df['Conversion_Difference'] = df['Conversion Rate'].diff()
    # Calculate percentage change difference between two months
    df['Conversion_pct_Difference'] = (df['Conversion Rate'].pct_change()) * 100
    df['Conversion_Difference'] = df['Conversion_Difference'].fillna(0)
    filter_month = df[df['Months'] == month]
    conversion = filter_month['Conversion Rate'].iloc[0]
    conversion_difference = filter_month['Conversion_Difference'].iloc[0]
    conversion_pct_change = filter_month['Conversion_pct_Difference'].iloc[0]
    
    if conversion_difference > 0:
        color="green"
        style={"color":color, "font-size":"25px", "margin-left":"5px"}
        children_card1 = [
            html.Div(className="ml-3", children=[
                html.P("Taux de conversion", className="text-black d-inline"), 
                html.Br(),
                html.P([DashIconify(icon="bx:dollar", width=10, color="gray"), html.Span(f"{conversion:,.0f}", className="text-black"), html.Span("USD", style={"color":"#777", "font-size":"15px", "margin-left":"4px"})], className="solde"),
                dmc.Text([DashIconify(icon="bxs:up-arrow", width=15, inline=True, color=color), f"+{conversion_difference:,.0f}$", f" ({conversion_pct_change:,.0f}%)"], style={"color": color}),
                html.Span("Par rapport au mois précédent")
            ])
        ]
        
    if conversion_difference < 0:
        color="red"
        style={"color":color, "font-size":"25px", "margin-left":"5px"} #  
        children_card1 = [
            html.Div(className="ml-3", children=[
                html.P("Taux de conversion", className="text-black d-inline"), #
                html.Br(),
                html.P([DashIconify(icon="bx:dollar", width=10, color="gray"), f"{conversion:,.0f}", html.Span("USD", style={"color":"#777", "font-size":"15px", "margin-left":"4px"})], className="solde"),
                dmc.Text([DashIconify(icon="bxs:down-arrow", width=15, inline=True, color=color), f"{conversion_difference:,.0f}$", " ", f"({conversion_pct_change:,.0f}%)"], style={"color": color}),
                html.Span("Par rapport au mois précédent")
            ])
        ]
        
    if conversion_difference == 0:
        style={"font-size":"35px", "margin-left":"5px"}
        color=None
        children_card1 = [
            html.Div(className="ml-3", children=[
                html.P("Taux de conversion", className="text-black d-inline"), #
                html.Br(),
                html.P([DashIconify(icon="bx:dollar", width=10, color="gray"), f"{conversion:,.0f}", html.Span("USD", style={"color":"#777", "font-size":"15px", "margin-left":"4px"})], className="solde"),
                dmc.Text([f"{conversion_difference:,.0f}$", f" ({conversion_pct_change:,.0f}%)"], style={"color": color}),
                html.Span("Par rapport au mois précédent")
                
            ])
        ]
    
    linecolor="rgb(31, 149, 233)"
    fillcolor="rgba(122, 147, 236, 0.192)"
    fig = go.Figure(
        go.Scatter(
            x=df['Months'], y=df['Conversion Rate'],    
            mode="lines+markers", line=dict(color=linecolor, width=1.6),
            hoverinfo="text", marker=dict(size=3.5, symbol="square"), fillcolor=fillcolor,
            stackgroup=True,
            hovertext=
            "Mois: " + df['Months'].astype(str) + "<br>" +
            "Conversion: " + [f"${x:,.0f}" for x in df['Conversion Rate']] + "<br>"
        )
    )
    
    fig.update_layout(**update_layout)
             
    return children_card1, fig

# ------------

@callback(
    Output("sales_vs_target", "figure"),
    Input("type-graph", "value"),)
def update_sales_target_graph(type_graph):
    df = data.copy()
    df["below_target"] = np.where(df["Revenues"] < df["Target"], df["Revenues"], 0)
    
    if type_graph == "bar":
        visible=True
        gridcolor="rgba(112, 112, 112, 0.18)"
        hoverinfo="text"
        showgrid=False
        fig = go.Figure(
            go.Bar(
                x=df["Months"],
                y=df["Revenues"],
                width = 0.6,
                marker=dict(color='rgb(31, 149, 233)'),
                name="Au dessus de la cible",
                hoverinfo=hoverinfo,
                hovertext="Mois: " + df["Months"].astype(str) + "<br>" +
                "Revenues: " + [f"{x:,.0f}" for x in df["Revenues"]] + "<br>"
            )
        )
        
        fig.add_bar(
            x=df["Months"],
            y=df["below_target"],
            width = 0.6,
            marker=dict(color='firebrick'),
            name="En dessous de la cible",
            hoverinfo=hoverinfo,
            hovertext="skip"
        )
        
        fig.add_scatter(
            x=df["Months"],
            y=df["Target"],   
            mode="lines+markers", 
            marker=dict(size=10, symbol="circle", color="orange"),
            line=dict(color='green', width=3),
            name="cible",
            hoverinfo=hoverinfo,
            hovertext="Mois: " + df["Months"].astype(str) + "<br>" +
                "Cible: " + [f"{x:,.0f}" for x in df["Target"]] + "<br>"
        )
        
    if type_graph == "area":
        visible = False
        gridcolor="rgba(112, 112, 112, 0.18)"
        showgrid=True
        hoverinfo="skip"
        fig = go.Figure(
            go.Scatter(
                x=df["Months"],
                y=df["Target"],  
                mode="lines+markers+text",
                marker=dict(size=8),
                line=dict(width=3),
                text=df["Target"], 
                textposition="top left",
                texttemplate="$" + "%{text:,.2s}",
                textfont=dict(size=13),
                name="cible",
                hoverinfo=hoverinfo
            )
        )
        
        fig.add_scatter(
            x=df["Months"],
            y=df["Revenues"],  
            mode="lines+markers+text",
            line=dict(width=3),
            marker=dict(size=8),
            text=df["Revenues"], 
            textposition="top left",
            texttemplate="$" + "%{text:,.2s}",
            textfont=dict(size=13),
            name="Revenues",
            hoverinfo=hoverinfo
        )
    
    fig.update_layout(
        barmode="overlay",
        height=408,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        template="simple_white",
        margin=dict(autoexpand=True, l=0, r=0, t=0, b=0),   
        xaxis=dict(
            visible = True,
            showgrid=showgrid,
            gridcolor=gridcolor,
            tickfont=dict(
                family="serif"
            )
        ),
        yaxis=dict(
            showline=False,
            showgrid=True,
            gridcolor="rgba(112, 112, 112, 0.18)",
            ticks="",
            visible = visible,
            tickprefix="$",
            tickformat=",.0f",
            tickfont=dict(
                family="serif"
            )
        ),
        legend=dict(
            orientation="h",
            xanchor="left", yanchor="bottom",
            x=.2, y=-.25
        )
    )
    
    return fig

# ------------

@callback(
    Output("avg_sales_customers", "children"),
    Output("avg_sales_customers_graph", "figure"),
    Input("select-month", "value")
)
def update_avg_sales_customers_graphand_title(month):
    if month is None: raise PreventUpdate
    
    df = data.copy()
    df["AVG / Customers"] = df["Revenues"] / df["Customers"]
    filter_month = df[df.Months == month]
    average_sale_per_customer = filter_month["AVG / Customers"].iloc[0]
    
    children_title = [
        html.Small("Solde moyen des ventes par clients", className="sub-avg ml-3"), html.Br(),
        html.Span([
            DashIconify(icon="bx:dollar", width=20, color="gray"), 
            f"{average_sale_per_customer:,.0f}", 
            html.Span("USD", style={"color":"#777", "font-size":"20px", "margin-left":"4px"})
        ], className="avg ml-3")
    ]
    
    fig = go.Figure(
        go.Scatter(
            x=df["Months"],
            y=df["AVG / Customers"],
            mode="lines", 
            line=dict(color="firebrick", shape="spline", width=2.2),
            hoverinfo="text", 
            textfont=dict(size=14),
            hovertext=
            "Mois: " + df['Months'].astype(str) + "<br>" +
            "Solde: " + [f"${x:,.0f}" for x in df["AVG / Customers"]] + "<br>"
        )
    )
    
    fig.update_layout(
        height=90,
        hovermode="x",
        template="plotly_dark",
        margin=dict(autoexpand=True, l=0, r=0, b=0, t=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(
            showline=True,
            linecolor='white',
            showticklabels=True,
            gridcolor="rgba(79, 79, 79, 0.113)",
            showgrid=True,
            tickangle=90,
            tickfont=dict(
                color="black",
                size=10,
                family="serif",
            )
        ),
        yaxis=dict(
            showticklabels=False,
            showline=False,
            showgrid=False
        ),
        hoverlabel=dict(
            bgcolor="white",
            bordercolor="rgba(0,0,0,0)",
            font=dict(
                color="black",
                size=11,
                family="serif"
            )
        )
    )
    
    return children_title, fig
    
# ------------

@callback(
    Output("avg_ticket_sales", "children"),
    Output("avg_ticket_sales_graph", "figure"),
    Input("select-month", "value")
)
def update_avg_sales_customers_graphand_title(month):
    if month is None: raise PreventUpdate
    
    df = data.copy()
    df['AVG Ticket Sales'] = df['Revenues'] / df['Orders Placed']
    filter_month = df[df.Months == month]
    average_ticket_sales = filter_month["AVG Ticket Sales"].iloc[0]
    
    children_title = [
        html.Small("Ventes moyenne des billets", className="sub-avg ml-3"), html.Br(),
        html.Span([
            DashIconify(icon="bx:dollar", width=20, color="gray"), 
            f"{average_ticket_sales:,.0f}", 
            html.Span("USD", style={"color":"#777", "font-size":"20px", "margin-left":"4px"})
        ], className="avg ml-3")
    ]
    
    fig = go.Figure(
        go.Scatter(
            x=df["Months"],
            y=df['AVG Ticket Sales'],
            mode="lines", 
            line=dict(color="firebrick", shape="spline", width=2.2),
            hoverinfo="text",
            #stackgroup=True,
            hovertext=
            "Mois: " + df['Months'].astype(str) + "<br>" +
            "Solde: " + [f"${x:,.0f}" for x in df['AVG Ticket Sales']] + "<br>"
        )
    )
    
    fig.update_layout(
        height=90,
        hovermode="x",
        template="plotly_dark",
        margin=dict(autoexpand=True, l=0, r=0, b=0, t=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(
            showline=True,
            linecolor = 'white',
            showticklabels=True,
            gridcolor="rgba(79, 79, 79, 0.113)",
            showgrid=True,
            tickangle = 90,
            tickfont=dict(
                color="black",
                size=10,
                family="serif",
            )
        ),
        yaxis=dict(
            showticklabels=False,
            showline=False,
            showgrid=False
        ),
        hoverlabel=dict(
            bgcolor="white",
            bordercolor="rgba(0,0,0,0)",
            font=dict(
                color="black",
                size=11,
                family="serif"
            )
        )
    )
    
    return children_title, fig

# ------------

@callback(
    Output("growth_graph", "figure"),
    Input("select-month", "value")
)
def render_cards_content(month):
    df = data.copy()
    df["Color"] = np.where(df["pct_change"] > 0, "green", "firebrick")
    
    fig = go.Figure(
        go.Bar(
            x=df["Months"],
            y=df["pct_change"],
            text=df["pct_change"],
            texttemplate="%{text:.1f}%",
            textposition="outside",
            width=.7,
            textfont=dict(
                size=15
            ),
            marker=dict(color=df["Color"])
        )
    )
    
    fig.update_layout(
        height=300,
        template="simple_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(autoexpand=True, l=0, r=0, b=0, t=0),
        font=dict(
            family="serif",
            color="black",
        ),
        yaxis=dict(
            ticks="",
            showgrid=True,
            gridcolor="rgba(112, 112, 112, 0.18)",
            showticklabels=False,
            showline=False,
        )
    )
    
    return fig

# ------------

@callback(
    Output("Diagrammes_entonoir", "figure"),
    Input("select-month", "value")
)
def update_funnel_chart(month):
    if month is None: raise PreventUpdate
    
    filter_month = data[data.Months == month].copy()
    inquiries = filter_month["Inquiries"].iloc[0]
    lead = filter_month['Lead'].iloc[0]
    opportunity = filter_month['Opportunity'].iloc[0]
    sales = filter_month['Sales'].iloc[0]
    object_data = [['Inquiries', inquiries], ['Lead', lead], ['Opportunity', opportunity], ['Sales', sales]]
    df = pd.DataFrame(object_data, columns = ['Text', 'Value'])
    df = df.sort_values(by = ['Value'], ascending = False)
    
    fig = go.Figure(
        go.Funnel(
            x=df["Value"], y=df["Text"],
            hoverinfo = 'skip'
        )
    )
    
    fig.update_layout(
        height=300,
        template="simple_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(autoexpand=True, l=0, r=0, b=0, t=0),
    )
    
    return fig

#------------

@callback(
    Output("revenues_target", "figure"),
    Input("select-month", "value")
)
def update_graph(select_month):
    if select_month is None:
        raise PreventUpdate
    else:
        filter_month = data[data['Months'] == select_month]
        target = filter_month['Target'].iloc[0]
        revenues = filter_month['Revenues'].iloc[0]
        object_data = [['Target', target], ['Revenues', revenues]]
        df2 = pd.DataFrame(object_data, columns = ['Text', 'Value'])
        
    fig = go.Figure(
        go.Bar(
            y=df2["Text"], x=df2["Value"],
            text = df2['Value'],
            texttemplate = '$' + '%{text:,.0f}',
            textposition = 'inside',
            width = 0.5,
            hoverinfo = 'skip',
            orientation="h"
        )
    )
    
    fig.update_layout(
        height=300,
        template="simple_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(autoexpand=True, l=0, r=0, b=0, t=0),
        xaxis = dict(
            tickprefix = '$',
            tickformat = ',.0f',
        )
    )
    
    return fig

# ------------

@callback(
    Output('sales_profit', 'figure'),
    Input('select-month', 'value')
)
def update_graph(select_month):
    if select_month is None:
        raise PreventUpdate
    else:
        # Calculate % profit
        data['% Profit'] = (data['Profit'] / data['Revenues']) * 100
        filter_month = data[data['Months'] == select_month]
        percentage_profit = filter_month['% Profit'].iloc[0]
        remaining_percentage_profit = 100 - (filter_month['% Profit'].iloc[0])
        colors = ['rgb(31, 149, 233)', 'white']
        
    fig=go.Figure(
        go.Pie(
            labels = ['', ''],
            values = [percentage_profit, remaining_percentage_profit],
            marker = dict(colors = colors, line=dict(color='rgb(31, 149, 233)', width=2)),
            hoverinfo = 'skip',
            textinfo = 'text',
            hole = .7,
            rotation = 90
        )
    )
    
    fig.update_layout(
        height=300,
        template="simple_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(autoexpand=True, l=50, r=50, b=50, t=50),
        showlegend = False,
        xaxis = dict(
            tickprefix = '$',
            tickformat = ',.0f',
        ),
        annotations=[dict(
            text=f"{percentage_profit:,.0f}%",
            showarrow=False,
            font=dict(size=20)
        )]
    )
    
    return fig
                        
# ------------

@callback(
    Output('monthly_goal', 'figure'),
    Input('select-month', 'value')
)
def update_graph(select_month):
    if select_month is None:
        raise PreventUpdate
    else:
        # Calculate % target
        data['% Target'] = (data['Revenues'] / data['Target']) * 100
        filter_month = data[data['Months'] == select_month]
        percentage_target = filter_month['% Target'].iloc[0]
        percentage_target1 = float(100.00)
        remaining_percentage_target = 100 - (filter_month['% Target'].iloc[0])
        colors = ['rgb(31, 149, 233)', 'white']
            
    if percentage_target > 100:
        fig=go.Figure(
            go.Pie(
                labels = [''],
                values = [percentage_target1],
                marker = dict(colors = colors, line=dict(color='rgb(31, 149, 233)', width=2)),
                hoverinfo = 'skip',
                textinfo = 'text',
                hole = .7,
                rotation = 90
            )
        )
 
    else:
        fig=go.Figure(
            go.Pie(
                labels = ['', ''],
                values = [percentage_target, remaining_percentage_target],
                marker = dict(colors = colors, line=dict(color='rgb(31, 149, 233)', width=2)),
                hoverinfo = 'skip',
                textinfo = 'text',
                hole = .7,
                rotation = 90
            )
        )
    
    fig.update_layout(
        height=300,
        template="simple_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(autoexpand=True, l=50, r=50, b=50, t=50),
        showlegend = False,
        xaxis = dict(
            tickprefix = '$',
            tickformat = ',.0f',
        ),
        annotations=[dict(
            text=f"{percentage_target:,.0f}%",
            showarrow=False,
            font=dict(size=20)
        )]
    )
    
    return fig
                        
# ------------

@callback(
    Output('YTD_goal', 'figure'),
    Input('select-month', 'value')
)
def update_graph(select_month):
    if select_month is None:
        raise PreventUpdate
    else:
        total_revenues = data['Revenues'].sum()
        total_target = data['Target'].sum()
        ytd_goal = (total_revenues / total_target) * 100
        colors = ['rgb(31, 149, 233)', 'white']
        
    fig=go.Figure(
        go.Pie(
            labels = [''],
            values = [ytd_goal],
            marker = dict(colors = colors, line=dict(color='rgb(31, 149, 233)', width=2)),
            hoverinfo = 'skip',
            textinfo = 'text',
            hole = .7,
            rotation = 90
        )
    )
    
    fig.update_layout(
        height=300,
        template="simple_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(autoexpand=True, l=50, r=50, b=50, t=50),
        showlegend = False,
        xaxis = dict(
            tickprefix = '$',
            tickformat = ',.0f',
        ),
        annotations=[dict(
            text=f"{ytd_goal:,.0f}%",
            showarrow=False,
            font=dict(size=20)
        )]
    )
    
    return fig
                        
