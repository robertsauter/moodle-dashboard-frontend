# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import dash
from dash import Dash, html
import dash_bootstrap_components as dbc
import pymysql
from sshtunnel import SSHTunnelForwarder
from lib.sql_to_json_converter import SQLToJSONConverter

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

tunnel = SSHTunnelForwarder(
    ('83.212.126.199', 22),
    ssh_username='user',
    ssh_password='Yz05ddnaTH',
    remote_bind_address=('127.0.0.1', 3306)
)
tunnel.start()

connection = pymysql.connect(
    host='127.0.0.1',
    user='moodledude',
    passwd='root',
    db='moodle',
    port=tunnel.local_bind_port
)

sql_cursor = connection.cursor()
sql_cursor.execute('SELECT * FROM mdl_quiz_grades')
result = sql_cursor.fetchall()

json_converter = SQLToJSONConverter()
json_data = json_converter.convert_to_json(result, sql_cursor)
print(json_data)

connection.close()

tunnel.close()

app.layout = html.Div([
    dbc.NavbarSimple(
        [
            dbc.NavLink(
                [
                    html.Div(page["name"], className="ms-2"),
                ],
                href=page["path"],
                active="exact",
            )
            for page in dash.page_registry.values()
        ],
        brand='Moodle analytics dashboard',
        fixed='top',
    ),
    dbc.Container(
        [
            dash.page_container
        ],
        style={
            'marginTop': '5rem'
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
