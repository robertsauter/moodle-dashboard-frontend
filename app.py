# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from group_services.app_service import fetch_users

app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)

users = fetch_users()

app.layout = html.Div(
    id='onLoad',
    children=[
        dcc.Store(id='userId', storage_type='local'),
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
            # html.Img(src='/assets/Moodle-Icon-1024-corners.png', className="ml-auto",
            # style={'height': '50px', 'width': '50px'}),  # orange icon
            # blue icon
            # brand=html.Img(src='/assets/icon-moodle.png', className="ml-auto",
            # style={'height':'50px', 'width':'95px'}),
            fixed='top',
            style={'background': 'linear-gradient(0deg, #e15707 0, #f28224 100%)'},
            # style =  {'background': 'linear-gradient(0deg, #0971B5 0, #00AEEE 100%)'}, #blue theme
        ),
        dbc.Container(
            [
                dbc.Select(
                    id='userSelect',
                    options=[
                        {'label': f'{user["firstname"]} {user["lastname"]}', 'value': user["id"]}
                        for user in users
                    ],
                    value=1
                ),
                dash.page_container,
            ],
            style={
                "margin-top": "6rem",
                "height": "100%",
                'border-radius': 20,
                "padding": "3rem 2rem",
                'background': 'white',
                'box-shadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
            },
        )

    ]
)


@dash.callback(
    Output('userId', 'data'),
    Input('userSelect', 'value'),
)
def set_user_id(user_id):
    return user_id


if __name__ == '__main__':
    app.run_server(debug=True)
