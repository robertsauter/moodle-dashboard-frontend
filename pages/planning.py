
import dash
import requests
from dash import html#, dcc
#import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import datetime
import calendar
from group_services.planning_service import operation
import re

dash.register_page(__name__,
                   path='/planning',
                   name='Planning',
                   title='Planning')

# This is the JSON object, that you can use to display your visualizations :)
data = operation()

# HTML Cleaner to remove tags
CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
def cleanhtml(raw_html):
  cleantext = re.sub(CLEANR, '', raw_html)
  return cleantext

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

  deadlineStr = "due " + weekdayAbbr + ", " + str(duedate_day) + " " + monthAbbr[duedate_month] + " " + str(duedate_year)
  return deadlineStr


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
                            html.Img(src='assets/check2-circle.svg',
                                     style={'position': 'absolute', 'top': '2rem', 'right': '2rem'}),
                            html.H5(deadline(assignment['duedate']), className='deadline duedate'),
                            html.P(cleanhtml(assignment['intro']), className='card-text', style={'margin': '2rem'}),

                        ]
                    ), className='done'
                    #className='done' if assignment['done'] else ''
                ),
                style={'marginBottom': '1rem'}

            ) for assignment in data["result_assign"]
        ],
        style={'listStyle': 'none', 'padding': '0', 'marginBottom': '5rem'}
    )
])