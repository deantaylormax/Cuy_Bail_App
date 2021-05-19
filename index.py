import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
pd.set_option('mode.chained_assignment', None)
from app import server

from app import app
from apps import bond_judge, bond_orc #import all apps for entire dashboard here

#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])

app.layout = html.Div([
                dbc.Row(
                    dbc.NavbarSimple(
                    children=[
                        dbc.DropdownMenu(
                            children=[
                                dbc.DropdownMenuItem("Search by Ohio Revised Code Section", href="/apps/bond_orc"),
                                dbc.DropdownMenuItem("Search by Judge", href="/apps/bond_judge"),
                                    ],
                            nav=True,
                            in_navbar=True,
                            label="Racial Disparities in Bail by Cuyahoga County Judges", style ={'color':'#ffffff'}
                                        ),               
                            ], 
                    className = "sticky-top",
                    brand="Cuyhahoga County Data",
                    brand_href="www.lawstata.com",
                    color="primary",
                    dark=True,
                    
                                        )),
                dbc.Row([
                        dbc.Col(),
                        dbc.Col(),
                        dbc.Col(),
                        ]),
                html.Br(),  #puts space between nav bar and content
                dcc.Location(id='url', refresh=False),
                html.Div(id='page-content'),
                    ], style={
                                'position': 'relative',
                                'zIndex': '2',
                            })

@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/apps/bond_judge':
        return bond_judge.layout
    else:
        return bond_orc.layout

if __name__ == '__main__':
    app.run_server(host='127.0.0.1', debug=True)