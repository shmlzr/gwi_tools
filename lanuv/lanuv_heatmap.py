import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
import geopandas as gpd
import numpy as np


def get_position():
    data_lib = "M:/Scholten_Juri/aa_Austausch_Scholten_Louis/Immisionskarten/Rohdaten_ungeöffnet/Messpunkte_SN_2020.xlsx"
    geoloc = pd.read_excel(data_lib, header=5, engine='openpyxl')

    geom = gpd.points_from_xy(x=geoloc['R-Wert'].values, y=geoloc['H-Wert'].values)
    gdf = gpd.GeoDataFrame(geoloc[['Unnamed: 0']], geometry=geom)
    # s = gpd.GeoSeries([Point(x, y) for x, y in zip(geoloc['R-Wert'], geoloc['H-Wert'])])
    # geo_df = gpd.GeoDataFrame(geoloc[['Unnamed: 0']], geometry=s)
    gdf.rename(columns={'Unnamed: 0': 'station_name'}, inplace=True)
    gdf = gdf.set_crs(epsg=25832).to_crs(epsg=4326)
    return ([dict(title=name, position=[y, x]) for name, y, x in zip(gdf.station_name, gdf.geometry.y, gdf.geometry.x)],
            [dict(center=[y, x]) for name, y, x in zip(gdf.station_name, gdf.geometry.y, gdf.geometry.x)],
            gdf)


def get_data(dataset_name):
    path = "M:/Scholten_Juri/aa_Austausch_Scholten_Louis/Immisionskarten/Rohdaten_ungeöffnet/"

    data_lib = {'geoloc': path + 'Messpunkte_SN_2020.xlsx',
                'no2_2018': path + 'OpenKontiLUQS_NO2_2018.csv',
                'no2_2019': path + 'OpenKontiLUQS_NO2_2019.csv',
                'no2_2020': path + 'OpenKontiLUQS_NO2_2020.csv',
                'pm10_2010-2019': path + 'OpenKontiLUQS_PM10_2010-2019.csv',
                'pm10_2018': path + 'OpenKontiLUQS_PM10_2018.csv',
                'pm10_2019': path + 'OpenKontiLUQS_PM10_2019.csv',
                'pm10_2020': path + 'OpenKontiLUQS_PM10_2020.csv'}

    data = pd.read_csv(data_lib[dataset_name], parse_dates=[['Datum', 'Zeit']], infer_datetime_format=True,
                       delimiter=';', header=2, encoding='unicode_escape').set_index('Datum_Zeit')

    # to numeric
    data.replace('<', '', regex=True, inplace=True)
    data = data.apply(pd.to_numeric)
    return data


def create_heatmap(data, station_name):

    data_name = [i for i in data.keys().to_list() if station_name in i][0]

    data = data[data_name]

    DAYS = ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun']
    MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']

    #plt.close('all')
    #fig, ax = plt.subplots(1, 1)
    start = data.index.min()
    end = data.index.max()
    num_days = (end - start).days
    #xticks = pd.date_range('00:00', '23:00', freq='1H').strftime('%H:%M')
    heatmap = np.full([num_days, 24], np.nan)

    for day in range(num_days):
        timei=0
        for time in list(range(1, 24)) + [0]:
            date = start + np.timedelta64(time, '1h') + np.timedelta64(day, 'D')
            # # print(date)
            # if date.day == 1:
            #     yticks[day] = MONTHS[date.month - 1]
            #
            # if date.dayofyear == 1:
            #     yticks[day] += f'\n{date.year}'

            # if start <= date < end:
            if type(data.loc[date]) == np.float64:
                heatmap[day, timei] = data.loc[date]
            else:
                heatmap[day, timei] = data.loc[date]
            timei += 1

    # Plotting
    fig = go.Figure(data=go.Heatmap(
                    z=heatmap,
                    x=pd.date_range('0:00', '23:00', freq='1H').strftime('%H:%M'),
                    y=pd.date_range(start, end),
                    colorscale='Oranges',
                    ))
    fig.update_layout(title=data_name)
    return fig


def create_heatmap_mpl(data, station_name):

    data_name = [i for i in data.keys().to_list() if station_name in i][0]

    data = data[data_name]

    DAYS = ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun']
    MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']

    plt.close('all')
    fig, ax = plt.subplots(1, 1)
    start = data.index.min()
    end = data.index.max()
    num_days = (end - start).days
    xticks = pd.date_range('00:00', '23:00', freq='1H').strftime('%H:%M')
    yticks = {}
    heatmap = np.full([num_days, 24], np.nan)
    for day in range(num_days):
        for time in range(24):
            date = start + np.timedelta64(time, '1h') + np.timedelta64(day, 'D')
            # print(date)
            if date.day == 1:
                yticks[day] = MONTHS[date.month - 1]

            if date.dayofyear == 1:
                yticks[day] += f'\n{date.year}'

            # if start <= date < end:
            if type(data.loc[date]) == np.float64:
                heatmap[day, time] = data.loc[date]
            else:
                heatmap[day, time] = data.loc[date]

    # Plotting
    mesh = ax.pcolormesh(heatmap, vmin=0, vmax=50, cmap='Oranges')  # , cmap = cmap, edgecolors = 'grey')
    # vmax=data.max()

    # Invert y-axis
    ax.invert_yaxis()

    # Hatch for out of bound values in a year
    ax.patch.set(hatch='xx', edgecolor='black')

    # Set ticks
    ax.set_yticks(list(yticks.keys()))
    ax.set_yticklabels(list(yticks.values()))
    ax.set_xticks([6, 12, 18])
    ax.set_xticklabels(xticks[[6, 12, 18]])

    plt.title(data_name)

    # Add color bar
    fig.colorbar(mesh, orientation="vertical")  # , pad=0.2)
    colorbar = ax.collections[0].colorbar

    return fig


def show_heatmap(dataset_name, station_name, mpl):
    center0 = [51.43, 7.66]
    zoom0 = 8
    data = get_data(dataset_name)
    if mpl:
        fig = create_heatmap_mpl(data, station_name)
    else:
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


def plotting_without_dash(mpl=False):
    pio.renderers.default = "browser"
    dataset_name = 'pm10_2018'
    data = get_data(dataset_name)
    station_name = data.keys().to_list()[0]  # first in row
    fig, _, _ = show_heatmap(dataset_name, station_name, mpl)
    fig.show()


if __name__ == '__main__':

    # with matplotlib
    plotting_without_dash(mpl=True)

    # with plotly
    plotting_without_dash(mpl=False)
