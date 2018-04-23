# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import time
from datetime import datetime


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

'''



#--APP--##
app = dash.Dash(__name__)

def make_layout():
    df=get_data()
    dic={'current_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
         'last_data_date':df['DATE'].max()}

    return html.Div(children=[
                html.H1(children='Users Under Risk'),

                html.Div(children='''
                    Last Updated {current_time} Last Data Date {last_data_date}.
                '''.format(**dic)),

                html.Label('Select Series'),
                dcc.Dropdown(
                    options=[
                        {'label': 'TOTAL USERS', 'value': 'TOTAL_USERS'},
                        {'label': 'UURS', 'value': 'UURS'},
                    ],
                    value=['TOTAL_USERS', 'UURS'],
                    multi=True
                ),

                dcc.Graph(
                    id='example-graph',
                    figure={
                        'data': [
                            {'x': df['DATE'], 'y': df['TOTAL_USERS'], 'type': 'line', 'name': 'TOTAL_USERS'},
                            {'x': df['DATE'], 'y': df['UURS'], 'type': 'line', 'name': 'UURS'},
                        ],
                        'layout': {
                            'title': 'Evolucion UURS'
                        }
                    }
                )
            ])


def schedule():
    while True:
        app.layout = make_layout
        app.run_server(debug=True)
        while datetime.datetime.now().second !=30:
            #DO PROCESS
            time.sleep(100)

if __name__ == '__main__':
    schedule()
