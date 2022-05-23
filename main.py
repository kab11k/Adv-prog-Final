import geopandas as gpd
import pandas as pd
import shapely
import pathlib2 as pl2
import folium
from folium.plugins import HeatMapWithTime
from folium.map import Layer
from jinja2 import Template 
from IPython.display import display
import datetime
import map_functions

#Load data:
df = pd.read_csv('data/df_monthly.csv') #contains the cleaned monthly vessel location data
df_encounter = pd.read_csv('data/df_encounter.csv') #contains data on encounters between fishing vessels and carriers, identifying which encounters were authorized or had unknown authorization
gdf_FAO_poly = gpd.read_file('data/MPA_FAO_poly.shp')
gdf_FAO_points = gpd.read_file('data/MPA_FAO_points.shp')#MPA_FAO_poly and MPA_FAO_points contain the FAO defined major marine areas and the corresponding MPAs contained within
fao_area = gpd.read_file('data/FAO_AREAS_CWP.shp') #contains FAO areas


#create user map region and data year menu:
#user map region selection:
print("Map Regions:\n")
options1 = ["Global", "FAO Area 58: Antartic and Southern Indian Ocean", "FAO Area 18: Arctic Sea", "FAO Area 48: Atlantic, Antartic", "FAO Area 34: Atlantic, Eastern Central", "FAO Area 27: Atlantic, Northeast", "FAO Area 47: Atlantic, Southeast", "FAO Area 41: Atlantic, Southwest", "FAO Area 31: Atlantic, Western-Central", "FAO Area 57: Indian Ocean, Eastern", "FAO Area 51: Indian Ocean, Western", "FAO Area 37: Mediterranean and Black Sea", "FAO Area 21: Northwest Atlantic", "FAO Area 88: Pacific, Antartic", "FAO Area 77: Pacific, Eastern Central", "FAO Area 67: Pacific, Northeast", "FAO Area 61: Pacific, Northwest", "FAO Area 87: Pacific, Southeast", "FAO Area 81: Pacific, Southwest", "FAO Area 71: Pacific, Western Central"]
res1 = map_functions.user_menu(options1)
print(options1[res1])
#user data year selection:
print("\nData Year:\n")
options2 = ["2012","2013","2014","2015","2016","2017","2018", "2019", "2020"]
res2 = map_functions.user_menu(options2)
print(options2[res2])


#Filter data based on user selection:
year_selection = (datetime.datetime.strptime(options2[res2], "%Y")).year
area_selection = options1[res1][9:11]
df = df.loc[df['year'] == year_selection]
df_encounter = df_encounter.loc[df_encounter['year'] == year_selection]


#Create weight columns for heatmap using fishing hours:
#Fishing hour weights must be nomalized between 0 and 1 for heatmapwithtimelapse plugin:
df['fishing_hours_normalized']=(df['fishing_hours']-df['fishing_hours'].min())/(df['fishing_hours'].max()-df['fishing_hours'].min())
#create dummy weight column for encounter data:
df_encounter['fishing_hours_normalized'] = 1


print('Please wait while map loads...')

#create nested list of latitude, longitude, and fishing hours by month for timelapse:
lat_lon_list = map_functions.lat_lon(df)
lat_lon_list2 = map_functions.lat_lon(df_encounter)


print('Almost there...')

#create time index for timelapse display:
time_index = [] 
for i in df['year_month'].astype(str).unique():
    time_index.append(i) 
      
    
#Create base map based on user selection:
if options1[res1] == "Global":
    my_map = folium.Map(location=[13,16], 
                    min_zoom = 0, max_zoom = 12, zoom_start = 2)
else:
    FAO_coords = map_functions.get_FAO_center(fao_area)
    FAO_coords = FAO_coords.loc[FAO_coords['FAO_code'] == area_selection]
    my_map = folium.Map(location=[FAO_coords['lat'],FAO_coords['lon']], 
                    min_zoom = 0, max_zoom = 12, zoom_start = 3)
    map_functions.plot_MPA(gdf_FAO_points, gdf_FAO_poly, int(area_selection),my_map) #add MPA layer
    map_functions.plot_FAO_areas(fao_area, area_selection, my_map) #add FAO layer
    

#Add vessel location layer:
HeatMapWithTime(lat_lon_list,radius=1,show=True,auto_play=True,position='bottomright',name="Fishing Effort",scale_radius=True,max_opacity=0.7,index=time_index).add_to(my_map)

#Add encounter data layer:
#color gradient for unauthorized encounters
gradient = {0: '#ccc', .75: '#9f9f9f', 1: '#000000'} 
map_functions.HeatMapWithTimeAdditional(lat_lon_list2, gradient=gradient,name="Unauthorized Encounters").add_to(my_map)

folium.LayerControl().add_to(my_map)
 
my_map.save("Map.html")

print('Finished - thank you!')