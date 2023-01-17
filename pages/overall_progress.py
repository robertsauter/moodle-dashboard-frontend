import dash
import requests
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from group_services.overall_progress_service import fetch_grades
import pandas as pd

dash.register_page(__name__,
                   path='/overall_progress',
                   name='Overall progress',
                   title='Overall progress')
#r = requests.get('http://localhost:5000/api/group/overall_progress')

grades = fetch_grades()
data = grades
# This is the JSON object, that you can use to populate your visualizations with data :)
#data = grades.json()

user_all_activities = pd.read_json(data[0])
unseen = pd.read_json(data[1])
perc = pd.read_json(data[2])
# print(user_all_activities)

# getting the percentages from the perc df
quiz_perc = perc[0][0]
assignment_perc = perc[0][1]
url_perc = perc[0][2]
file_perc = perc[0][3]

fig4 = go.Figure(data=[go.Table(
            header=dict(values=['<b> Completed</b>', '<b>Not Completed</b>'],
                        fill_color='paleturquoise',
                        align='left'),
            cells=dict(values=[user_all_activities[user_all_activities['Component'] == "Quiz"]['Event context'],
                                unseen[unseen['Component'] == "Quiz"]['Event context']],
                        fill_color='lavender',
                        align='left'))

                                    ])
fig4.update_layout(width=550, height=250, autosize=False, margin=dict(l=10, r=25, b=5, t=5))

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
            dbc.Col([html.H3("Quiz",style={'margin-left':'15px'}),
                    dbc.Progress(label=quiz_perc, value=quiz_perc, max=100, striped=True, color="success",
                                style={'hight': '20px','margin-left' :'20px'}), html.Br(),
                    dcc.Graph(figure=fig4)], width=5, style={"height": "50vh"})
            , dbc.Col([html.H3("Assignment",style={'margin-left':'15px'}),
                    dbc.Progress(label=assignment_perc, value=assignment_perc, max=100, striped=True,
                                    color="success", style={'hight': '20px','margin-left' :'20px'}), html.Br(),
                    dcc.Graph(figure=fig5)], width=5, style={"height": "50vh"})], justify='left'),
        dbc.Row([dbc.Col([html.H3("URL",style={'margin-left':'15px'}),
                        dbc.Progress(label=url_perc, value=url_perc, max=100, striped=True, color="success",
                                    style={'hight': '20px','margin-left' :'20px'}), html.Br(),
                        dcc.Graph(figure=fig6)], width=5, style={"height": "50vh"})
                    , dbc.Col([html.H3("File",style={'margin-left':'15px'}),
                            dbc.Progress(label=file_perc, value=file_perc, max=100, striped=True,
                                            color="success", style={'hight': '20px','margin-left' :'20px'}), html.Br(),
                            dcc.Graph(figure=fig7)], width=5, style={"height": "50vh"})], justify='left')
                                    ])

# # Value for the progress bar
# progress = 50
# # This is a python dict, that can be used to create a bar chart
# dict_figure = {
#     'data': [
#         {
#             'x': ['Assignment 1', 'Assignment 2', 'Assignment 3'],
#             'y': [10, 1, 5],
#             'type': 'bar',
#             'name': 'Grades'
#         }
#     ],
#     'layout': {
#         'title': 'Assignment grades'
#     }
# }
# # This is a plotly graph object to create the same bar chart
# graph_object_figure = go.Figure(
#     data=[go.Bar(x=['Assignment 1', 'Assignment 2', 'Assignment 3'], y=[10, 1, 5])],
#     layout=go.Layout(
#         title=go.layout.Title(text='Assignment grades')
#     )
# )


# # This is the html layout, that is displayed on the page
# # I found this progressbar component from bootstrap. Maybe it's helpful for you?
# layout = html.Div(children=[
#     html.H1(
#         'Overall progress page',
#         style={'marginBottom': '2rem'}
#     ),
#     html.H2('Just a simple progress bar from bootstrap'),
#     dbc.Progress(
#         value=progress,
#         label=f'{progress}%',
#         style={'marginBottom': '5rem'}
#     ),
#     html.H2('Simple chart from a python dict'),
#     dcc.Graph(
#         figure=dict_figure,
#         style={'marginBottom': '5rem'}
#     ),
#     html.H2('Simple chart from a plotly graph object'),
#     dcc.Graph(figure=graph_object_figure)
# ])