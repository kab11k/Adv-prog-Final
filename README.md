
# Adv-prog-Final
Interactive fishing map
in this project we have set ourselves the goal of understanding and getting people to understand how fishing develops in different parts of the world and how it affects different Marine Protected Areas (MPAs), to do this, we developed a map to show the positioning of boats in the various regions of the world during from 2012 to 2020 and also added a layer showing the different Marine Protected Areas (MPAs)

## Motivation
We decided to choose this topic and consequently to develop this map because we believe that the problem of overfishing and illegal fishing related to MPAS is often underestimated, and furthermore, it is a problem that affects everyone.

## Method 
we thought that using a very simple and intuitive map for the user allows anyone, by following a few simple steps, to be able to consult the map and consequently realise how extensive the problem is and which are the regions more touched by this problem.

To create these maps we first had to filter the data we needed, this was done, as the amount of data was very large, by doing this we made our code more efficient.
We  decided to use the 'folium' library as it is very intuitive for the user. 
To use this library, we had to convert our data and put it into a 'nested list'.
For MPAs, we had to use a different approach ...... [ANNA continue].
We then created a temporal index to allow our map to become a 'timelapse' and finally merged the different databases (fishing effort, encounter and MPAs) into one map.

## Data description
…



# Running instructions
Explain to potential users how to run/replicate your workflow. If necessary, touch upon the required input data, which secret credentials are required (and how to obtain them), which software tools are needed to run the workflow (including links to the installation instructions), and how to run the workflow.

# Required software
```bash
pip install Pandas

pip install Folium

pip install Geopandas

pip install Shapely

pip install Pathlib2

.....
```

PackagePandas - version
item Folium - version
item Geopandas - version 
item Shapely - version
item Pathlib2 - version 
item Display from Template from jinja2 - version 
item Datetime - version
item Os
item Matplotlib.pyplot


## More resources
Data MMSI,Encounter https://globalfishingwatch.org/datasets-and-code/ 

Data MPAs https://www.protectedplanet.net/en/resources

Data FAO https://www.fao.org/fishery/en/area/search

## About
BONNER Katelyn, GAMBERONI Anna, BUHIC Davor.

Project carried out with the help of the University of Lausanne (UNIL), in particular thanks to Professor Simon SCHEINDEGGER and the TAs: Aryan EFTEKHARI , Antoine DIDISHEIM, Aleksandra MALOVA



UNIL Advanced programming final project
