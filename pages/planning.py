import json

import dash
import requests
from dash import html


r = requests.get('http://localhost:5000/api/group/planning')
data = r.json()


dash.register_page(__name__,
                   path='/planning',
                   name='Planning',
                   title='Planning')

layout = html.Div(children=[
    html.H1('Planning page'),
    html.Div(json.dumps(data))
])
