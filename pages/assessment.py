import json

import dash
import requests
from dash import html


r = requests.get('http://localhost:5000/api/group/assessment')
data = r.json()


dash.register_page(__name__,
                   path='/assessment',
                   name='Assessment',
                   title='Assessment')

layout = html.Div(children=[
    html.H1(children='Assessment page'),
    html.Div(children=json.dumps(data))
])
