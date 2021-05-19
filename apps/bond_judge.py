import itertools
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_bootstrap_components as dbc
from dash_core_components.RadioItems import RadioItems
import csv
pd.options.mode.chained_assignment = None  # default='warn'
from datetime import datetime
import time
from datetime import date
now = pd.to_datetime('now')
import plotly.express as px
from dash.dependencies import Input, Output

""" DATA AND VARIABLES """
df_2 = pd.read_pickle("data/bail.pkl")
df_2 = df_2.rename(columns={'bond_amt':'bail_amt'})

judge_lst_2 = sorted(list(set(df_2.judge)))
for i in judge_lst_2:
    if i == 'SHEEHAN_BJ':
        rem_word = i
        judge_lst_2.remove(rem_word)
        judge_lst_2.insert(0, rem_word)

judge_options_2 = [{'label':i, 'value':i} for i in judge_lst_2]

from app import app

#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])

judge_dropdown_2 = dcc.Dropdown(id='judge-dd-2', multi=False, value=judge_options_2[0]['value'],options=judge_options_2, style={'width':'50%', 'color':'#000000'}, clearable=False)

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
            dcc.Graph(id='bond-fig-2-avg', config={'displayModeBar':False}),
        ]
    ), className='float-box col-lg-9 mt-4',
    
), 

charge_dropdown_2 = dcc.Dropdown(
        id='charge-dd-2', multi=False, 
        options=[],
        value=[],
        style={'width':'50%', 'color':'#000000'}
    ),



table_card = dbc.Card(
    dbc.CardBody(
        [
            # html.H5(id='9-table-sub', children="", style={'text-align': 'center'}
            # ),
            html.Div(id='by-race-table'),
        ]
    ), className='float-box col-lg-12 mt-5',
    
), 

layout = dbc.Container([
                        dbc.Row(
                                dbc.Col(html.H1('Cuyahoga County Bail Statistics - 2009-2019*', style={'color':'#000000'})), className="mt-5 row justify-content-center", ),
                                html.P('Choose a Judge and ORC sections appearing in cases they have handled appear in dropdown below', style={'color':'#000000'}),
                        dbc.Row([
                                dbc.Col([
                                    dbc.Row(judge_dropdown_2),
                                    dbc.Row(charge_dropdown_2, className = 'mt-2'),
                                        ]),
                                ]),
                        dbc.Row([
                                dbc.Col([
                                    dbc.Row(html.H4(id='bond-header-2', style={'color':'#000000'}, className = 'mt-4', children="")),
                                    dbc.Row(bond_figure_2)
                                        ]),
                                dbc.Col([
                                    dbc.Row(html.H4(id='bond_avg-header-2', style={'color':'#000000'}, className = 'mt-4', children="")),
                                    dbc.Row(bond_fig_avg_2)
                                        ]),
                                ]),
                        # dbc.Row(table_card),
                            ])
# """ Callback Functions """
# """ for the status dropdown """
@app.callback(
    Output('charge-dd-2', 'options'),
    Output('charge-dd-2', 'value'),
    Input('judge-dd-2', 'value'))
def set_orc_options(judge):
    judge_choice = df_2[df_2['judge'] == judge]
    if judge == 'SHEEHAN_BJ':
        orc_lst = ['2903.04(A)','2903.06(A)(1)(A)', '2903.12', '2903.22', '2905.01(B)(2)', '2905.02(A)(2)', '2905.03(A)', '2907.03(A)(1)', '2907.03(A)(3)', '2907.07(B)', '2907.31(A)(1)', '2907.322(A)(1)', '2907.322(A)(2)', '2907.323(A)(1)', '2909.05(A)', '2909.05(B)(1)(B)', '2909.05(B)(2)', '2909.06(A)(1)', '2909.07(A)(1)', '2911.01(A)(1)','2911.01(A)(2)', '2911.01(A)(3)','2911.02(A)(3)','2911.12', '2911.12(A)(1)','2911.13(A)', '2911.13(B)', '2911.31(A)', '2913.02', '2913.02(A)(1)', '2913.02(A)(3)','2913.02(A)(4)', '2913.04(A)', '2913.05(A)', '2913.11(B)', '2913.21(C)', '2913.31(A)(2)', '2913.31(A)(3)','2913.42(A)(1)', '2913.51(A)', '2921(A)(3)', '2911.31(A)', '2913.02(A)(1)', '2913.02(A)(3)', '2913.04(A)', '2917.02(A)(3)', '2917.11', '2917.11(A)(1)', '2917.21(A)(2)', '2919.22(B)(1)', '2919.24(B)(1)', '2919.25(C)', '2919.27(A)(1)', '2921.02(C)', '2921.03(A)', '2921.05(B)', '2921.13(A)(2)', '2921.32(A)(2)', '2921.33(A)', '2921.33(B)', '2921.331(A)', '3772.99(E)(7)', '2921.34(A)(1)', '2921.36(A)(1)', '2921.36(A)(2)', '2921.38(B)', '2921.51.E', '2923.03(A)(2)', '2923.12(A)(1)', '2921.12(A)(2)', '2923.13(A)(2)', '2923.16(B)', '2923.16(D)(1)', '2923.17(A)', '2923.201(A)(2)', '2923.42(A)', '2925.02(A)(3)', '2925.03(A)(1)', '2925.03(A)(2)', '2925.11(A)', '2925.13(B)', '2925.14(C)(1)','2925.24(B)', '2950.05.E(1)', '2950.06.F']
    else:
        orc_lst = sorted(list(set(itertools.chain.from_iterable(judge_choice.charge_orc))))
    orc_lst = [x.strip(' ') for x in orc_lst]
    orc_lst = [x for x in orc_lst if x]
    # orc_lst = []
    # for i in orc_lst_raw:
    #     new_i = i.str.strip()
    #     orc_lst.append(new_i)
    # print(f'orc lst {orc_lst}')
    # print(f'the orc list is {len(orc_lst)} elements long')
        # orc_lst = sorted(list(set(judge_choice['charge_orc'])))
    value = orc_lst[0]  #makes the default value the first option in the status_lst
    return [{'label': i, 'value': i} for i in orc_lst], value

