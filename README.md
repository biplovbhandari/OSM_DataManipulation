# OSM_DataManipulation
##Prerequisities
-Python 2.7

-Jinja2(Folium dependency)

-Pandas(Folium dependency)

-Numpy(Folium dependency)

-Vincent(Folium dependency)

-Libpq(Psycopg2 dependency)

-Folium(Manipulate data and visualize it in Leaflet.js)

-Psycopg2(PostgreSQL database adapter)

##Installation
-Install all prerequisities.

-Place postgis2folium.py into your python project folder.

-If you want to visualize map tiles from your local computer place localopenstreetmap folder into postgis2folium.py into YOUR_PYTHON_PATH\Lib\site-packages\folium\templates\tiles
##Code Example
```
postgis2folium = Postgis2folium("localopenstreetmap")
postgis2folium.connect2db("DATABASENAME","USER","PASSWORD")
postgis2folium.mapping("planet_osm_point")
postgis2folium.mapping("planet_osm_roads")
postgis2folium.mapping("planet_osm_line")
postgis2folium.mapping("planet_osm_polygon")
postgis2folium.create_map()
postgis2folium.disconnectdb()
```
