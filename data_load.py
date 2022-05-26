##################################################################################################################Note: This code was used to combine and clean the raw vessel location data, FAO marine area shape files, and MPA shape files. Due to the size of these raw files and the processing time, we have provided the output of this code as the data to load in the main file. Do not run this.
##################################################################################################################


import pandas as pd
import os
import datetime as dt
import geopandas as gpd
import os
import webbrowser
import folium
import matplotlib.pyplot as plt
import numpy as np
import shapely
import map_functions
from google.colab import drive
drive.mount('/content/gdrive')

##################################################################################################################Vessel Data:


#read in all vessel location data:
parent_path = "/Users/katebonner/Documents/UNIL/Spring 22/Adv programming/GFW Data"

df_list = []
for folder in os.listdir(parent_path):
    if not folder.startswith('.'): #mac contains hidden folders that we must skip
        for csv_file in os.listdir(os.path.join(parent_path, folder)):
            df = pd.read_csv(os.path.join(parent_path, folder, csv_file))
            df_list.append(df)

df_raw = pd.concat(df for df in df_list)


#Remove entries with no fishing hours:
df_raw = df_raw.loc[df_raw['fishing_hours'] != 0 ]

#read in all encounter authorization data:
df_encounter = pd.read_csv('/Users/katebonner/Documents/UNIL/Spring 22/Adv programming/encounter.csv', usecols = ["start","lat","lon","vessel.mmsi","encounter.encountered_vessel.mmsi","encounter.authorization_status"])
#Remove authorized encounters:
df_encounter = df_encounter.loc[df_encounter['encounter.authorization_status'] == 'unknown' ]
#Rename lat and lon columns to match vessel data:
df_encounter.rename(columns={'lat': 'cell_ll_lat', 'lon': 'cell_ll_lon'}, inplace=True)

#create year and year_month column:
df_raw['year_month'] = pd.to_datetime(df_raw['date']).dt.to_period('M')
df_encounter['year_month'] = pd.to_datetime(df_encounter['start']).dt.to_period('M')

df_raw['year'] = pd.DatetimeIndex(df_raw['date']).year
df_encounter['year'] = pd.DatetimeIndex(df_encounter['start']).year

#Aggregate vessel data
df_monthly = df_raw.groupby(['year_month','year','cell_ll_lat','cell_ll_lon'],as_index = False)['fishing_hours'].sum()

#save dfs:
df_monthly.to_csv('/Users/katebonner/Documents/UNIL/Spring 22/Adv programming/GFW Data cleaned/df_monthly.csv', index=False)
df_encounter.to_csv('/Users/katebonner/Documents/UNIL/Spring 22/Adv programming/GFW Data cleaned/df_encounter.csv',index=False)



##################################################################################################################FAO and MPA:

#Data load and clean:

#load MPA point data:
file_point = os.listdir('/content/gdrive/My Drive/AD_DATA/points')
path_point = [os.path.join('/content/gdrive/My Drive/AD_DATA/points', i) for i in file_point if ".shp" in i]

gdf_points = gpd.GeoDataFrame(pd.concat([gpd.read_file(i) for i in path_point], 
                        ignore_index=True), crs=gpd.read_file(path_point[0]).crs)

# Files contain terrestrial conservation areas as well, keep only marine areas:
gdf_points = gdf_points[gdf_points['MARINE']!='0']

#load MPA polygon files:
os.listdir('/content/gdrive/My Drive/AD_DATA/polygons')
path = '/content/gdrive/My Drive/AD_DATA/polygons/WDPA_May2022_Public_shp-polygons0.shp'
gdf_poly = gpd.read_file(path)
path = '/content/gdrive/My Drive/AD_DATA/polygons/WDPA_May2022_Public_shp-polygons1.shp'
gdf_poly1 = gpd.read_file(path)
path = '/content/gdrive/My Drive/AD_DATA/polygons/WDPA_May2022_Public_shp-polygons2.shp'
gdf_poly2 = gpd.read_file(path)

# append the files
gdf_poly = gdf_poly.append(gdf_poly1)
gdf_poly = gdf_poly.append(gdf_poly2)

# keep only marine MPAs
gdf_poly = gdf_poly[gdf_poly['MARINE']!='0']

# load FAO Areas:
fao_path = '/Users/katebonner/Documents/UNIL/Spring 22/Adv programming/FAO_AREAS_CWP/FAO_AREAS_CWP.shp'
fao_area = gpd.read_file(fao_path)

# assign MPA points and polygon to their respective major FAO area
fao_major = fao_area[fao_area['F_LEVEL']== 'MAJOR']
map_functions.assign_FAO_area(gdf_points, fao_major)
map_functions.assign_FAO_area(gdf_poly, fao_major)

# save to shp file
gdf_points.to_file('/content/gdrive/My Drive/AD_DATA/MPA_FAO_points.shp') 
gdf_poly.to_file('/content/gdrive/My Drive/AD_DATA/MPA_FAO_poly.shp') 
