import psycopg2

class PostGresAPI():
    def __init__(self, dbname, username, password, host, port):
        script = "dbname=\'%s\' user= %s password= %s host= %s port= %s" %(dbname, username, password, host, port)
        self.conn = psycopg2.connect(script)
        self.cur = self.conn.cursor()
        self.dbname = dbname
        
    def disconnect(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()
        
    def isLoginValid(self,username,password):
        script = "select password from accounts where username = \'%s\' and role != 'ban' and role != 'unknown'" %(username)
        self.cur.execute(script)
        data = self.cur.fetchall()
        self.conn.commit()
        if len(data) == 0:
            return "Invalid_username"
        elif data[0][0] == password:
            return "Valid"
        else:
            return "Invalid_password"
        
    def isRegisterValid(self, username):
        script = "select * from accounts where username = \'%s\'" %(username)
        self.cur.execute(script)
        data = self.cur.fetchall()
        self.conn.commit()
        if len(data) == 0:
            return True
        else:
            return False

    def isDuplicateTMS(self, TMS_link):
        script = "select * from tiles where linkname = \'%s\'" %(TMS_link)
        self.cur.execute(script)
        data = self.cur.fetchall()
        self.conn.commit()
        if len(data) == 0:
            return True
        else:
            return False
        
    def saveAccountData(self, username, password, email, firstname, lastname, role):
        script="""INSERT INTO accounts (username,password,email,firstname,lastname,role)
            values (\'%s\', \'%s\', \'%s\'
            , \'%s\', \'%s\', \'%s\')""" %(username, password, email, firstname, lastname, role)
        self.cur.execute(script)
        self.conn.commit()
        
    def getTileData(self):
        self.cur.execute("select * from tiles")
        data = self.cur.fetchall()
        self.conn.commit()
        return data
    
    def saveTileData(self, link, linkname, minlat, minlong, maxlat, maxlong, epsg, createby, createon, hide):
        script="""INSERT INTO tiles (link,linkname,minlat,minlong,maxlat,maxlong,epsg,createby,createon,hide)
            values (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\'
            , \'%s\')""" %(link, linkname, minlat, minlong, maxlat, maxlong, epsg, createby, createon, hide)
        self.cur.execute(script)
        self.conn.commit()

    def getPassword(self, username, email):
        script="select email from accounts where username = \'%s\'" %(username)
        self.cur.execute(script)
        data = self.cur.fetchall()
        self.conn.commit()
        if len(data) == 0:
            return None
        elif data[0][0] == email:
            password_script="select password from accounts where username = \'%s\'" %(username)
            self.cur.execute(password_script)
            password = self.cur.fetchall()
            self.conn.commit()
            return password[0][0]
        else:
            return None

    def getUserData(self,username):
        script="select firstname,lastname from accounts where username = \'%s\'" %(username)
        self.cur.execute(script)
        data = self.cur.fetchall()
        self.conn.commit()
        if len(data) == 0:
            return None
        else:
            return data[0]

    def checkRole(self,username):
        script="select role from accounts where username = \'%s\'" %(username)
        self.cur.execute(script)
        data = self.cur.fetchall()
        self.conn.commit()
        if len(data) == 0:
            return None
        else:
            return data[0][0]

    def changeRole(self,username,newrole):
        script="update accounts set role = \'%s\' where username = \'%s\'" %(newrole, username)
        self.cur.execute(script)
        self.conn.commit()

    def countUnknown(self):
        script = "select username from accounts where role = 'unknown'"
        self.cur.execute(script)
        data = self.cur.fetchall()
        self.conn.commit()
        return len(data)

    def getUnknown(self):
        script = "select * from accounts where role = 'unknown'"
        self.cur.execute(script)
        data = self.cur.fetchall()
        self.conn.commit()
        return data

    def changeHide(self,link,newhide):
        script="update tiles set hide = \'%s\' where link = \'%s\'" %(newhide,link)
        self.cur.execute(script)
        self.conn.commit()
