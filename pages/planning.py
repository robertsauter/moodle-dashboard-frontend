import dash
from dash import html

dash.register_page(__name__,
                   path='/planning',
                   name='Planning',
                   title='Planning')

layout = html.Div(children=[
    html.H1(children='Planning page')
])
