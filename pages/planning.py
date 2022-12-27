import dash
import requests
from dash import html, dcc
import plotly.graph_objects as go
import dash_bootstrap_components as dbc


dash.register_page(__name__,
                   path='/planning',
                   name='Planning',
                   title='Planning')
r = requests.get('http://localhost:5000/api/group/planning')


# This is the JSON object, that you can use to display your visualizations :)
data = r.json()


# This is a dummy list of assignments, that we can iterate over to display on the page
assignments = [
    {'title': 'Assigment 1', 'desc': 'Blablabla', 'done': True},
    {'title': 'Assigment 2', 'desc': 'Blablabla', 'done': True},
    {'title': 'Assigment 3', 'desc': 'Blablabla', 'done': False},
    {'title': 'Assigment 4', 'desc': 'Blablabla', 'done': False},
    {'title': 'Assigment 5', 'desc': 'Blablabla', 'done': False}
]
# This is a python dict, that can be used to create a bar chart
dict_figure = {
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
}
# This is a plotly graph object to create the same bar chart
graph_object_figure = go.Figure(
    data=[go.Bar(x=['Assignment 1', 'Assignment 2', 'Assignment 3'], y=[10, 1, 5])],
    layout=go.Layout(
        title=go.layout.Title(text='Assignment grades')
    )
)


# This is the html layout, that is displayed on the page
layout = html.Div(children=[
    html.H1(
        'Planning page',
        style={'marginBottom': '2rem'}
    ),
    html.H2('This is a list of items, to show you how to iterate and use bootstrap components'),
    html.Ul(
        [
            html.Li(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H4(assignment['title'], className='card-title'),
                            html.P(assignment['desc'], className='card-text')
                        ]
                    ),
                    className='done' if assignment['done'] else ''
                ),
                style={'marginBottom': '1rem'}
            ) for assignment in assignments
        ],
        style={'listStyle': 'none', 'padding': '0', 'marginBottom': '5rem'}
    ),
    html.H2('Simple chart from a python dict'),
    dcc.Graph(
        figure=dict_figure,
        style={'marginBottom': '5rem'}
    ),
    html.H2('Simple chart from a plotly graph object'),
    dcc.Graph(figure=graph_object_figure)
])
