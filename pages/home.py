import dash
from dash import html
from dash.dependencies import Input, Output
from group_services.app_service import fetch_quiz_grades, do_something_with_user_id

dash.register_page(__name__,
                   path='/',
                   name='Home',
                   title='Home')

# You can just fetch data in the layout file, if it does not depend on the user id.
data = fetch_quiz_grades()

layout = html.Div([
    html.Div([
        html.Br(),
        html.H1('Welcome to our Moodle Analytics Dashboard'),
        html.Img(src='/assets/Moodle-logo.png', className="ml-auto", style={'height':'auto', 'maxWidth':'550px', 'width':'100%'}),
        # html.P('This is the homepage of the moodle analytics dashboard!'),
    ]),
    # html.H1('Fetched data on load'),
    # html.P('This data is fetched every time the page is loaded. Just put the request before the layout.'),
    # html.P(f'Fetched data: {str(data)}'),
    # html.Div(id='dataDependingOnUserId')
])


@dash.callback(
    Output('dataDependingOnUserId', 'children'),
    Input('userId', 'data'),
)
def fetch_data_on_user_select(user_id):

    user_data = do_something_with_user_id(user_id)

    content = [
        html.H1('Callback depending on user id'),
        html.P('This is a callback, that gets triggered every time a user id gets selected. '
               'Use is to fetch data, that depends on the user id. '
               f'The id of the currently selected user is: {user_id}'),
        html.P(f'Fetched data: {str(user_data)}')
    ]
    return content
