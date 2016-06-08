import folium
import webbrowser
import psycopg2
import time  

class Postgis2folium:
     
     def __init__(self,latitude = 0,longitude = 0,zoom_start = 1):
          
          self.map1 = folium.Map([latitude,longitude], zoom_start=zoom_start)
          
     def convert2list(self,way):
          way = way.split(',')
          for j in range(len(way)):
               way[j] = way[j].split(' ')
               for i in range(len(way[j])):
                    way[j][i] = float(''.join(c for c in way[j][i] if c.isdigit() or c == '.'))
               way[j][0],way[j][1] = way[j][1],way[j][0]
          return way
     
     def plotting(self,id1,name,way,color):
          
          if len(way) == 1:
               self.map1.circle_marker(way[0], popup=str(id1)+"\n"+str(name).decode('utf-8')+"\n",fill_color=color, radius=3)
          else:
               self.map1.line(way, line_color=color, line_weight=5, popup=str(id1)+"\n"+str(name).decode('utf-8')+"\n")
               
     def multiline_plotting(self,ways,color):
          
          m.multiline(locations=ways,line_color=color, line_weight=2,line_opacity=1.0)
          
     def mapping(self,table_name):
          
          cur.execute("SELECT osm_id,name,ST_AsText(ST_Transform(way, 4326)) FROM "+table_name)
          data = cur.fetchall()
          for i in range(len(data)):
               if table_name == "planet_osm_roads":
                    self.plotting(data[i][0],data[i][1],self.convert2list(data[i][2]),"#FF0000")
               elif table_name == "planet_osm_line":
                    self.plotting(data[i][0],data[i][1],self.convert2list(data[i][2]),"#00FF00")
               elif table_name == "planet_osm_polygon":
                    self.plotting(data[i][0],data[i][1],self.convert2list(data[i][2]),"#0000FF")
               elif table_name == "planet_osm_point":
                    self.plotting(data[i][0],data[i][1],self.convert2list(data[i][2]),"#FFFFFF")
          print(table_name+" Done")

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
