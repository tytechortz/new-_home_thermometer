from dash import Dash, html, dcc
import pandas as pd

url = "http://10.0.1.7:8080"

app = Dash(name=__name__, 
                title="Environmental Data Dashboard",
                assets_folder="static",
                assets_url_path="static")

application = app.server

app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    html.H1('Hello')

])

if __name__ == "__main__":
    app.run_server(port=8000, debug=True)