import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_leaflet as dl
#import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from lanuv_heatmap import *


station_names = ['AABU', 'BIEL', 'BONN', 'BORG', 'BOTT', 'CHOR', 'DATT', 'DDCS',
                 'DMD2', 'DUB2', 'DURH', 'DWER', 'EIFE', 'ELAN', 'ELSB', 'EVOG',
                 'GELS', 'HATT', 'HUE2', 'JACK', 'JHNK', 'KRHA', 'LEV2', 'LOER',
                 'MGRH', 'MSGE', 'NETT', 'NIED', 'RAT2', 'RODE', 'ROTH', 'SHW2',
                 'SOES', 'SOLI', 'STYR', 'UNNA', 'VACW', 'VBID', 'VBIH', 'VDOM',
                 'VDUI', 'VEAE', 'VESN', 'VGES', 'VGLG', 'VHAM', 'VKCL', 'VKTU',
                 'VLEG', 'VMGF', 'VMS2', 'VOBM', 'VSGK', 'VWEL', 'WALS', 'WAST',
                 'WULA']

center0 = [51.43, 7.66]
zoom0 = 8

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SIMPLEX])

app.layout = html.Div([
    html.Title("LANUV - Daten"),
    dcc.Dropdown(
        id='dataset_name_dropdown',
        options=[
            {'label': 'pm10_2018', 'value': 'pm10_2018'},
            {'label': 'pm10_2019', 'value': 'pm10_2019'},
            {'label': 'pm10_2020', 'value': 'pm10_2020'},
            {'label': 'no2_2018', 'value': 'no2_2018'},
            {'label': 'no2_2019', 'value': 'no2_2019'},
            {'label': 'no2_2020', 'value': 'no2_2020'}
        ],
        value='pm10_2020'
    ),
    dcc.Dropdown(id='station_name_dropdown', placeholder="Select a station!",),
    html.Div(children=[
            dcc.Graph(id="graph", style={'width': '90vh', 'height': '70vh','display': 'inline-block'}),
            dl.Map([dl.TileLayer()] + [dl.Marker(**city) for city in get_position()[0]] + [dl.CircleMarker(**city) for city in get_position()[1]],
            #dl.Map(dl.TileLayer(), dl.GeoJSON(data=[dl.Marker(**city) for city in get_position()]),
            # [
                # dl.TileLayer(),
                # get_position()
                # #dl.LayerGroup(id="layer")
                # ],
                id="map",
                style={'width': '90vh', 'height': '70vh', 'margin': "auto", "display": "inline-block"},
                center=center0,
                zoom=zoom0),
    ]),
])


@app.callback(
    Output('station_name_dropdown', 'options'),
    [Input('dataset_name_dropdown', 'value')]
)
def update_stationname_dropdown(dataset_name):
    data = get_data(dataset_name)
    return [{'label': station, 'value': station} for station in data.keys().to_list()]

@app.callback(
    [Output("graph", "figure"), Output("map", "center"), Output("map", "zoom")],
    [Input("station_name_dropdown", "value")],
    [State("dataset_name_dropdown", "value")],
    prevent_initial_call=True)
def show_heatmap(station_name, dataset_name):
    data = get_data(dataset_name)
    fig = create_heatmap(data, station_name)

    _, _, location = get_position()

    try:
        loc_station = location.loc[location['station_name'].str.contains(station_name[:4])].loc[0]
        loc_station = [loc_station.geometry.y, loc_station.geometry.x]
        zoom = 10
    except:
        loc_station = center0
        zoom = zoom0
    return fig, loc_station, zoom

# @app.callback(
#     Output("map", "figure"),
#     [Input("dataset_name_dropdown", "value"),
#      Input("station_name_dropdown", "value")]
# )
# def show_map(dataset_name, station_name):
#     df = get_position()
#     fig = go.Figure(data=go.Scattergeo(
#         geo=df['geometry'],
#         text=df['station_name'],
#         mode='markers'
#     ))

if __name__ == '__main__':
    app.run_server(debug=True, port=8502, host='0.0.0.0')