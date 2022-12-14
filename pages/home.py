import dash
from dash import html

dash.register_page(__name__,
                   path='/',
                   name='Home',
                   title='Home')

layout = html.Div(children=[
    html.H1('Home page'),
    html.P('This is the homepage of ')
])
