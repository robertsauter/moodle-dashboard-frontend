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

eu = ['anonfirstname31 anonlastname31', 'anonfirstname62 anonlastname62', 'anonfirstname65 anonlastname65',
         'anonfirstname51 anonlastname51', 'anonfirstname66 anonlastname66', 'anonfirstname47 anonlastname47',
         'anonfirstname48 anonlastname48', 'anonfirstname68 anonlastname68', 'anonfirstname59 anonlastname59',
         'anonfirstname64 anonlastname64', 'anonfirstname67 anonlastname67', 'anonfirstname53 anonlastname53',
         'anonfirstname49 anonlastname49', 'anonfirstname55 anonlastname55', 'anonfirstname73 anonlastname73',
         'anonfirstname60 anonlastname60', 'anonfirstname57 anonlastname57', 'anonfirstname70 anonlastname70',
         'anonfirstname63 anonlastname63', 'anonfirstname54 anonlastname54', 'anonfirstname56 anonlastname56',
         'anonfirstname61 anonlastname61', 'anonfirstname69 anonlastname69', 'anonfirstname58 anonlastname58',
         'anonfirstname52 anonlastname52', 'anonfirstname71 anonlastname71', 'anonfirstname72 anonlastname72',
         'anonfirstname21 anonlastname21']
enrolled_users = [strValue.split(' ', 1)[0] for strValue in eu ]

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
            brand=html.Img(src='/assets/Moodle-Icon-1024-corners.png', className="ml-auto", style={'height':'50px', 'width':'50px'}), # orange icon
            #brand=html.Img(src='/assets/icon-moodle.png', className="ml-auto", style={'height':'50px', 'width':'95px'}), # blue icon
            fixed='top',
            style =  {'background': 'linear-gradient(0deg, #e15707 0, #f28224 100%)'},
            #style =  {'background': 'linear-gradient(0deg, #0971B5 0, #00AEEE 100%)'}, #blue theme
        ),
        dbc.Container(
            [
                dbc.Select(
                    id='userSelect',
                    options=[
                        {'label': f'{user["firstname"]} {user["lastname"]}', 'value': user["id"]}
                        for user in users if user["firstname"] in enrolled_users
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
    #print(user_id)
    return user_id



if __name__ == '__main__':
    app.run_server(debug=True)
