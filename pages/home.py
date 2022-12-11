import dash
from dash import html

dash.register_page(__name__,
                   path='/',
                   name='Home',
                   title='Home')

layout = html.Div(children=[
    html.H1(children='Home page')
])
