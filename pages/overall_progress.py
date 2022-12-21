import dash
import requests
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go


dash.register_page(__name__,
                   path='/overall_progress',
                   name='Overall progress',
                   title='Overall progress')
r = requests.get('http://localhost:5000/api/group/overall_progress')


# This is the JSON object, that you can use to populate your visualizations with data :)
data = r.json()


# Value for the progress bar
progress = 50
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
# I found this progressbar component from bootstrap. Maybe it's helpful for you?
layout = html.Div(children=[
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
])
