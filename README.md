
# Visualizing Fishing effort

In this project, we aim to provide an understanding of the extent of global fishing effort, unauthorized transshipment events, and fishing within Marine Protected Areas (MPAs). To do this, we developed a heatmap to show the density of fishing effort leveraging the Automatic Identification System (AIS) satellite positioning of vessels from 2012 to 2020 (provided by Global Fishing Watch) and added layers showing the world's current Marine Protected Areas (MPAs)

## Motivation

We choose this topic and consequently to develop this map, due to the severe state of the world's fisheries and the extent of illegal, unreported, and unregulated (IUU) fishing which is often underestimated, and furthermore, is in need of tools providing transparancy.

## Method 

We created a simple and intuitive map that allows the user to select either a global view or a specific ocean area (as defined by the FAO's major marine areas) in order view and understand the extent of fishing effort.

We have leveraged python's folium library which allows for the creation of several types of Leaflet maps and features (including heatmap and timelapse capabilities)


# Running instructions
In the terminal you need to run the "main.py" code, 

Note: data_load.py contains the code to load the raw data files and clean them. This code needs only to be run once for new years of data. Therefore, there is no need to run data_load.py when executing the program (unless you have new years of data to include)

# Required software

```bash
pip install pandas

pip install Folium

pip install Geopandas

pip install Shapely

pip install Pathlib2

```



## More resources

Data AIS vessel location and fishing effort, Transshipment encounters https://globalfishingwatch.org/datasets-and-code/ 

Data MPAs https://www.protectedplanet.net/en/resources

Data FAO https://www.fao.org/fishery/en/area/search

##Citations

Copyright 2021, Global Fishing Watch, Inc. Accessed on 18 May 2022, www.globalfishingwatch.org

Protected Planet Accessed on 22 May 2022, https://www.protectedplanet.net/en/thematic-areas/marine-protected-areas

Food and Agriculture Organization of the United Nations, Accessed on 22 May 2022, https://www.fao.org/fishery/en/area/search

## About

BONNER Katelyn, GAMBERONI Anna, BUHIC Davor.

Project carried out with the help of the University of Lausanne (UNIL), in particular thanks to Professor Simon SCHEINDEGGER and the TAs: Aryan EFTEKHARI , Antoine DIDISHEIM, Aleksandra MALOVA



UNIL Advanced programming final project
