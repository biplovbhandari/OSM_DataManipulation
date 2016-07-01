import posixpath
import argparse
import urllib
import os
import sys
from ftplib import FTP
from SimpleHTTPServer import SimpleHTTPRequestHandler
from BaseHTTPServer import HTTPServer

class RootedHTTPServer(HTTPServer):

    def __init__(self, base_path, *args, **kwargs):
        HTTPServer.__init__(self, *args, **kwargs)
        self.RequestHandlerClass.base_path = base_path


class RootedHTTPRequestHandler(SimpleHTTPRequestHandler):

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
         
     def grabFile(self,location):
         localfile = open(location, "wb")
         self.ftp.retrbinary("RETR "+ location, localfile.write, 1024)
         localfile.close()
         
     def placeFile(self,location):
         self.ftp.storbinary("STOR "+location, open(location, 'rb'))
         
     def disconnect(self):
         self.ftp.quit()
         
     def createDir(self,directory): 
         if self.dirExist(directory) == False:
             self.ftp.mkd(directory)
         self.ftp.cwd(directory)
         
     def dirExist(self,directory):
         filelist = []
         self.ftp.retrlines('LIST',filelist.append)
         for f in filelist:
             if f.split()[-1] == directory and f.upper().startswith('D'):
                 return True
         return False
     
     def showDir(self):
          self.ftp.dir()
          
def createHttpServer(address,path,HandlerClass=RootedHTTPRequestHandler,ServerClass=RootedHTTPServer):
     httpd = ServerClass(path, address, HandlerClass)
     sa = httpd.socket.getsockname()
     print "Serving HTTP on", sa[0], "port", sa[1], "..."
     httpd.serve_forever()
