import postgis2folium

start = time.time()
dbname="boracay"
conn = psycopg2.connect("dbname='"+dbname+"' user=postgres password=polpol01")
cur = conn.cursor()
Postgis2folium = Postgis2folium()
Postgis2folium.mapping("planet_osm_roads")
Postgis2folium.mapping("planet_osm_line")
Postgis2folium.mapping("planet_osm_polygon")
Postgis2folium.mapping("planet_osm_point")
print("Time used:",time.time()-start)
conn.commit()
cur.close()
conn.close()
#Postgis2folium.map1.click_for_marker(popup='Waypoint')
Postgis2folium.map1.create_map(path=dbname+".html")
webbrowser.open(dbname+".html")
