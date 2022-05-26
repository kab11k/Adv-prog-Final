import pandas as pd
import geopandas as gpd
import folium
import matplotlib.pyplot as plt
import shapely
from jinja2 import Template 
from folium.map import Layer


def user_menu(options):
    '''Function creates user option list'''
    
    for idx, element in enumerate(options):
        print("{}) {}".format(idx + 1, element))
        
    while True:
        try:
            i = input("\nPlease enter selection: ")
            if 0 < int(i) <= len(options):
                return int(i) -1
        except ValueError:
            pass
        
        print("Invlaid Input")

def assign_FAO_area(dataset, data_fao):
  '''Function to assign a dataframe to the corresponding major FAO area'''

  for index, row in data_fao.iterrows():
    fao_polygon = row.geometry

    for i, r in dataset.iterrows():
      MPA_polygon = r.geometry

      if fao_polygon.contains(MPA_polygon):
        dataset.at[i, 'FAO_area'] = data_fao.at[index, 'F_AREA']

        
def lat_lon(df):
    '''Function to create a nested list of latitude, longitude, and weight by month'''
  
    lat_lon_list = []
    for i in df['year_month'].unique():
        temp = []
        for index, instance in df[df['year_month'] == i].iterrows():
            temp.append([instance['cell_ll_lat'],instance['cell_ll_lon'],instance['fishing_hours_normalized']])
        lat_lon_list.append(temp)
    
    return lat_lon_list



    
def plot_MPA(datapoints, datapoly, area, folium_map):
  '''Function to plot MPAs over the Foilum map. Only the first 150 MPAs with the greatest area are take into account'''
  
  area = str(area)
  datapoints = datapoints[datapoints['FAO_area'] == area]
  datapoly = datapoly[datapoly['FAO_area'] == area].sort_values('REP_AREA', ascending=False)[:150]

  # loop through dataset of points
  for index in range(len(datapoints)):
    # obtain the coordinates of each point in a list
    sim_geo = (datapoints.iloc[index].geometry).bounds[0:2]
    # list is inverted as latitude and longiture are inverted in foilum.Polygon
    sim_geo = sim_geo[::-1]
    folium.Polygon([sim_geo], color='black', weight=1, fill=True, fill_color='orange', fill_opacity=0.1).add_to(folium_map)

  # plot the points corresponding to MPA(points)
  for index in range(len(datapoly)):
    # check whether the area is a polygon or a multipolygon
    if type(datapoly.iloc[index].geometry) is shapely.geometry.polygon.Polygon:
      coor_pol = list(datapoly.iloc[index].geometry.exterior.coords)
      coor_pol = [(y, x) for x, y in coor_pol]
      folium.Polygon(coor_pol, color='black', weight=1, fill=True, fill_color='orange', fill_opacity=0.1).add_to(folium_map)
      
    if type(datapoly.iloc[index].geometry) is shapely.geometry.multipolygon.MultiPolygon:
      # obtain the list of polygons from the Multi-polygon and loop through them to obtain the coordinates
      pol_geom = datapoly.iloc[index].geometry
      for i in range(0,len(pol_geom)):
        coor_list = list(pol_geom.geoms[i].exterior.coords)
        coor_list = [(y, x) for x, y in coor_list]
        folium.Polygon(coor_list, color='black', weight=1, fill=True, fill_color='orange', fill_opacity=0.1).add_to(folium_map)



          
def plot_FAO_areas(fao_area, fao_code: str, folium_map):
   '''Function plots selected FAO areas to the foilum map'''
  
   fao_major = fao_area[fao_area['F_LEVEL']== 'MAJOR']
   fao_areas = fao_major[fao_major['F_CODE'] == fao_code]

   for index in range(len(fao_areas)):
     # check whether the area is a polygon or a multipolygon
     if type(fao_areas.iloc[index].geometry) is shapely.geometry.polygon.Polygon:
       coor_pol = list(fao_areas.iloc[index].geometry.exterior.coords)
       coor_pol = [(y, x) for x, y in coor_pol]
       folium.Polygon(coor_pol, color='black', weight=1, fill=True, fill_color='blue', fill_opacity=0.1, tooltip=fao_code).add_to(folium_map)
      
     if type(fao_areas.iloc[index].geometry) is shapely.geometry.multipolygon.MultiPolygon:
       # obtain the list of polygons from the Multi-polygon and loop through them to obtain the coordinates
       pol_geom = fao_areas.iloc[index].geometry
       for i in range(0,len(pol_geom)):
         coor_list = list(pol_geom.geoms[i].exterior.coords)
         coor_list = [(y, x) for x, y in coor_list]
         folium.Polygon(coor_list, color='black', weight=1, fill=True, fill_color='blue', fill_opacity=0.1, tooltip=fao_code).add_to(folium_map)



              
def get_FAO_center(fao_area):
  '''Function to obtain the central coordinates of each major FAO area'''

  #####  lat = y and lon = x ######
  fao_major = fao_area[fao_area['F_LEVEL']== 'MAJOR']
  FAO_center = fao_major[['F_CODE']].copy()
  FAO_center = FAO_center.rename(columns={'F_CODE': 'FAO_code'})

  for index, row in fao_major.iterrows():
    lat_center = row.geometry.centroid.y
    lon_center = row.geometry.centroid.x
    FAO_center.at[index, 'lat'] = lat_center
    FAO_center.at[index, 'lon'] = lon_center

  return FAO_center



    
class HeatMapWithTimeAdditional(Layer):
    '''Alows for multiple map layers to be added to heat map with timelapse without having multiple lapse control bars'''
    _template = Template("""
        {% macro script(this, kwargs) %}
            var {{this.get_name()}} = new TDHeatmap({{ this.data }},
                {heatmapOptions: {
                    radius: {{this.radius}},
                    minOpacity: {{this.min_opacity}},
                    maxOpacity: {{this.max_opacity}},
                    scaleRadius: {{this.scale_radius}},
                    useLocalExtrema: {{this.use_local_extrema}},
                    defaultWeight: 1,
                    {% if this.gradient %}gradient: {{ this.gradient }}{% endif %}
                }
            }).addTo({{ this._parent.get_name() }});
        {% endmacro %}
    """)

    def __init__(self, data, name=None, radius=1,
                 min_opacity=0, max_opacity=0.7,
                 scale_radius=True, gradient=None, use_local_extrema=False,
                 overlay=True, control=True, show=True):
        super(HeatMapWithTimeAdditional, self).__init__(
            name=name, overlay=overlay, control=control, show=show
        )
        self._name = 'HeatMap'
        self.data = data

        # Heatmap settings.
        self.radius = radius
        self.min_opacity = min_opacity
        self.max_opacity = max_opacity
        self.scale_radius = 'true' if scale_radius else 'false'
        self.use_local_extrema = 'true' if use_local_extrema else 'false'
        self.gradient = gradient
      
    
def map_of_MPA(fao_area, gdf_FAO_poly, gdf_FAO_points):
  '''The function creates a map with all the MPAs and the borders of the major FAO areas'''

  fao_major = fao_area[fao_area['F_LEVEL']== 'MAJOR']

  world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
  fig, ax = plt.subplots(figsize=(24,18))
  world.plot(ax=ax, alpha=0.3, color='black')
  gdf_FAO_poly.plot(ax=ax, color='blue', legend=True)
  gdf_FAO_points.plot(ax=ax, color='blue', legend=True)
  fao_major.geometry.boundary.plot(color=None,edgecolor='k',linewidth = 1,ax=ax)
  plt.title('MPA and FAO areas')
  plt.show()
        
        
