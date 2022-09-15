import pandas as pd
from geopy import distance


def place_sender_stats(df):
    items = {}
    for g, gdf in df.groupby('place_sender_ref'):
        if "https://sws.geonames.org" in g:
            row = gdf.iloc[0]
            items[g] = {}
            items[g]['amount'] = len(gdf)
            for x in ['lat_x', 'long_x', 'name_x', 'country_code_x']:
                items[g][x] = row[x]
    item_df = pd.DataFrame.from_dict(items, orient='index')\
        .dropna(inplace=False).sort_values('amount', ascending=False, inplace=False)
    return item_df


def place_receiver_stats(df):
    items = {}
    for g, gdf in df.groupby('place_receiver_ref'):
        if "https://sws.geonames.org" in g:
            row = gdf.iloc[0]
            items[g] = {}
            items[g]['amount'] = len(gdf)
            for x in ['lat_y', 'long_y', 'name_y', 'country_code_y']:
                items[g][x] = row[x]
    item_df = pd.DataFrame.from_dict(items, orient='index')\
        .dropna(inplace=False).sort_values('amount', ascending=False, inplace=False)
    return item_df


def sender_stats(df):
    items = {}
    for g, gdf in df.groupby('sender_ref'):
        if "d-nb.info" in g:
            row = gdf.iloc[0]
            items[g] = {}
            items[g]['amount'] = len(gdf)
            for x in ['sender_name', 'sender_ref']:
                items[g][x] = " ".join(row[x].split())
    item_df = pd.DataFrame.from_dict(items, orient='index')\
        .dropna(inplace=False).sort_values('amount', ascending=False, inplace=False)
    return item_df


def receiver_stats(df):
    items = {}
    for g, gdf in df.groupby('receiver_ref'):
        if "d-nb.info" in g:
            row = gdf.iloc[0]
            items[g] = {}
            items[g]['amount'] = len(gdf)
            for x in ['receiver_name', 'receiver_ref']:
                items[g][x] = " ".join(row[x].split())
    item_df = pd.DataFrame.from_dict(items, orient='index')\
        .dropna(inplace=False).sort_values('amount', ascending=False, inplace=False)
    return item_df


def get_distance(row):
    """ helper function to calculate distance from lat/lng columns in dataframe """
    if row['place_sender_name'] == row['place_receiver_name']:
        dist = 0
    else:
        point_a = (row['lat_x'], row['long_x'])
        point_b = (row['lat_y'], row['long_y'])
        try:
            dist = distance.distance(point_a, point_b).km
        except:
            dist = 0
    return dist