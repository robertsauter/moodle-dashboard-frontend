# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import dash
from dash import Dash, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from group_services.app_service import fetch_users

app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)

app.layout = html.Div(
    id='onLoad',
    children=[
        dbc.NavbarSimple(
            [
                dbc.NavLink(
                    [
                        html.Div(page["name"], className='ms-2'),
                    ],
                    href=page["path"],
                    active='exact',
                )
                for page in dash.page_registry.values()
            ],
            brand='Moodle analytics dashboard',
            fixed='top',
        ),
        dbc.Container(
            [
                html.Div(id='userSelectWrapper'),
                dash.page_container,
            ],
            style={
                'marginTop': '5rem'
            },
        )
    ]
)


@dash.callback(
    Output('userSelectWrapper', 'children'),
    Input('onLoad', 'children'),
)
def get_users(children):
    users = fetch_users()
    content = dbc.Select(
        id='userSelect',
        options=[
            {'label': f'{user["firstname"]} {user["lastname"]}', 'value': user["id"]}
            for user in users
        ],
        value=1
    ),

    return content


if __name__ == '__main__':
    app.run_server(debug=True)
