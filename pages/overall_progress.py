import json

import dash
import requests
from dash import html


r = requests.get('http://localhost:5000/api/group/overall_progress')
data = r.json()


dash.register_page(__name__,
                   path='/overall_progress',
                   name='Overall progress',
                   title='Overall progress')

layout = html.Div(children=[
    html.H1('Overall progress page'),
    html.Div(json.dumps(data))
])
