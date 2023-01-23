import dash
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from group_services.overall_progress_service import operation, fetch_data
import pandas as pd
from dash.dependencies import Input, Output

progress_data = operation()

dash.register_page(__name__,
                   path='/overall_progress',
                   name='Overall progress',
                   title='Overall progress')

layout = html.Div([
    dbc.Container(id='dataDependingOnUserIdOP')
])

@dash.callback(
    Output('dataDependingOnUserIdOP', 'children'),
    Input('userId', 'data'),
)
def fetch_selected_progress(user_id):

        # This is the JSON object, that you can use to populate your visualizations with data :)
        data = fetch_data(user_id, progress_data)

        # getting the dataframes from the json file
        user_all_activities = pd.read_json(data[0])
        unseen = pd.read_json(data[1])
        perc = pd.read_json(data[2])
        print("its the new fetch data")
        print(user_all_activities)

        # getting the percentages from the perc df
        quiz_perc = perc[0][0]
        assignment_perc = perc[0][1]
        url_perc = perc[0][2]
        file_perc = perc[0][3]

        quiz_data1 = pd.DataFrame(
                {'Completed': user_all_activities[user_all_activities['Component'] == "Quiz"]['Event context']})
        quiz_table1 = dash_table.DataTable(
                id='quiz_table1',
                columns=[{"name": i, "id": i, "type": "text", 'presentation': "markdown"}
                        for i in quiz_data1.columns],
                data=quiz_data1.to_dict('records'),
                style_cell={
                'textAlign': 'center',
                'width': '{}%'.format(len(quiz_data1.columns)),
                'textOverflow': 'ellipsis',
                'overflowY': 'auto',
                'whiteSpace': 'normal',
                'height': 'auto',
                },
                style_header=dict(backgroundColor="paleturquoise"),
                style_data=dict(backgroundColor="lavender"),
                style_table={
                'height': '200px',
                'maxHeight': '100%',
                'maxWidth': 'width=300px',
                'overflowY': 'auto',
                'margin': '25px',
                },
                css=[{'selector': 'table', 'rule': 'table-layout: fixed'}],
        )

        # zweite quiz data table (uncompleted quizes)

        quiz_data2 = pd.DataFrame({'Uncompleted': unseen[unseen['Component'] == "Quiz"]['Event context']})
        quiz_table2 = dash_table.DataTable(
                id='quiz_table2',
                columns=[{"name": i, "id": i, "type": "text", 'presentation': "markdown"}
                        for i in quiz_data2.columns],
                data=quiz_data2.to_dict('records'),
                style_cell={
                'textAlign': 'center',
                'width': '{}%'.format(len(quiz_data2.columns)),
                'textOverflow': 'ellipsis',
                'overflowY': 'auto',
                'whiteSpace': 'normal',
                'height': 'auto',
                },
                style_header=dict(backgroundColor="paleturquoise"),
                style_data=dict(backgroundColor="lavender"),
                style_table={'height': '200px',
                        'maxHeight': '100%',
                        'maxWidth': 'width=300px',
                        'overflowY': 'auto',
                        'margin': '25px',
                        },
                css=[{'selector': 'table', 'rule': 'table-layout: fixed'}],
        )

        assignment_data1 = pd.DataFrame(
                {'Completed': user_all_activities[user_all_activities['Component'] == "Assignment"]['Event context']})
        assign_table1 = dash_table.DataTable(
                id='assign_table1',
                columns=[{"name": i, "id": i, "type": "text", 'presentation': "markdown"}
                        for i in assignment_data1.columns],
                data=assignment_data1.to_dict('records'),
                style_cell={
                'textAlign': 'center',
                'width': '{}%'.format(len(quiz_data1.columns)),
                'textOverflow': 'ellipsis',
                'overflowY': 'auto',
                'whiteSpace': 'normal',
                'height': 'auto',
                },
                style_header=dict(backgroundColor="paleturquoise"),
                style_data=dict(backgroundColor="lavender"),
                style_table={'height': '200px',

                        'maxHeight': '100%',
                        'maxWidth': 'width=300px',
                        'overflowY': 'auto',
                        'margin': '25px',
                        },
                css=[{'selector': 'table', 'rule': 'table-layout: fixed'}],
        )

        #  second datatable (Uncompleted assignments)

        assignment_data2 = pd.DataFrame({'Uncompleted': unseen[unseen['Component'] == "Assignment"]['Event context']})
        assign_table2 = dash_table.DataTable(
                id='assign_table2',
                columns=[{"name": i, "id": i, "type": "text", 'presentation': "markdown"}
                        for i in assignment_data2.columns],
                data=assignment_data2.to_dict('records'),
                style_cell={
                'textAlign': 'center',
                'width': '{}%'.format(len(quiz_data2.columns)),
                'textOverflow': 'ellipsis',
                'overflowY': 'auto',
                'whiteSpace': 'normal',
                'height': 'auto',
                },
                style_header=dict(backgroundColor="paleturquoise"),
                style_data=dict(backgroundColor="lavender"),
                style_table={'height': '200px',
                        'maxHeight': '100%',
                        'maxWidth': 'width=300px',
                        'overflowY': 'auto',
                        'margin': '25px',
                        },
                css=[{'selector': 'table', 'rule': 'table-layout: fixed'}],
        )

        url_data1 = pd.DataFrame({'Seen': user_all_activities[user_all_activities['Component'] == "URL"]['Event context']})
        url_table1 = dash_table.DataTable(
                id='url_table1',
                columns=[{"name": i, "id": i, 'presentation': 'markdown', 'type': 'text'}
                        for i in url_data1.columns],
                data=url_data1.to_dict('records'),
                style_cell={
                'textAlign': 'center',
                'width': '{}%'.format(len(url_data1.columns)),
                'textOverflow': 'ellipsis',
                'overflowY': 'auto',
                'whiteSpace': 'normal',
                'height': 'auto',
                },
                style_header=dict(backgroundColor="paleturquoise"),
                style_data=dict(backgroundColor="lavender"),
                style_table={
                'height': '200px',
                'maxHeight': '100%',
                'maxWidth': 'width=550px',
                'overflowY': 'auto',
                'margin': '25px',
                },
                css=[{'selector': 'table', 'rule': 'table-layout: fixed'}]

        )
        # second url table(unseen)
        url_data2 = pd.DataFrame({'Unseen': unseen[unseen['Component'] == "URL"]['Event context']})
        url_table2 = dash_table.DataTable(
                id='url_table2',
                columns=[{"name": i, "id": i, 'presentation': 'markdown', 'type': 'text'}
                        for i in url_data2.columns],
                data=url_data2.to_dict('records'),
                style_cell={
                'textAlign': 'center',
                'width': '{}%'.format(len(url_data2.columns)),
                'textOverflow': 'ellipsis',
                'overflowY': 'auto',
                'whiteSpace': 'normal',
                'height': 'auto',
                },
                style_header=dict(backgroundColor="paleturquoise"),
                style_data=dict(backgroundColor="lavender"),
                style_table={
                'height': '200px',
                'maxHeight': '100%',
                'maxWidth': 'width=550px',
                'overflowY': 'auto',
                'margin': '25px',
                },
                css=[{'selector': 'table', 'rule': 'table-layout: fixed'}]

        )

        file_data1 = pd.DataFrame(
                {'Seen': user_all_activities[user_all_activities['Component'] == "File"]['Event context']})
        file_table1 = dash_table.DataTable(
                id='file_table1',
                columns=[{"name": i, "id": i, "type": "text", 'presentation': "markdown"}
                        for i in file_data1.columns],
                data=file_data1.to_dict('records'),
                style_cell={
                'textAlign': 'center',
                'width': '{}%'.format(len(quiz_data1.columns)),
                'textOverflow': 'ellipsis',
                'overflowY': 'auto',
                'whiteSpace': 'normal',
                'height': 'auto',
                },
                style_header=dict(backgroundColor="paleturquoise"),
                style_data=dict(backgroundColor="lavender"),
                style_table={'height': '200px',
                        'maxHeight': '100%',
                        'maxWidth': 'width=300px',
                        'overflowY': 'auto',
                        'margin': '25px',
                        },
                css=[{'selector': 'table', 'rule': 'table-layout: fixed'}],
        )

        # second file datatable (unseen)

        file_data2 = pd.DataFrame({'Unseen': unseen[unseen['Component'] == "File"]['Event context']})
        file_table2 = dash_table.DataTable(
                id='file_table2',
                columns=[{"name": i, "id": i, "type": "text", 'presentation': "markdown"}
                        for i in file_data2.columns],
                data=file_data2.to_dict('records'),
                style_cell={
                'textAlign': 'center',
                'width': '{}%'.format(len(quiz_data2.columns)),
                'textOverflow': 'ellipsis',
                'overflowY': 'auto',
                'whiteSpace': 'normal',
                'height': 'auto',
                },
                style_header=dict(backgroundColor="paleturquoise"),
                style_data=dict(backgroundColor="lavender"),
                style_table={'height': '200px',
                        'maxHeight': '100%',
                        'maxWidth': 'width=300px',
                        'overflowY': 'auto',
                        'margin': '25px',
                        },
                css=[{'selector': 'table', 'rule': 'table-layout: fixed'}],
        )
        return dbc.Container([
        dbc.Row([dbc.Col([html.H3("Quiz",style={'margin-top':'30px','margin-left':'15px'}),
                        dbc.Progress(label=quiz_perc, value=quiz_perc, max=100, striped=True, color="success",
                                style={'height': '20px','margin-left' :'20px','margin-down':'30px'}),
                        dbc.Row(children=[quiz_table1,quiz_table2], style={"height": "65vh"}),html.Br(),html.Br()],width=6),
                dbc.Col([html.H3("Assignment",style={'margin-top':'30px','margin-left':'15px'}),
                        dbc.Progress(label=assignment_perc, value=assignment_perc, max=100, striped=True,
                                        color="success", style={'height': '20px','margin-left' :'20px','margin-down':'30px'}),
                dbc.Row(children=[assign_table1,assign_table2], style={"height": "65vh"}),html.Br(),html.Br()],width=6),
        dbc.Row([dbc.Col([html.H3("URL",style={'margin-left':'15px','margin-top':'30px'}),
                        dbc.Progress(label=url_perc, value=url_perc, max=100, striped=True, color="success",
                                        style={'height': '20px','margin-left' :'20px','margin-down':'30px'}),
                        dbc.Row(children=[url_table1,url_table2], style={"height": "65vh"})],width=6)
                ,dbc.Col([html.H3("File",style={'margin-left':'15px','margin-top':'30px'}),
                        dbc.Progress(label=file_perc, value=file_perc, max=100, striped=True, color="success",
                                        style={'height': '20px', 'margin-left': '20px','margin-down':'30px'}),
                        dbc.Row(children=[file_table1,file_table2], style={"height": "65vh"})],width=6)
                ])])])

