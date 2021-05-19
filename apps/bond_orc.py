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
orc_lst = orc_lst = sorted(list(set(itertools.chain.from_iterable(df.charge_orc))))
orc_lst = [x.strip(' ') for x in orc_lst]
orc_lst = [x for x in orc_lst if x]
orc_options = [{'label':i, 'value':i} for i in orc_lst]

from app import app

#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])

charge_dropdown = dcc.Dropdown(id='charge-dd', multi=False, value=orc_options[0]['value'],options=orc_options, style={'width':'50%', 'color':'#000000'}, clearable=False)

# judge_dropdown_2 = dcc.Dropdown(id='judge-dd-2', multi=False, value=judge_options[0]['value'],options=judge_options, style={'width':'50%', 'color':'#000000'}, clearable=False)

bond_fig = dbc.Card(
    dbc.CardBody(
        [
            # html.H5("PRODUCT DATA", className="card-title"),
            
            # html.P(id='6-graph-sub', children=""
            # ),
            dcc.Graph(id='bond-fig', config={'displayModeBar':False}),
        ]
    ), className='float-box col-lg-9 mt-4',
    
), 

bond_fig_avg = dbc.Card(
    dbc.CardBody(
        [
            # html.H5("PRODUCT DATA", className="card-title"),
            
            # html.P(id='6-graph-sub', children=""
            # ),
            dcc.Graph(id='bond-fig-avg', config={'displayModeBar':False}),
        ]
    ), className='float-box col-lg-9 mt-4',
    
), 

bond_figure_2 = dbc.Card(
    dbc.CardBody(
        [
            # html.H5("PRODUCT DATA", className="card-title"),
            
            # html.P(id='6-graph-sub', children=""
            # ),
            dcc.Graph(id='bond-fig-2', config={'displayModeBar':False}),
        ]
    ), className='float-box col-lg-9 mt-4',
    
), 

