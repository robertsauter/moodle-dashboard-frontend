import dash
import pandas as pd
import requests
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from group_services.overall_progress_service import fetch_data

dash.register_page(__name__,
                   path='/overall_progress',
                   name='Overall progress',
                   title='Overall progress')
data = fetch_data()

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


layout = dbc.Container([
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

# Value for the progress bar
# progress = 50
# This is a python dict, that can be used to create a bar chart
"""dict_figure = {
    'data': [
        {
            'x': ['Assignment 1', 'Assignment 2', 'Assignment 3'],
            'y': [10, 1, 5],
            'type': 'bar',
            'name': 'Grades'
        }
    ],
    'layout': {
        'title': 'Assignment grades'
    }
}"""
# This is a plotly graph object to create the same bar chart
"""graph_object_figure = go.Figure(
    data=[go.Bar(x=['Assignment 1', 'Assignment 2', 'Assignment 3'], y=[10, 1, 5])],
    layout=go.Layout(
        title=go.layout.Title(text='Assignment grades')
    )
)"""


# This is the html layout, that is displayed on the page
# I found this progressbar component from bootstrap. Maybe it's helpful for you?
"""layout = html.Div(children=[
    html.H1(
        'Overall progress page',
        style={'marginBottom': '2rem'}
    ),
    html.H2('Just a simple progress bar from bootstrap'),
    dbc.Progress(
        value=progress,
        label=f'{progress}%',
        style={'marginBottom': '5rem'}
    ),
    html.H2('Simple chart from a python dict'),
    dcc.Graph(
        figure=dict_figure,
        style={'marginBottom': '5rem'}
    ),
    html.H2('Simple chart from a plotly graph object'),
    dcc.Graph(figure=graph_object_figure)
])"""
