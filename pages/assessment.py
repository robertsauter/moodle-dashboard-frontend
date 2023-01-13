import dash
import requests
from dash import html, dcc
import plotly.graph_objects as go
import dash_bootstrap_components as dbc


dash.register_page(__name__,
                   path='/assessment',
                   name='Assessment',
                   title='Assessment')
#r = requests.get('http://localhost:5000/api/group/assessment')


# This is the JSON object, that you can use to display your visualizations :)
#data = r.json()


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
    html.H1('Assessment page', style={'marginBottom': '2rem'}),
    html.H2('Just a simple button, to show you how to use bootstrap components'),
    dbc.Button(
        "Click me, but I won't do anything!",
        color="primary",
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