# # # """ callbacks  for ORC, then Judge charts """
@app.callback(
    Output('bond-fig-2', 'figure'),
    Output('bond-header-2', 'children'),
    Output('bond-fig-2-avg', 'figure'),
    Output('bond_avg-header-2', 'children'),
    # Output('by-race-table', 'children'),
    # Output('6-status-text', 'children'),
    Input("charge-dd-2", 'value'),
    Input("judge-dd-2", 'value'))
def update_orc_graph(charge, judge):
    charge_lst = [charge]
    # print(f'charge_lst = {charge_lst[0]}')
    main_df_2 = df_2[(df_2['judge'] == judge) & (df_2['charge_orc'].apply(lambda x: set(x).intersection(charge_lst)).astype(bool))]
    # print(f'main df 2 = {main_df_2}')


    all_judges = df_2[df_2['charge_orc'].apply(lambda x: set(x).intersection(charge_lst)).astype(bool)]
    # print(f'main_df_2 head = {main_df_2.head()}')
    # main_df_2 = df_2[(df_2['charge_orc'] == charge) & (df_2['judge'] == judge)] 
    total_cases_2 = main_df_2.shape[0]
    all_total_cases = all_judges.shape[0]
    if total_cases_2 == 1:
        bond_header_2 = f' Judge {judge} - - {total_cases_2} Case including charge {charge}'
    else:
        bond_header_2 = f' Judge {judge} - - {total_cases_2} Cases including charge {charge}'
    by_race_2 = main_df_2.groupby(['race']).mean().reset_index()
    all_by_race_2 = all_judges.groupby(['race']).mean().reset_index()
    by_race_2 = by_race_2.round({"bail_amt":0})
    all_by_race_2 = all_by_race_2.round({"bail_amt":0})
    by_race_2 = by_race_2.rename(columns={'race':'Defendant Race', 'bail_amt':'Average Bail Amount'})
    all_by_race_2 = all_by_race_2.rename(columns={'race':'Defendant Race', 'bail_amt':'Average Bail Amount'})

    bond_fig_2=px.bar(by_race_2,text='Average Bail Amount',x='Defendant Race', y='Average Bail Amount')
    all_bond_fig_2=px.bar(all_by_race_2,text='Average Bail Amount',x='Defendant Race', y='Average Bail Amount')
    # bond_fig_2.update_layout(showlegend=False)
    # bond_fig_avg_2=px.bar(by_race_2,
    #                 text='bail_amt',  #puts direct label on bar graph
    #                 x='race', y='bail_amt', color="race")
    # bond_fig_avg_2.update_layout(showlegend=False)
    bond_avg_header_2 = f'{all_total_cases} cases including ORC {charge} among all Judges'

    return bond_fig_2, bond_header_2, all_bond_fig_2, bond_avg_header_2

if __name__ == '__main__':
    app.run_server(debug=True)








    # """ CONTENT FOR ALL THE TEXT FIELDS """
    # master_status_number = final_df.SubjectId.nunique()
    # if status == 'All':
    #     master_status_text = f'All {master_status_number} Clients' 
    # else:
    #     master_status_text = f'{master_status_number} {status} Clients'

    # #average age stats_2
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
    # #     master_retailer_avg = df_2
    # # else:
    # #     master_retailer_avg = df_2[df_2['retailers'].str.contains(selected_retailer)]
    # # #Average Age stats_2
    
    
    # # #dataset averages
    # # master_dataset_avg_age = round(filtered_retailer['age'].mean(),1)
    # # master_dataset_avg_age_text = f'Average Age:  {master_dataset_avg_age}'
    # # master_dataset_avg_dur = round(filtered_retailer['total_use_years'].mean(),1)
    # # master_dataset_avg_dur_text = f'Average Years of Use:  {master_dataset_avg_dur}'
    # # #totals_2 for status chosen
    
   
    
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
