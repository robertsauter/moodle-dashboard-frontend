import dash
from dash import html
from dash.dependencies import Input, Output
from group_services.app_service import fetch_quiz_grades, do_something_with_user_id

dash.register_page(__name__,
                   path='/',
                   name='Home',
                   title='Home')

layout = html.Div(
    id='onLoad',
    children=[
        html.Div([
            html.H1('Moodle Dashboard'),
            html.P('This is the homepage of the moodle analytics dashboard!'),
        ]),
        html.Div(id='dataFetchedOnLoad'),
        html.Div(id='dataDependingOnUserId')
    ]
)


@dash.callback(
    Output('dataFetchedOnLoad', 'children'),
    Input('onLoad', 'children'),
)
def fetch_data_on_load(children):

    data = fetch_quiz_grades()

    content = [
        html.H1('Callback on load'),
        html.P('This is a callback, that gets triggered when the page loads. '
               'Use is to fetch data, for which you dont need the user id.'),
        html.P(f'Fetched data: {str(data)}')
    ]
    return content


@dash.callback(
    Output('dataDependingOnUserId', 'children'),
    Input('userSelect', 'value'),
)
def fetch_data_on_user_select(user_id):

    data = do_something_with_user_id(user_id)

    content = [
        html.H1('Callback depending on user id'),
        html.P('This is a callback, that gets triggered every time a user id gets selected. '
               'Use is to fetch data, that depends on the user id. '
               f'The id of the currently selected user is: {user_id}'),
        html.P(f'Fetched data: {str(data)}')
    ]
    return content
