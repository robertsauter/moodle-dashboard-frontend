import dash
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from group_services.overall_progress_service import fetch_grades
import pandas as pd
from dash.dependencies import Input, Output


dash.register_page(__name__,
                   path='/overall_progress',
                   name='Overall progress',
                   title='Overall progress')

layout = html.Div([
    html.Div(id='dataDependingOnUser')
])

@dash.callback(
    Output('dataDependingOnUser', 'children'),
    Input('userId', 'data'),
)
def fetch_data_on_user(user_id):

        user_data = fetch_grades(user_id)

        # This is the JSON object, that you can use to populate your visualizations with data :)
        data = user_data

        # getting the dataframes from the json file
        user_all_activities = pd.read_json(data[0])
        unseen = pd.read_json(data[1])
        perc = pd.read_json(data[2])
        print(user_all_activities)

        # getting the percentages from the perc df
        quiz_perc = perc[0][0]
        assignment_perc = perc[0][1]
        url_perc = perc[0][2]
        file_perc = perc[0][3]

        # putting together data for quiz-table
        quiz_data = pd.DataFrame({'Completed':user_all_activities[user_all_activities['Component'] == "Quiz"]['Event context'], 'Uncompleted':unseen[unseen['Component'] == "Quiz"]['Event context']})
        print(quiz_data.to_dict())

        # creating quiz-table
        quiz_table = dash_table.DataTable(
        id='quiz_table',
        columns=[{"name": 'Completed', "id": 'Completed', 'presentation':'markdown'}
                for i in quiz_data.columns],
        data=quiz_data.to_dict('records'),
        style_cell={
                'textAlign':'left',
                'width': '{}%'.format(len(quiz_data.columns)),
                'textOverflow': 'ellipsis',
                'overflowY': 'auto',
                'whiteSpace': 'normal',
                'height': 'auto',
        },
        style_header=dict(backgroundColor="paleturquoise"),
        style_data=dict(backgroundColor="lavender"),
        style_table={
                'maxHeight': '100%',
                'maxWidth': 'width=550px',
                'overflowY': 'auto',
                'margin': '25px',
                },
        css=[{'selector': 'table', 'rule': 'table-layout: fixed'}],
        )
        #section for assignments
        assign_data = pd.DataFrame({'Completed':user_all_activities[user_all_activities['Component'] == "Assignment"]['Event context'], 'Uncompleted':unseen[unseen['Component'] == "Assignment"]['Event context']})
        assign_values = assign_data.values
        print(assign_values)
        i = assign_data.index
        for x, y in assign_values:
                print('x:' , x)
                print('y:' , y)
                if not isinstance(y, str):
                        print('ya')
        print(assign_data.to_dict())

        assign_table = dash_table.DataTable(
        id='assign_table',
        columns=[{"name": i, "id": i, "type": "text"}
                for i in assign_data.columns],
        data=assign_data.to_dict('records'),
        style_cell={
                'textAlign':'left',
                'width': '{}%'.format(len(assign_data.columns)),
                'textOverflow': 'ellipsis',
                'overflowY': 'auto',
                'whiteSpace': 'normal',
                'height': 'auto',
        },
        style_header=dict(backgroundColor="paleturquoise"),
        style_data=dict(backgroundColor="lavender"),
        style_table={
                'maxHeight': '100%',
                'maxWidth': 'width=550px',
                'overflowY': 'auto',
                'margin': '25px',
                },
        css=[{'selector': 'table', 'rule': 'table-layout: fixed'}],
        )

        # section for URL Data
        url_data = pd.DataFrame()
        url_data['Completed'] = user_all_activities[user_all_activities['Component'] == "URL"]['Event context']
        url_data['Uncompleted'] = unseen[unseen['Component'] == "URL"]['Event context']
        # print(url_data.to_dict())

        url_table = dash_table.DataTable(
        id='url_table',
        columns=[{"name": i, "id": i, 'presentation':'markdown'}
                for i in url_data.columns],
        data=url_data.to_dict('records'),
        style_cell={
                'textAlign':'left',
                'width': '{}%'.format(len(url_data.columns)),
                'textOverflow': 'ellipsis',
                'overflowY': 'auto',
                'whiteSpace': 'normal',
                'height': 'auto',
        },
        style_header=dict(backgroundColor="paleturquoise"),
        style_data=dict(backgroundColor="lavender"),
        style_table={
                'maxHeight': '100%',
                'maxWidth': 'width=550px',
                'overflowY': 'auto',
                'margin': '25px',
                },
        css=[{'selector': 'table', 'rule': 'table-layout: fixed'}],
        )

        #section for File Data
        file_data = pd.DataFrame()
        file_data['Completed'] = user_all_activities[user_all_activities['Component'] == "File"]['Event context']
        file_data['Uncompleted'] = unseen[unseen['Component'] == "File"]['Event context']
        print(file_data.to_dict())

        file_table = dash_table.DataTable(
        id='file_table',
        columns=[{"name": i, "id": i, 'presentation':'markdown'}
                for i in file_data.columns],
        data=file_data.to_dict('records'),
        style_cell={
                'textAlign':'left',
                'width': '{}%'.format(len(file_data.columns)),
                'textOverflow': 'ellipsis',
                'overflowY': 'auto',
                'whiteSpace': 'normal',
                'height': 'auto',
        },
        style_header=dict(backgroundColor="paleturquoise"),
        style_data=dict(backgroundColor="lavender"),
        style_table={
                'maxHeight': '100%',
                'maxWidth': 'width=550px',
                'overflowY': 'auto',
                'margin': '25px',
                },
        css=[{'selector': 'table', 'rule': 'table-layout: fixed'}],
        )



        fig5 = go.Figure(data=[go.Table(
        header=dict(values=['<b> Completed</b>', '<b>Not Completed</b>'],
                        fill_color='paleturquoise',
                        align='left'),
        cells=dict(values=[user_all_activities[user_all_activities['Component'] == "Assignment"]['Event context'],
                        unseen[unseen['Component'] == "Assignment"]['Event context']],
                fill_color='lavender',align='left'))

        ])
        fig5.update_layout(width=550, height=250, autosize=False, margin=dict(l=15, r=15, b=5, t=5))

        fig6 = go.Figure(data=[go.Table(
        header=dict(values=['<b> Seen</b>', '<b>Not Seen</b>'],
                        fill_color='paleturquoise',
                        align='left'),
        cells=dict(values=[user_all_activities[user_all_activities['Component'] == "URL"]['Event context'],
                        unseen[unseen['Component'] == "URL"]['Event context']],
                fill_color='lavender',
                align='left'))

        ])
        fig6.update_layout(width=550, height=250, autosize=False, margin=dict(l=15, r=25, b=5, t=5))
        fig7 = go.Figure(data=[go.Table(
        header=dict(values=['<b> Seen</b>', '<b>Not Seen</b>'],
                        fill_color='paleturquoise',
                        align='left'),
        cells=dict(values=[user_all_activities[user_all_activities['Component'] == "File"]['Event context'],
                        unseen[unseen['Component'] == "File"]['Event context']],
                fill_color='lavender',
                align='left'))

        ])
        fig7.update_layout(width=550, height=250, autosize=False, margin=dict(l=15, r=15, b=5, t=5))


        return dbc.Container([
        dbc.Row([
                dbc.Col([
                dbc.Row(children=[html.H3("Quiz",style={'margin-left':'15px'}),
                        dbc.Progress(label=quiz_perc, value=quiz_perc, max=100, striped=True, color="success",
                                style={'hight': '20px','margin-left' :'20px'}), html.Br()]),
                dbc.Row(children=[quiz_table], style={"height": "50vh"})
                ], width=5),
                dbc.Col([
                dbc.Row(children=[html.H3("Assignment",style={'margin-left':'15px'}),
                        dbc.Progress(label=assignment_perc, value=assignment_perc, max=100, striped=True,
                                        color="success", style={'hight': '20px','margin-left' :'20px'}), html.Br()]),
                dbc.Row(children=[assign_table], style={"height": "50vh"}),
                ])
        ]),
        dbc.Row([dbc.Col([html.H3("URL",style={'margin-left':'15px'}),
                        dbc.Progress(label=url_perc, value=url_perc, max=100, striped=True, color="success",
                                        style={'hight': '20px','margin-left' :'20px'}), html.Br(),
                        dcc.Graph(figure=fig6)], width=5, style={"height": "50vh"})
                        , dbc.Col([html.H3("File",style={'margin-left':'15px'}),
                        dbc.Progress(label=file_perc, value=file_perc, max=100, striped=True, color="success",
                                        style={'hight': '20px', 'margin-left': '20px'}), html.Br(),
                        dcc.Graph(figure=fig7)], width=5, style={"height": "50vh"})

        ])
        ])