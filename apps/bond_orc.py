import itertools
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash_core_components.RadioItems import RadioItems
import csv
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
from datetime import datetime
import time
from datetime import date
now = pd.to_datetime('now')
import plotly.express as px
from dash.dependencies import Input, Output

""" DATA AND VARIABLES """
df = pd.read_pickle("data/bail.pkl")
df = df.rename(columns={'bond_amt':'bail_amt', 'race':'Defendant Race'})
# df = pd.read_csv("data/bail.csv")
orc_lst = sorted(list(set(itertools.chain.from_iterable(df.charge_orc))))
orc_lst = [x.strip(' ') for x in orc_lst]
orc_lst = [x for x in orc_lst if x]
orc_options = [{'label':i, 'value':i} for i in orc_lst]

from app import app

#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])

charge_dropdown = dcc.Dropdown(id='charge-dd', multi=False, value=orc_options[0]['value'],options=orc_options, style={'width':'50%', 'color':'#000000'}, clearable=False)

bond_fig = dbc.Card(
    dbc.CardBody(
        [
            dcc.Graph(id='bond-fig', config={'displayModeBar':False}),
        ]
    ), className='float-box col-lg-9 mt-4',
    
), 

bond_fig_avg = dbc.Card(
    dbc.CardBody(
        [
            dcc.Graph(id='bond-fig-avg', config={'displayModeBar':False}),
        ]
    ), className='float-box col-lg-9 mt-4',
    
), 

bond_figure_2 = dbc.Card(
    dbc.CardBody(
        [
            dcc.Graph(id='bond-fig-2', config={'displayModeBar':False}),
        ]
    ), className='float-box col-lg-9 mt-4',
    
), 

bond_fig_avg_2 = dbc.Card(
    dbc.CardBody(
        [
            dcc.Graph(id='bond-fig-avg-2', config={'displayModeBar':False}),
        ]
    ), className='float-box col-lg-9 mt-4',
    
), 

judge_dropdown = dcc.Dropdown(
        id='judge-dd', multi=False, 
        options=[],
        value=[],
        style={'width':'50%', 'color':'#000000'}
    ),




layout = dbc.Container([
                        dbc.Row(
                                dbc.Col(html.H1('Cuyahoga County Bail Statistics - 2009-2019*', style={'color':'#000000'})), className="mt-5 row justify-content-center", ),
                                html.P('Choose an Ohio Revised Code Section and all Judges having a case involving that section appear in dropdown below', style={'color':'#000000'}),
                        dbc.Row([
                                dbc.Col([
                                    dbc.Row(charge_dropdown, className = 'mt-5'),
                                    dbc.Row(judge_dropdown, className = 'mt-2'),
                                    html.Br(),
                                        ]),
                                ]),
                        dbc.Row(html.H1('Average Bail Imposed by Race', className="d-flex justify-content-center")),
                        dbc.Row([
                                dbc.Col([
                                    dbc.Row(html.P(id='bond-header', style={'color':'#000000'}, className = 'mt-4', children="")),
                                    dbc.Row(bond_fig)
                                        ]),
                                dbc.Col([
                                    dbc.Row(html.P(id='bond-avg-header', style={'color':'#000000'}, className = 'mt-4', children="")),
                                    dbc.Row(bond_fig_avg)
                                        ]),
                                ]),
                        # dbc.Row(table_card),
                            ])
# """ Callback Functions """
# """ for the status dropdown """
@app.callback(
    Output('judge-dd', 'options'),
    Output('judge-dd', 'value'),
    Input('charge-dd', 'value'))
def set_judge_options(charge):
    charge_lst = [charge]
    # print(f'charge is {charge}')
    # print(f'charge_lst {charge_lst}')
    charge_choice = df[df['charge_orc'].apply(lambda x: set(x).intersection(charge_lst)).astype(bool)]
    #make the judge list now based upon those judges that have any cases involving the selected charge
    # print(f' charge_choice head {charge_choice.head()}')
    charge_judge_lst = sorted(list(set(charge_choice['judge'])))
    for i in charge_judge_lst:
        if i == 'SHEEHAN_BJ':
            rem_word = i
            charge_judge_lst.remove(rem_word)
            charge_judge_lst.insert(0, rem_word)
    value = charge_judge_lst[0]  #makes the default value the first option in the status_lst
    return [{'label': i, 'value': i} for i in charge_judge_lst], value

# # # """ callbacks  for ORC, then Judge charts """
@app.callback(
    Output('bond-fig', 'figure'),
    Output('bond-header', 'children'),
    Output('bond-fig-avg', 'figure'),
    Output('bond-avg-header', 'children'),
    Input("charge-dd", 'value'),
    Input("judge-dd", 'value'))
def update_orc_graph(charge1, judge1):
    charge_lst = [charge1]
    main_df = df[(df['judge'] == judge1) & (df['charge_orc'].apply(lambda x: set(x).intersection(charge_lst)).astype(bool))]
    # print(f'main df {main_df.head()}')
    
    judge_cases = main_df.shape[0]
    if judge_cases == 1:
        bond_header = f' Judge {judge1} {judge_cases} Case including charge {charge1}'
    else:
        bond_header = f' Judge {judge1} {judge_cases} Cases including charge {charge1}'

    all_judges = df[df['charge_orc'].apply(lambda x: set(x).intersection(charge_lst)).astype(bool)]
    all_total_cases = all_judges.shape[0]
    #creates a df of the averages by race for the chosen orc that has been selected
    by_race = main_df.groupby(['Defendant Race']).mean().reset_index()
    all_by_race = all_judges.groupby(['Defendant Race']).mean().reset_index()
    by_race = by_race.round({"bail_amt":0})
    all_by_race = all_by_race.round({"bail_amt":0})
    by_race = by_race.rename(columns={'bail_amt':'Average Bail Amount'})
    all_by_race = all_by_race.rename(columns={'bail_amt':'Average Bail Amount'})
    bond_fig=px.bar(by_race,
                    text='Average Bail Amount',  #puts direct label on bar graph
                    x='Defendant Race', y='Average Bail Amount', color='Defendant Race')
    bond_fig.update_layout(showlegend=False)
    bond_fig_avg=px.bar(all_by_race,
                    text='Average Bail Amount',  #puts direct label on bar graph
                    x='Defendant Race', y='Average Bail Amount', color='Defendant Race')
    bond_fig_avg.update_layout(showlegend=False)
    bond_avg_header = f'Average Bail: {all_total_cases} cases including ORC {charge1}'


    return bond_fig, bond_header, bond_fig_avg, bond_avg_header

if __name__ == '__main__':
    app.run_server(debug=True)