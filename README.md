
# Visualizing Fishing effort

in this project we have set ourselves the goal of understanding and getting people to understand how fishing develops in different parts of the world and how it affects different Marine Protected Areas (MPAs), to do this, we developed a map to show the positioning of boats in the various regions of the world during from 2012 to 2020 and also added a layer showing the different Marine Protected Areas (MPAs)

## Motivation

We decided to choose this topic and consequently to develop this map because we believe that the problem of overfishing and illegal fishing related to MPAS is often underestimated, and furthermore, it is a problem that affects everyone.

## Method 

we thought that using a very simple and intuitive map for the user allows anyone, by following a few simple steps, to be able to consult the map and consequently realise how extensive the problem is and which are the regions more touched by this problem.

To create these maps we first had to filter the data we needed, this was done, as the amount of data was very large, by doing this we made our code more efficient.
We  decided to use the 'folium' library as it is very intuitive for the user. 
To use this library, we had to convert our data and put it into a 'nested list'.
We then created a temporal index to allow our map to become a 'timelapse' and finally merged the different databases (fishing effort, encounter and MPAs) into one map.


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

Data MMSI,Encounter https://globalfishingwatch.org/datasets-and-code/ 

Data MPAs https://www.protectedplanet.net/en/resources

Data FAO https://www.fao.org/fishery/en/area/search

## About

BONNER Katelyn, GAMBERONI Anna, BUHIC Davor.

Project carried out with the help of the University of Lausanne (UNIL), in particular thanks to Professor Simon SCHEINDEGGER and the TAs: Aryan EFTEKHARI , Antoine DIDISHEIM, Aleksandra MALOVA



UNIL Advanced programming final project
