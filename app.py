from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import requests
import time
from datetime import datetime as dt

import pandas as pd

url = "http://10.0.1.7:8080"


# print(today)

app = Dash(name=__name__, 
                title="Environmental Data Dashboard",
                assets_folder="static",
                assets_url_path="static")

application = app.server

app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    html.Div([
        html.Div([
            html.Div([
                html.Div(id='live-thermometer', style={'color':'green', 'font-size': 30, 'font-family':'sans-serif'}),
                html.H6('Today', style={'color':'white', 'text-align':'center'}),
            ],
                className='row'
            ),
            html.Div([
                html.Div([
                   html.Div(id='daily-high', style={'color':'red', 'text-align':'center'}), 
                ],
                    className='six columns'
                ),
                html.Div([
                   html.Div(id='daily-low', style={'color':'dodger-blue', 'text-align':'center'}), 
                ],
                    className='six columns'
                ),
            ],
                className='row'
            ),
            html.Div([
                html.H6('Ranks', style={'color':'white', 'text-align':'center'}),
            ],
                className='row'
            ),
            html.Div([
                html.Div([
                   html.Div(id='daily-high-high-rank', style={'color':'red', 'text-align':'center'}), 
                ],
                    className='six columns'
                ),
                html.Div([
                   html.Div(id='daily-low-low-rank', style={'color':'dodger-blue', 'text-align':'center'}), 
                ],
                    className='six columns'
                ),
            ],
                className='row'
            ),
            html.Div([
                html.Div([
                   html.Div(id='daily-high-low-rank', style={'color':'red', 'text-align':'center'}), 
                ],
                    className='six columns'
                ),
                html.Div([
                   html.Div(id='daily-low-high-rank', style={'color':'dodger-blue', 'text-align':'center'}), 
                ],
                    className='six columns'
                ),
            ],
                className='row'
            ),
            html.Div([
                html.H6('Monthly Rank', style={'color':'white', 'text-align':'center'}),
            ],
                className='row'
            ),
            html.Div([
                html.Div([
                   html.Div(id='monthly-high-high-rank', style={'color':'red', 'text-align':'center'}), 
                ],
                    className='six columns'
                ),
                html.Div([
                   html.Div(id='monthly-low-low-rank', style={'color':'dodger-blue', 'text-align':'center'}), 
                ],
                    className='six columns'
                ),
            ],
                className='row'
            ),
            html.Div([
                html.Div([
                   html.Div(id='monthly-high-low-rank', style={'color':'red', 'text-align':'center'}), 
                ],
                    className='six columns'
                ),
                html.Div([
                   html.Div(id='monthly-low-high-rank', style={'color':'dodger-blue', 'text-align':'center'}), 
                ],
                    className='six columns'
                ),
            ],
                className='row'
            ),
            html.Div([
                html.H6('90 Degree Days', style={'color':'white', 'text-align':'center'}),
            ],
                className='row'
            ),
            html.Div([
                html.Div(id='ninety-days', style={'color':'white', 'text-align':'center'}),
            ],
                className='row'
            ),
        ],
            className='four columns'
        ),
        html.Div([
            dcc.Graph(id='live-graph'),
        ],
            className='eight columns'
        ),
    ],
        className='row'
    ),
    html.Div([

    ],
        className='row'
    ),
    dcc.Interval(
        id='interval-component',
        interval=60000,
        n_intervals=0
    ),
    dcc.Interval(
        id='interval-component-graph',
        interval=900000,
        n_intervals=0
    ),
    dcc.Store(id='raw-data', storage_type='memory'),
    dcc.Store(id='daily-data', storage_type='memory'),
    dcc.Store(id='y2018', storage_type='session'),
    dcc.Store(id='y2019', storage_type='session'),
    dcc.Store(id='y2020', storage_type='session'),
    dcc.Store(id='y2021', storage_type='session'),
    dcc.Store(id='y2022', storage_type='session'),
])

@app.callback(
    Output('ninety-days', 'children'),
    [Input('interval-component', 'n_intervals'),
    Input('raw-data', 'data')])
