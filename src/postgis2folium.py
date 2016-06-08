import folium
import psycopg2

class Postgis2folium:
     
     def __init__(self,latitude = 0,longitude = 0,zoom_start = 1):
          
          self.map1 = folium.Map([latitude,longitude], zoom_start=zoom_start)
          
     def connect2db(self,dbname,username,password):
          self.dbname = dbname
          self.conn = psycopg2.connect("dbname='"+dbname+"' user= "+username+" password= "+password)
          self.cur = self.conn.cursor()

     def disconnectdb(self):
          self.conn.commit()
          self.cur.close()
          self.conn.close()
          
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
               self.map1.add_children(folium.CircleMarker(location=way[0], popup=str(id1)+"\n"+str(name).decode('utf-8')+"\n",fill_color=color, radius=3))
          else:
               self.map1.add_children(folium.PolyLine(locations=way, color=color, weight=5, popup=str(id1)+"\n"+str(name).decode('utf-8')+"\n"))
               
     def mapping(self,table_name):
          
          self.cur.execute("SELECT osm_id,name,ST_AsText(ST_Transform(way, 4326)) FROM "+table_name)
          data = self.cur.fetchall()
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
          
     def create_map(self):
          postgis2folium.map1.create_map(path=self.dbname+".html")
'''
postgis2folium = Postgis2folium()
postgis2folium.connect2db("boracay","postgres","polpol01")
postgis2folium.mapping("planet_osm_point")
postgis2folium.mapping("planet_osm_roads")
postgis2folium.mapping("planet_osm_line")
postgis2folium.mapping("planet_osm_polygon")
postgis2folium.create_map()
postgis2folium.disconnectdb()
'''
