import psycopg2
class PostGresAPI():
    def __init__(self, dbname, username, password, host, port):
        self.conn = psycopg2.connect("dbname='"+dbname+"' user= "+username+" password= "+password+" host= "+host+" port= "+port)
        self.cur = self.conn.cursor()
        self.dbname = dbname
        
    def disconnect(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()
        
    def isLoginValid(self,username,password):
        self.cur.execute("select password from accounts where username = '"+username+"'")
        data = self.cur.fetchall()
        self.conn.commit()
        if len(data) == 0:
            #print("Wrong Username")
            return "Invalid_username"
        elif data[0][0] == password:
            return "Valid"
        else:
            #print("Wrong Password")
            return "Invalid_password"
        
    def isRegisterValid(self, username):
        self.cur.execute("select * from accounts where username = '"+username+"'")
        data = self.cur.fetchall()
        self.conn.commit()
        if len(data) == 0:
            return True
        else:
            return False
        
    def saveAccountData(self, username, password, email, firstname, lastname, role):
        self.cur.execute("INSERT INTO accounts (username,password,email,firstname,lastname,role) "+
                         "values ('"+username+"','"+password+"','"+email+"','"+firstname+"','"+lastname+"','"+role+"')")
        self.conn.commit()
        
    def getTileData(self):
        self.cur.execute("select * from tiles")
        data = self.cur.fetchall()
        self.conn.commit()
        return data
    
    def saveTileData(self, link, linkname, minlat, minlong, maxlat, maxlong, epsg, createby, createon, hide):
        self.cur.execute("INSERT INTO accounts (link,linkname,minlat,minlong,maxlat,maxlong,epsg,createby,createon,hide) "+
                         "values ('"+link+"','"+linkname+"','"+minlat+"','"+minlong+"','"+maxlat+"','"+maxlong+"','"+
                                     epsg+"','"+createby+"','"+createon+"','"+hide+"')")
        self.conn.commit()

    def getPassword(self, username, email):
        self.cur.execute("select email from accounts where username = '"+username+"'")
        data = self.cur.fetchall()
        self.conn.commit()
        if len(data) == 0:
            return None
        elif data[0][0] == email:
            self.cur.execute("select password from accounts where username = '"+username+"'")
            password = self.cur.fetchall()
            self.conn.commit()
            return password[0][0]
        else:
            return None

    def getUserData(self,username):
        self.cur.execute("select firstname,lastname from accounts where username = '"+username+"'")
        data = self.cur.fetchall()
        self.conn.commit()
        if len(data) == 0:
            return None
        else:
            return data[0]

    def checkRole(self,username):
        self.cur.execute("select role from accounts where username = '"+username+"'")
        data = self.cur.fetchall()
        self.conn.commit()
        if len(data) == 0:
            return None
        else:
            return data[0][0]

    def changeRole(self,username,newrole):
        self.cur.execute("update accounts set role = '"+newrole+"' where username = '"+username+"'")
        self.conn.commit()

    def countUnknown(self):
        self.cur.execute("select username from accounts where role = 'unknown'")
        data = self.cur.fetchall()
        self.conn.commit()
        return len(data)

    def getUnknown(self):
        self.cur.execute("select * from accounts where role = 'unknown'")
        data = self.cur.fetchall()
        self.conn.commit()
        return data
        
