import dash
from dash import html#, dcc
import dash_bootstrap_components as dbc
from group_services.planning_service import *
from dash.dependencies import Input, Output


dash.register_page(__name__,
                   path='/planning',
                   name='Planning',
                   title='Planning')


# Our data
data = operation()

# Done?
assignmentDone = "default"


# Layout
"""
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
                            html.P(assignment['intro'], className='card-text', style={'margin': '2rem'}),

                        ]
                    ), className=assignmentDone #className='done'
                    #className='done' if assignment['done'] else ''
                ),
                style={'marginBottom': '1rem'}

            ) for assignment in assignmentsToDisplay(1, data)
        ],
        style={'listStyle': 'none', 'padding': '0', 'marginBottom': '5rem'}
    )
])
"""
layout = html.Div(children=[
    html.H1(
        'Planning page',
        style={'marginBottom': '2rem'}
    ),
    html.H2('To do:'),
    html.Div(id="assignmentsDisplayed")
])
@dash.callback(
    Output('assignmentsDisplayed', 'children'),
    Input('userId', 'data'),
)
def fetch_data_on_user_select(user_id):

    if len(assignmentsToDisplay(user_id, data)) > 0:
        content = [
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
                                    html.P(assignment['intro'], className='card-text', style={'margin': '2rem'}),

                                ]
                            ), className=assignmentDone  # className='done'
                            # className='done' if assignment['done'] else ''
                        ),
                        style={'marginBottom': '1rem'}

                    ) for assignment in assignmentsToDisplay(user_id, data)
                ],
                style={'listStyle': 'none', 'padding': '0', 'marginBottom': '5rem'}
            )
        ]

    else:
        content = [html.P("There are no assignments due.")]

    return content

