import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__,
                   path='/',
                   name='Home',
                   title='Home')

layout = html.Div(children=[
    html.H1('Home page'),
    html.P('This is the homepage of the moodle analytics dashboard!'),
    dbc.Row([
        dbc.Col(dbc.Button(
            'User 1',
            type='button',
            value='user1',

        )),
        dbc.Col(dbc.Button('User 2')),
        dbc.Col(dbc.Button('User 3'))
    ])
])
