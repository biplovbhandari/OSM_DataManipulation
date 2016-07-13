import posixpath
import argparse
import urllib
import os
import sys
import base64
import settings as setting
import progressTiles as progress_tiles
import database_api as db
from ftplib import FTP
from SimpleHTTPServer import SimpleHTTPRequestHandler
from BaseHTTPServer import HTTPServer

class RootedHTTPAuthServer(HTTPServer):
    def __init__(self, base_path, *args, **kwargs):
        HTTPServer.__init__(self, *args, **kwargs)
        self.RequestHandlerClass.base_path = base_path

class RootedHTTPAuthHandler(SimpleHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header("WWW-Authenticate", "Basic realm=\"Test\"")
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
    def do_GET(self):
        if self.headers.getheader("Authorization") == None:
            self.do_AUTHHEAD()
            self.wfile.write("no auth header received")
            pass
        else:
            header = str(self.headers.getheader("Authorization"))
            key = base64.b64decode(header.split(" ")[1]).split(":")
            database = db.PostGresAPI(setting.database_name, setting.database_username, setting.database_password, setting.database_host, setting.database_port)
            if database.isLoginValid(key[0],key[1]) == "Valid":
                SimpleHTTPRequestHandler.do_GET(self)
                f = self.send_head()
                if f:
                    try:
                        self.copyfile(f, self.wfile)
                    finally:
                        f.close()
                pass
            else:
                self.do_AUTHHEAD()
                self.wfile.write(self.headers.getheader("Authorization"))
                self.wfile.write("not authenticated")
                pass
            
    def send_head(self):
        path = self.translate_path(self.path)
        f = None
        ctype = self.guess_type(path)
        try:
            f = open(path, 'rb')
        except IOError:
            self.send_error(404, "File not found")
            return None
        try:
            self.send_response(200)
            self.send_header("Content-type", ctype)
            fs = os.fstat(f.fileno())
            self.send_header("Content-Length", str(fs[6]))
            self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
            self.end_headers()
            return f
        except:
            f.close()
            raise
        
    def translate_path(self, path):
        path = posixpath.normpath(urllib.unquote(path))
        words = path.split('/')
        words = filter(None, words)
        path = self.base_path
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir):
                continue
            path = os.path.join(path, word)
        return path
    
class FtpClient:
     def __init__(self,address,username,password):
         self.ftp = FTP(address)
         self.ftp.login(user=username,passwd=password)
         self.progresso = progress_tiles.ProgressTMS(None, -1, "Uploading tiles...")
         
     def grabFile(self,location):
         localfile = open(location, "wb")
         self.ftp.retrbinary("RETR "+ location, localfile.write, 1024)
         localfile.close()
         
     def placeFile(self,location):
         self.ftp.storbinary("STOR "+location, open(location, "rb"))
         
     def placedirectory(self,location):
         pos = len(location)-1
         if location[pos] == "/":
             pos = pos-1
         root_name = ""
         while location[pos] != "/":
             root_name = location[pos]+root_name
             pos = pos-1
         self.createDir(root_name)
         for root, dirs, files in os.walk(location, topdown=True):
            relative = root[len(location):].lstrip(os.sep).replace('\\','/')
            for d in dirs:
                self.ftp.cwd(root_name)
                path_dir = os.path.join(relative, d)
                self.createDir(path_dir)
            for f in files:
                if relative == "":
                    cur_dir = root_name+"/"+f
                else:
                    cur_dir = root_name+"/"+relative+"/"+f
                if cur_dir not in self.ftp.nlst(root_name+"/"+relative):
                    self.ftp.cwd(root_name+"/"+relative)
                    path_file = os.path.join(location, relative, f)
                    self.progresso.changeValue(path_file)
##                    print(path_file)
                    self.ftp.storbinary("STOR " + f, open(path_file, "rb"))
                    self.ftp.cwd("/")
         self.progresso.Destroy()
            
     def disconnect(self):
         self.ftp.quit()
         
     def createDir(self,directory): 
         try:
             self.ftp.mkd(directory)
         except:
             pass
         self.ftp.cwd("/")

     def showDir(self):
          self.ftp.dir()
          
def createHttpServer(address,path,HandlerClass=RootedHTTPAuthHandler,ServerClass=RootedHTTPAuthServer):
     httpd = ServerClass(path, address, HandlerClass)
     sa = httpd.socket.getsockname()
     httpd.serve_forever()
#createHttpServer(("203.159.29.196",8000),"E:/ftpserver")
##client = FtpClient("203.159.29.196","polawat789","polpol01")
##client.placedirectory("D:/Sateltiles/Alles/tiff/Astana2")