bond_fig_avg_2 = dbc.Card(
    dbc.CardBody(
        [
            # html.H5("PRODUCT DATA", className="card-title"),
            
            # html.P(id='6-graph-sub', children=""
            # ),
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
    charge_choice = df[df['charge_orc'].apply(lambda x: set(x).intersection(charge_lst)).astype(bool)]
    #make the judge list now based upon those judges that have any cases involving the selected charge
    # print(judge_choice.head())
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
    judge_cases = main_df.shape[0]
    if judge_cases == 1:
        bond_header = f' Judge {judge1} {judge_cases} Case including charge {charge1}'
    else:
        bond_header = f' Judge {judge1} {judge_cases} Cases including charge {charge1}'

    all_judges = df[df['charge_orc'].apply(lambda x: set(x).intersection(charge_lst)).astype(bool)]
    all_total_cases = all_judges.shape[0]
    #creates a df of the averages by race for the chosen orc that has been selected
    by_race = main_df.groupby(['race']).mean().reset_index()
    all_by_race = all_judges.groupby(['race']).mean().reset_index()
    by_race = by_race.round({"bond_amt":0})
    all_by_race = all_by_race.round({"bond_amt":0})
    by_race = by_race.rename(columns={'race':'Defendant Race', 'bond_amt':'Average Bail Amount'})
    all_by_race = all_by_race.rename(columns={'race':'Defendant Race', 'bond_amt':'Average Bail Amount'})

    bond_fig=px.bar(by_race,
                    text='Average Bail Amount',  #puts direct label on bar graph
                    x='Defendant Race', y='Average Bail Amount', color="Defendant Race")
    bond_fig.update_layout(showlegend=False)
    bond_fig_avg=px.bar(all_by_race,
                    text='Average Bail Amount',  #puts direct label on bar graph
                    x='Defendant Race', y='Average Bail Amount', color="Defendant Race")
    bond_fig_avg.update_layout(showlegend=False)
    bond_avg_header = f'Average Bail: {all_total_cases} cases including ORC {charge1}'

    return bond_fig, bond_header, bond_fig_avg, bond_avg_header

if __name__ == '__main__':
    app.run_server(debug=True)








    # """ CONTENT FOR ALL THE TEXT FIELDS """
    # master_status_number = final_df.SubjectId.nunique()
    # if status == 'All':
    #     master_status_text = f'All {master_status_number} Clients' 
    # else:
    #     master_status_text = f'{master_status_number} {status} Clients'

    # #average age stats
    # if selected_retailer == 'All':
    #     master_retailer = final_df
    # else:
    #     master_retailer = final_df[final_df['retailers'].str.contains(selected_retailer)]
    # master_avg_age_retailer = round(master_retailer['age'].mean(), 1)
    # master_avg_age_retailer_text = f'Average Age:  {master_avg_age_retailer}'
    # # #average duration text
    # master_avg_dur = round(master_retailer['total_use_years'].mean(),1)
    # master_avg_dur_text = f'Average Years of Use:  {master_avg_dur}'
    # #Use years text
    # master_years_use_header = f"Years Used {use_years[0]} to {use_years[1]}"
    # #duration header text
    # master_dur_use_header = f'Duration Used {duration[0]} to {duration[1]} years'

    # # if selected_retailer == 'All':
    # #     master_retailer_avg = df
    # # else:
    # #     master_retailer_avg = df[df['retailers'].str.contains(selected_retailer)]
    # # #Average Age Stats
    
    
    # # #dataset averages
    # # master_dataset_avg_age = round(filtered_retailer['age'].mean(),1)
    # # master_dataset_avg_age_text = f'Average Age:  {master_dataset_avg_age}'
    # # master_dataset_avg_dur = round(filtered_retailer['total_use_years'].mean(),1)
    # # master_dataset_avg_dur_text = f'Average Years of Use:  {master_dataset_avg_dur}'
    # # #totals for status chosen
    
   
    
    # # #age header text
    # master_age_header = f'Clients  {age[0]} to {age[1]} years old'
    # # #the graph header
    # # master_graph_header = f'{master_status_text} using any Product {years[0]} - {years[1]}, from {duration[0]} - {duration[1]} years duration, ages {age[0]} - {age[1]}'
    # # master_table_header = f'{master_status_text} using any Product {years[0]} - {years[1]}, from {duration[0]} - {duration[1]} years duration, ages {age[0]} - {age[1]}'

    # # final_data = filtered_retailer.groupby(['formulation'])['SubjectId'].count().reset_index()
    # # final_data.drop_duplicates(columns=['SubjectId'], inplace=True)
    # # final_data = final_data.rename(columns={'SubjectId':'Total'})
    # # final_data = final_data[final_data['Total'] >0]
    # # print(f'final data rows = {final_data.shape[0]}')
    # # print(f'final data head {final_data.head()}')
    # # print(final_data.head())
    
    # # master_table_fig =html.Div([dash_table.DataTable
    # #             (id='table',
    # #             style_header={'backgroundColor': '#df691a', 'color': '#ffffff'},
	# # 			columns=[{"name": i, "id": i} for i in filtered_retailer.   columns if i != 'retailers'],
	# # 			page_size=10,
    # #             style_as_list_view=True,
	# # 			data=filtered_retailer.to_dict("records"),
    # #             # export_format="csv",
    # #             export_format="xlsx",
    # #             filter_action="native",
    # #             sort_action="native",
	# # 			style_cell={'width': '300px',
    # #                         'height': '20px',
    # #                         'textAlign': 'left', 
    # #                         'backgroundColor': 'rgb(43, 62, 80)',
    # #                         'color': 'white'}
    # #             ),
    # #                     ])
    # # # page_title = 'Master Usage Data'
    # # return master_product_fig, master_avg_age_text_retailer, master_avg_dur_text, master_status_text, master_years_use_header, master_dur_use_header, master_age_header, master_table_fig, master_graph_header, master_table_header, master_dataset_avg_age_text, master_dataset_avg_dur_text

    # # return master_product_fig, master_avg_age_text_retailer, master_avg_dur_text, master_status_text, master_years_use_header, master_dur_use_header, master_age_header, master_graph_header, master_dataset_avg_age_text, master_dataset_avg_dur_text

    # return master_product_fig, master_status_text, master_avg_age_retailer_text, master_avg_dur_text, master_years_use_header, master_dur_use_header, master_age_header
