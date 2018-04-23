# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import time
from datetime import datetime
import plotly.graph_objs as go


'''
https://plot.ly/pandas/dashboard/
'''
#--FUNCTIONS--##
def get_data():
    return pd.read_csv('data.csv')


#--TODOS--##
'''
#BETER SCHEDULER
https://community.plot.ly/t/solved-updating-server-side-app-data-on-a-schedule/6612/2
https://github.com/agronholm/apscheduler/tree/master/examples/?at=master
#CLICK MAPS TO SELECT COUNTRIES
https://plot.ly/python/choropleth-maps/
#Download Link
https://community.plot.ly/t/download-raw-data/4700/8

'''



#--APP--##
app = dash.Dash(__name__)


df=get_data()

dic={'current_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
         'last_data_date':df['DATE'].max()}
options=[
    {'label': 'TOTAL USERS', 'value': 'TOTAL_USERS'},
    {'label': 'UURS', 'value': 'UURS'}
]

value=['TOTAL_USERS', 'UURS']
hoverData={'points': [{'x': dic['last_data_date']}]}

app.layout= html.Div(children=[
                html.H1(children='Users Under Risk'),

                html.Div(children='''
                    Last Updated {current_time} Last Data Date {last_data_date}.
                '''.format(**dic)),
                html.Div(children=' '),


                html.Div(dcc.Input(id='input-box', type='text'),style={'display': 'inline-block', 'width': '20%'}),
                html.Div(dcc.Input(id='input-box', type='text'),style={'display': 'inline-block', 'width': '20%'}),
                html.Div(dcc.Input(id='input-box', type='text'),style={'display': 'inline-block', 'width': '20%'}),
                html.Button('Update', id='button'),
                html.Div(id='output-container-button', children='Account Money Minimum'),


                html.Div([dcc.Dropdown(id='dropdown-definition1', options=options, value=value, multi=True)],style={'display': 'inline-block', 'width': '34%'}),
                html.Div([dcc.Dropdown(id='dropdown-definition2', options=options, value=value, multi=True)],style={'display': 'inline-block', 'width': '33%'}),
                html.Div([dcc.Dropdown(id='dropdown-definition3', options=options, value=value, multi=True)],style={'display': 'inline-block', 'width': '33%'}),


                html.Div([dcc.Graph(id='map-select')],style={'display': 'inline-block', 'width': '25%'}),

                html.Div([
                        dcc.Dropdown(id='dropdown-time-series', options=options, value=value, multi=True),
                        dcc.Graph(id='time-series-graph', hoverData=hoverData)
                        ],style={'display': 'inline-block', 'width': '75%'}),

                html.Div([dcc.Dropdown(id='dropdown-pie-graph1', options=options, value=value, multi=True)],style={'display': 'inline-block', 'width': '25%'}),
                html.Div([dcc.Dropdown(id='dropdown-pie-graph2', options=options, value=value, multi=True)],style={'display': 'inline-block', 'width': '25%'}),
                html.Div([dcc.Dropdown(id='dropdown-pie-graph3', options=options, value=value, multi=True)],style={'display': 'inline-block', 'width': '25%'}),
                html.Div([dcc.Dropdown(id='dropdown-pie-graph4', options=options, value=value, multi=True)],style={'display': 'inline-block', 'width': '25%'}),

                html.Div([dcc.Graph(id='pie-graph1')],style={'display': 'inline-block', 'width': '25%'}),
                html.Div([dcc.Graph(id='pie-graph2')],style={'display': 'inline-block', 'width': '25%'}),
                html.Div([dcc.Graph(id='pie-graph3')],style={'display': 'inline-block', 'width': '25%'}),
                html.Div([dcc.Graph(id='pie-graph4')],style={'display': 'inline-block', 'width': '25%'})

            ])

@app.callback(
    dash.dependencies.Output('time-series-graph', 'figure'),
    [dash.dependencies.Input('dropdown-time-series', 'value')])
def update_figure(series):
    traces=[]
    for i in series:
        print(i)
        traces.append(go.Scatter(
            x=df['DATE'],
            y=df[i],
            text=i,
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'title': 'Date'},
            yaxis={'title': ''},
            legend={'x': 0, 'y': 1},
            hovermode='closest'

        )
    }

#pie-graph
@app.callback(
    dash.dependencies.Output('pie-graph1', 'figure'),
    [dash.dependencies.Input('time-series-graph', 'hoverData'),
     dash.dependencies.Input('dropdown-pie-graph1', 'value')
    ])
def update_figure(hoverData,value):
    DATE = hoverData['points'][0]['x']
    print('DATE is {}'.format(DATE))

    LIST=df[df['DATE']==DATE][value].values.tolist()
    print('LIST is {}'.format(LIST))
    values=[v for v in value]

    data = [
        {
            'values': LIST[0],
            'labels':value,
            'title': DATE,
            "hole": .4,
            'type': 'pie',
        },
    ]
    return {'data': data}

@app.callback(
    dash.dependencies.Output('pie-graph2', 'figure'),
    [dash.dependencies.Input('time-series-graph', 'hoverData')])
def update_figure(hoverData):
    DATE = hoverData['points'][0]['x']
    print('DATE is {}'.format(DATE))

    LIST=df[df['DATE']==DATE][['TOTAL_USERS','UURS']].values.tolist()
    print('LIST is {}'.format(LIST))
    data = [
        {
            'values': LIST[0],
            'labels':['TOTAL_USERS','UURS'],
            'title': DATE,
            "hole": .4,
            'type': 'pie',
        },
    ]
    return {'data': data}

@app.callback(
    dash.dependencies.Output('pie-graph3', 'figure'),
    [dash.dependencies.Input('time-series-graph', 'hoverData')])
def update_figure(hoverData):
    DATE = hoverData['points'][0]['x']
    print('DATE is {}'.format(DATE))

    LIST=df[df['DATE']==DATE][['TOTAL_USERS','UURS']].values.tolist()
    print('LIST is {}'.format(LIST))
    data = [
        {
            'values': LIST[0],
            'labels':['TOTAL_USERS','UURS'],
            'title': DATE,
            "hole": .4,
            'type': 'pie',
        },
    ]
    return {'data': data}

@app.callback(
    dash.dependencies.Output('pie-graph4', 'figure'),
    [dash.dependencies.Input('time-series-graph', 'hoverData')])
def update_figure(hoverData):
    DATE = hoverData['points'][0]['x']
    print('DATE is {}'.format(DATE))

    LIST=df[df['DATE']==DATE][['TOTAL_USERS','UURS']].values.tolist()
    print('LIST is {}'.format(LIST))
    data = [
        {
            'values': LIST[0],
            'labels':['TOTAL_USERS','UURS'],
            'title': DATE,
            "hole": .4,
            'type': 'pie',
        },
    ]
    return {'data': data}

if __name__ == '__main__':
    app.run_server(debug=True)