def update_graph(n, raw_data):  
    df = pd.read_json(raw_data)
    df['datetime'] = pd.to_datetime(df[0])
    df = df.set_index('datetime')

    highs = df.resample('D').max()
    df90 = highs.loc[highs[1] >= 90]
    df95 = highs.loc[highs[1] >= 95]
    df100 = highs.loc[highs[1] >= 100]

    ndds = df90.groupby(df90.index.year).count()
    nfdds = df95.groupby(df95.index.year).count()
    hdds = df100.groupby(df100.index.year).count()
    # print(nfdds, hdds)
    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also

    #     print(df90, df95, nfdds)
    # df22dh = df22.resample('D').max()
    
    
    return(print(ndds))

@app.callback([
    Output('monthly-high-high-rank', 'children'),
    Output('monthly-high-low-rank', 'children'),
    Output('monthly-low-high-rank', 'children'),
    Output('monthly-low-low-rank', 'children')],
    [Input('interval-component-graph', 'n_intervals'),
    Input('raw-data', 'data')])
def update_daily_stats(n, data):
    today = time.strftime("%Y-%m-%d")
    df = pd.read_json(data)
    df_s = df
    df_s['date'] = pd.to_datetime(df_s[0])
    df_s = df_s.set_index('date')
    current_month = dt.now().month
    print(current_month)
    
    daily_highs = df_s.resample('D').max()
    df1 = daily_highs[daily_highs.index.month == current_month]
    print(df1)
    # print(daily_highs)



    total_days = len(daily_highs)
    print(total_days)
    daily_high = daily_highs.groupby([daily_highs.index.month, daily_highs.index.day]).idxmax()
    highest_daily_highs = daily_highs.sort_values(1, ascending=False)
    lowest_daily_highs = daily_highs.sort_values(1, ascending=True)
    high_high_rank = highest_daily_highs.index.get_loc(today)+1
    low_high_rank = lowest_daily_highs.index.get_loc(today)+1
        
    daily_lows = df_s.resample('D').min()
    daily_low = daily_lows.groupby([daily_lows.index.month, daily_lows.index.day]).idxmin()
    highest_daily_lows = daily_lows.sort_values(1, ascending=True)
    lowest_daily_lows = daily_lows.sort_values(1, ascending=False)
    # print(lowest_daily_lows.head(30))
    low_low_rank = highest_daily_lows.index.get_loc(today)+1
    high_low_rank = lowest_daily_lows.index.get_loc(today)+1




    return html.H6('HH-{}'.format(high_high_rank[0])), html.H6('HL-{}'.format(high_low_rank[0])), html.H6('LH-{}'.format(low_high_rank[0])), html.H6('LL-{}'.format(low_low_rank[0]))

@app.callback([
    Output('daily-high-high-rank', 'children'),
    Output('daily-high-low-rank', 'children'),
    Output('daily-low-high-rank', 'children'),
    Output('daily-low-low-rank', 'children')],
    [Input('interval-component-graph', 'n_intervals'),
    Input('raw-data', 'data')])
def update_daily_stats(n, data):
    today = time.strftime("%Y-%m-%d")
    df = pd.read_json(data)
    df_s = df
    df_s['date'] = pd.to_datetime(df_s[0])
    df_s = df_s.set_index('date')
    
    daily_highs = df_s.resample('D').max()



    total_days = len(daily_highs)
    print(total_days)
    daily_high = daily_highs.groupby([daily_highs.index.month, daily_highs.index.day]).idxmax()
    highest_daily_highs = daily_highs.sort_values(1, ascending=False)
    lowest_daily_highs = daily_highs.sort_values(1, ascending=True)
    high_high_rank = highest_daily_highs.index.get_loc(today)+1
    low_high_rank = lowest_daily_highs.index.get_loc(today)+1
        
    daily_lows = df_s.resample('D').min()
    daily_low = daily_lows.groupby([daily_lows.index.month, daily_lows.index.day]).idxmin()
    highest_daily_lows = daily_lows.sort_values(1, ascending=True)
    lowest_daily_lows = daily_lows.sort_values(1, ascending=False)
    # print(lowest_daily_lows.head(30))
    low_low_rank = highest_daily_lows.index.get_loc(today)+1
    high_low_rank = lowest_daily_lows.index.get_loc(today)+1




    return html.H6('HH-{}'.format(high_high_rank[0])), html.H6('HL-{}'.format(high_low_rank[0])), html.H6('LH-{}'.format(low_high_rank[0])), html.H6('LL-{}'.format(low_low_rank[0]))



