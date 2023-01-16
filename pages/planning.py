import dash
import requests
from dash import html#, dcc
#import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import datetime
import calendar


dash.register_page(__name__,
                   path='/planning',
                   name='Planning',
                   title='Planning')
r = requests.get('http://localhost:5000/api/group/planning')


# This is the JSON object, that you can use to display your visualizations :)
data = r.json()

# Calendar Arrays
dayNames = [x for x in calendar.day_name]
dayAbbr = [y for y in calendar.day_abbr]
monthNames = [z for z in calendar.month_name]
monthAbbr = [w for w in calendar.month_abbr]


# Def
def deadline(duedate_epoch):
  duedate_full = str(datetime.datetime.fromtimestamp(duedate_epoch))
  duedate_year = int(duedate_full[0:4])
  duedate_month = int(duedate_full[5:7])
  duedate_day = int(duedate_full[8:10])

  weekdayNumber = calendar.weekday(duedate_year, duedate_month, duedate_day)
  weekdayAbbr = dayAbbr[weekdayNumber]

  deadlineStr = "due" + weekdayAbbr + ", " + str(duedate_day) + " " + monthAbbr[duedate_month] + " " + str(duedate_year)
  return deadlineStr


# This is a dummy list of assignments, that we can iterate over to display on the page
"""assignments = [
    {'title': 'Assigment 1', 'desc': 'Blablabla', 'done': True},
    {'title': 'Assigment 2', 'desc': 'Blablabla', 'done': True},
    {'title': 'Assigment 3', 'desc': 'Blablabla', 'done': False},
    {'title': 'Assigment 4', 'desc': 'Blablabla', 'done': False},
    {'title': 'Assigment 5', 'desc': 'Blablabla', 'done': False}
]"""
# This is a python dict, that can be used to create a bar chart
"""dict_figure = {
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
"""

# This is the html layout, that is displayed on the page
layout = html.Div(children=[
    html.H1(
        'Planning page',
        style={'marginBottom': '2rem'}
    ),
    html.H2('To do:'),
    html.Ul(
        [
            html.Li(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H4(assignment['name'], className='card-title'),
                            html.H5(deadline(assignment['duedate']), className='deadline'),
                            html.P(assignment['intro'], className='card-text')
                        ]
                    ),
                    #className='done' if assignment['done'] else ''
                ),
                style={'marginBottom': '1rem'}

            ) for assignment in data["result_assign"]
        ],
        style={'listStyle': 'none', 'padding': '0', 'marginBottom': '5rem'}
    ),
    """
    html.H2('Simple chart from a python dict'),
    dcc.Graph(
        figure=dict_figure,
        style={'marginBottom': '5rem'}
    ),
    html.H2('Simple chart from a plotly graph object'),
    dcc.Graph(figure=graph_object_figure)
"""
])