from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import requests

import pandas as pd

url = "http://10.0.1.7:8080"

app = Dash(name=__name__, 
                title="Environmental Data Dashboard",
                assets_folder="static",
                assets_url_path="static")

application = app.server

app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    html.Div([
        html.Div([
            html.Div(id='live-thermometer', style={'color':'green', 'font-size': 40, 'font-family':'sans-serif'})
        ],
            className='four columns'
        ),
    ],
        className='row'
    ),
    dcc.Interval(
                    id='interval-component',
                    interval=60000,
                    n_intervals=0
                ),
])

@app.callback(Output('live-thermometer', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout(n):
    res = requests.get(url)
    data = res.json()
    f = ((9.0/5.0) * data) + 32
    return 'Current Temperature: {:.1f}'.format(f)

if __name__ == "__main__":
    app.run_server(port=8000, debug=True)