@app.callback([
    Output('daily-high', 'children'),
    Output('daily-low', 'children')],
    [Input('interval-component-graph', 'n_intervals'),
    Input('daily-data', 'data')])
def update_daily_stats(n, daily_data):
    daily_df = pd.read_json(daily_data)
    daily_max = daily_df[1].max()
    daily_min = daily_df[1].min()

    return html.H6('High: {:.1f}'.format(daily_max)), html.H6('Low: {:.1f}'.format(daily_min))

@app.callback(Output('live-thermometer', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout(n):
    res = requests.get(url)
    data = res.json()
    f = ((9.0/5.0) * data) + 32
    return 'Current Temperature: {:.1f}'.format(f)

@app.callback(Output('raw-data', 'data'),
              [Input('interval-component', 'n_intervals')])
def update_layout(n):
    df = pd.read_csv('../../tempjan19.csv', header=None)
    
    return df.to_json()

@app.callback([
    Output('daily-data', 'data'),
    Output('y2018', 'data'),
    Output('y2019', 'data'),
    Output('y2020', 'data'),
    Output('y2021', 'data'),
    Output('y2022', 'data')],
    [Input('interval-component-graph', 'n_intervals'),
    Input('raw-data', 'data')])
def process_df_daily(n, data):
    df = pd.read_json(data)

    df_stats = df
    df_stats['datetime'] = pd.to_datetime(df_stats[0])
    df_stats = df_stats.set_index('datetime')
    today = time.strftime("%m-%d")

    td = dt.now().day
    tm = dt.now().month
    ty = dt.now().year
    ly = ty-1
    # print(ly)

    dfd = df_stats[df_stats.index.day == td]
    dfdm = dfd[dfd.index.month == tm]
    dfdmy = dfdm[dfdm.index.year == ty]
    # print(dfdmy)

    dfly = dfdm[dfdm.index.year == ly]
    df2018 = dfdm[dfdm.index.year == 2018]
    df2019 = dfdm[dfdm.index.year == 2019]
    df2020 = dfdm[dfdm.index.year == 2020]
    df2021 = dfdm[dfdm.index.year == 2021]
    df2022 = dfdm[dfdm.index.year == 2022]
    # print(df2022)

    record_high_temps = df_stats.groupby(df_stats.index.strftime('%m-%d')).max()
    # print(record_high_temps)
    record_highs = df_stats.resample('D').max()
    daily_highs = record_highs.groupby([record_highs.index.month, record_highs.index.day]).max()
    low_daily_highs = record_highs.groupby([record_highs.index.month, record_highs.index.day]).min()
    low_daily_highs_date = record_highs.groupby([record_highs.index.month, record_highs.index.day]).idxmin()
    daily_highs_date = record_highs.groupby([record_highs.index.month, record_highs.index.day]).idxmax()

    rec_high_date = daily_highs_date.loc[(tm,td), 1].year

    rec_low_high = low_daily_highs.loc[(tm,td), 1]
    rec_low_high_date = low_daily_highs_date.loc[(tm,td), 1].year

    record_low_temps = df_stats.groupby(df_stats.index.strftime('%m-%d')).min()
    record_lows = df_stats.resample('D').min()
    daily_lows = record_lows.groupby([record_lows.index.month, record_lows.index.day]).min()
    high_daily_lows = record_lows.groupby([record_lows.index.month, record_lows.index.day]).max()
    high_daily_lows_date = record_lows.groupby([record_lows.index.month, record_lows.index.day]).idxmax()
    daily_lows_date = record_lows.groupby([record_lows.index.month, record_lows.index.day]).idxmin()
    rec_low_date = daily_lows_date.loc[(tm,td), 1].year
    rec_high_low = high_daily_lows.loc[(tm,td), 1]
    rec_high_low_date = high_daily_lows_date.loc[(tm,td), 1].year

    months = {1:31, 2:31, 3:28, 4:31, 5:30, 6:31, 7:30, 8:31, 9:31, 10:30, 11:31, 12:30}
    months_ly = {1:31, 2:31, 3:29, 4:31, 5:30, 6:31, 7:30, 8:31, 9:31, 10:30, 11:31, 12:30}

    if td > 1:
        df_yest = df_stats[(df_stats.index.day == td-1) & (df_stats.index.month == tm) & (df_stats.index.year == ty)]
    elif td == 1:
        df_yest = df_stats[(df_stats.index.day == months.get(tm)) & (df_stats.index.month == tm-1) & (df_stats.index.year == ty)]

    return (dfdmy.to_json(), df2018.to_json(), df2019.to_json(), df2020.to_json(), df2021.to_json(), df2022.to_json())




@app.callback(
    Output('live-graph', 'figure'),
    [Input('interval-component', 'n_intervals'),
    Input('daily-data', 'data'),
    Input('y2018', 'data'),
    Input('y2019', 'data'),
    Input('y2020', 'data'),
    Input('y2021', 'data')])
def update_graph(n, daily_data, y2018, y2019, y2020, y2021):
    dfdmy = pd.read_json(daily_data)
    dfdmy['time'] = pd.to_datetime(dfdmy[0])
    dfdmy['time'] = dfdmy['time'].dt.strftime('%H:%M')
    # yest = pd.read_json(yest)
    # yest['time'] = pd.to_datetime(yest[0])
    # yest['time'] = yest['time'].dt.strftime('%H:%M')

    # dfly = pd.read_json(last_year)
    # dfly['time'] = pd.to_datetime(dfly[0])
    # dfly['time'] = dfly['time'].dt.strftime('%H:%M')

    df2018 = pd.read_json(y2018)
    df2018['time'] = pd.to_datetime(df2018[0])
    df2018['time'] = df2018['time'].dt.strftime('%H:%M')

    df2019 = pd.read_json(y2019)
    df2019['time'] = pd.to_datetime(df2019[0])
    df2019['time'] = df2019['time'].dt.strftime('%H:%M')

    df2020 = pd.read_json(y2020)
    df2020['time'] = pd.to_datetime(df2020[0])
    df2020['time'] = df2020['time'].dt.strftime('%H:%M')

    df2021 = pd.read_json(y2021)
    df2021['time'] = pd.to_datetime(df2021[0])
    df2021['time'] = df2021['time'].dt.strftime('%H:%M')

    # if selected_date == ''

    data = [
        # go.Scatter(
        #     x = yest['time'],
        #     y = yest[1],
        #     mode = 'markers+lines',
        #     marker = dict(
        #         color = 'black',
        #     ),
        #     name='yesterday'
        # ),
        go.Scatter(
            x = dfdmy['time'],
            y = dfdmy[1],
            mode = 'markers+lines',
            marker = dict(
                color = 'red',
            ),
            name='today'
        ),
        go.Scatter(
            x = df2018['time'],
            y = df2018[1],
            mode = 'markers+lines',
            marker = dict(
                color = 'orange',
            ),
            name='2018'
        ),
        go.Scatter(
            x = df2019['time'],
            y = df2019[1],
            mode = 'markers+lines',
            marker = dict(
                color = 'blue',
            ),
            name='2019'
        ),
        go.Scatter(
            x = df2020['time'],
            y = df2020[1],
            mode = 'markers+lines',
            marker = dict(
                color = 'turquoise',
            ),
            name='2020'
        ),
        go.Scatter(
            x = df2021['time'],
            y = df2021[1],
            mode = 'markers+lines',
            marker = dict(
                color = 'green',
            ),
            name='2021'
        ),
    ]
    layout = go.Layout(
        xaxis=dict(tickformat='%H%M'),
        height=500,
        paper_bgcolor="#1f2630",
        plot_bgcolor="#1f2630",
        font=dict(color="#2cfec1"),
    )
    return {'data': data, 'layout': layout}


if __name__ == "__main__":
    app.run_server(port=8000, debug=True)