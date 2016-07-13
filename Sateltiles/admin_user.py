import wx
import os
import time
from init import *
import login as log
import manage_user as manage
import database_api as db
import settings as setting
import generateTiles as gdal
import protocol as serverTMS

class AdminUserPage(wx.Frame):
    def __init__(self, parent, role, userName, title):
        super(AdminUserPage, self).__init__(parent, title=title, size=(600,520)
            , style=wx.MINIMIZE_BOX| wx.SYSTEM_MENU | wx.CAPTION
            | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        wx.Frame.CenterOnScreen(self)
        self.panel = wx.Panel(self)
        self.icon = wx.Icon("iconn.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)
        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(25)
        existing_label = wx.StaticText(self.panel, pos=(20,20), label="Existing TMS")
        existing_label.SetFont(font)
        generate_label = wx.StaticText(self.panel, pos=(20,200+130), label="Generate TMS")
        generate_label.SetFont(font)
        source_filePath_label = wx.StaticText(self.panel, pos=(10,230+130), label="Source file (.tif) : ") 
        self.source_filePath_entry = wx.TextCtrl(self.panel, pos=(100,230+130), size=(165,20)) # sorce file path entries
        save_filePath_label = wx.StaticText(self.panel, pos=(20,260+130), label="Save location : ")
        self.save_filePath_entry = wx.TextCtrl(self.panel, pos=(100,260+130), size=(165,20)) # destination file path entries
        # all buttons
        getLink_button = wx.Button(self.panel, label="GET TMS LINK", pos=(470,190+130), size=(100,40)) 
        getLink_button.Bind(wx.EVT_BUTTON, self.getTMS_Link)
        back_button = wx.Button(self.panel, label="BACK", pos=(10,310+130), size=(100,40)) 
        back_button.Bind(wx.EVT_BUTTON, self.backHome)
        source_button = wx.Button(self.panel, label="Browse", pos=(280,227+130), size=(90,25)) 
        source_button.Bind(wx.EVT_BUTTON, self.browseSourceFile)
        save_button = wx.Button(self.panel, label="Browse", pos=(280,257+130), size=(90,25)) 
        save_button.Bind(wx.EVT_BUTTON, self.browseSaveFile)
        generate_button = wx.Button(self.panel, label="GENERATE", pos=(175,285+130), size=(90,30)) 
        generate_button.Bind(wx.EVT_BUTTON, self.generateTMS)
        manage_button = wx.Button(self.panel, label="Manage user", pos=(470,310+130), size=(100,40)) 
        manage_button.Bind(wx.EVT_BUTTON, self.manageUser)
        self.hideLink_button = wx.Button(self.panel, label="Hide", pos=(480,240+130), size=(80,30)) 
        self.hideLink_button.Bind(wx.EVT_BUTTON, self.hide_Link)       
        try:# try to connect to main database
            self.database = db.PostGresAPI(setting.database_name, setting.database_username
                , setting.database_password, setting.database_host, setting.database_port) 
            count_user = self.database.countUnknown()
            if count_user < 2:
                amount_label = "%s user on waiting list" %(count_user)
            else:
                amount_label = "%s users on waiting list" %(count_user)
            self.amount_of_unauthenticated_label = wx.StaticText(self.panel, pos=(440,290+130), label=amount_label)
            self.amount_of_unauthenticated_label.SetFont(font)
            if role != "superadmin":  # only super admin can see this button
                manage_button.Show(False)
                self.hideLink_button.Show(False)
                self.amount_of_unauthenticated_label.Show(False)
            self.createTable()
            self.tif_path = ""
            self.save_path = ""
            self.curUserName = userName
            self.Show(True)
        except:
            msg = "Can not connect to database (%s:%s)" %(setting.database_host, setting.database_port)
            wx.MessageBox(msg, "Connection error", wx.OK | wx.ICON_ERROR)
            self.Destroy() # close LoginPage
            log.LoginPage(None, title="Sateltiles")  # open up login page

    def hide_Link(self, evt):
        count = self.list.GetItemCount()
        item_data = []
        try:
            for row in range(count):
                if self.list.IsSelected(row): # get selected item data
                    for k in range(self.list.GetColumnCount()):
                        item = self.list.GetItem(itemId=row, col=k) # add item element in item_data list
                        item_data.append(item.GetText())
                    if self.table[row][9] == "1":
                        self.database.changeHide(self.table[row][0], "0") # unhide this link
                    elif self.table[row][9] == "0":
                        self.database.changeHide(self.table[row][0], "1") # unhide this link
                    break
            self.list.Destroy()
            self.createTable()
        except:
            msg = "Can not connect to database (%s:%s)" %(setting.database_host, setting.database_port)
            wx.MessageBox(msg, "Connection error", wx.OK | wx.ICON_ERROR)
            self.Destroy() # close LoginPage
            log.LoginPage(None, title="Sateltiles")  # open up login page

    def backHome(self, evt):
        self.Destroy() # close LoginPage
        log.LoginPage(None, title="LoginPage")  # open up login page

    def getTMS_Link(self, evt):
        count = self.list.GetItemCount()
        item_data = []
        for row in range(count):
            if self.list.IsSelected(row): # get selected item data
                for k in range(self.list.GetColumnCount()):
                    item = self.list.GetItem(itemId=row, col=k) # add item element in item_data list
                    item_data.append(item.GetText())
                dlg = wx.TextEntryDialog(None, self.table[row][1], "TMS link", self.table[row][0])
                ret = dlg.ShowModal()
                dlg.Destroy()
                break

    def createTable(self):
        self.list = wx.ListCtrl(self.panel,pos=(20,0+50), size=(550,260), style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        colName = ["Name", "Min lat", "Max lat", "Min long", "Max long", "EPSG", "Create by", "Create on", "Hide"]
        # Insert columns
        for i in range(9):
            self.list.InsertColumn(i,colName[i])
        self.table = self.database.getTileData()
        for row in range(len(self.table)):
            pos = self.list.InsertStringItem(row, self.table[row][1])
            self.list.SetStringItem(pos, 1, self.table[row][2])
            self.list.SetStringItem(pos, 2, self.table[row][4])
            self.list.SetStringItem(pos, 3, self.table[row][3])
            self.list.SetStringItem(pos, 4, self.table[row][5])
            self.list.SetStringItem(pos, 5, self.table[row][6])
            self.list.SetStringItem(pos, 6, self.table[row][7])
            self.list.SetStringItem(pos, 7, self.table[row][8])
            self.list.SetStringItem(pos, 8, self.table[row][9])
        self.list.Show(True)

    # Upload file into program
    def browseSourceFile(self, evt): 
        wildcard = ("TIF source (*.tif)|*.tif|" 
                    "All files (*.*)|*.*")
        dialog = wx.FileDialog(None, "Choose a file", os.getcwd(), "", wildcard, wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.tif_path = dialog.GetPath()
            self.source_filePath_entry.SetValue(self.tif_path)

    def browseSaveFile(self, evt): 
        dialog = wx.DirDialog(None, "Choose a directory:",style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dialog.ShowModal() == wx.ID_OK:
            self.save_path = dialog.GetPath()
            self.save_filePath_entry.SetValue(self.save_path)

    def generateTMS(self, evt):
        if (self.tif_path == "") or (self.save_path == ""):
            wx.MessageBox("Please include both file path source file(.tif) and save file", "Invalid", 
            wx.OK | wx.ICON_ERROR)
        else:
            try:
                path = self.save_path.replace("\\","/").split("/")
                path_file = path[len(path)-1]
                TMS_link = "http://%s:%s/%s/{zoom}/{x}/{-y}.png" %(setting.TMSserver_hostIP, setting.TMSserver_hostPort, path_file)
                if not (self.database.isDuplicateTMS(TMS_link)):
                    generator = gdal.GenerateTiles(self.tif_path, self.save_path) # generate TMS tiles
                    generator.tilesGenerator()
                    file_location = self.save_path.replace("\\","/")
                    file_location += "/tilemapresource.xml"
                    content = self.getFileData(file_location)
                    content.append(str(TMS_link))
                    content.append(str(self.curUserName))
                    client = serverTMS.FtpClient(setting.TMSserver_hostIP , setting.TMSserver_hostName, setting.TMS_hostPassword)
                    client.placedirectory(self.save_path.replace("\\","/"))
                    self.database.saveTileData(content[7], content[0], content[2]
                        , content[3], content[4], content[5], content[1], content[8], content[6],"0")
                    wx.MessageBox("You have uploaded file to TMS server", "Successful", wx.OK | wx.ICON_INFORMATION)
                    self.list.Destroy()
                    self.createTable()
                else:
                    wx.MessageBox("The link already exist", "Duplicate file", wx.OK | wx.ICON_ERROR)
            except Exception as ex:
                template = "An exception of type {0} occured. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print message
                msg = "Can not upload file to server" 
                wx.MessageBox(msg, "Connection error", wx.OK | wx.ICON_ERROR)
                self.Destroy() # close LoginPage
                log.LoginPage(None, title="Sateltiles")  # open up login page

    def manageUser(self, evt):
        self.Destroy()
        manage.ManageUser(None, str(self.curUserName), title="Sateltiles")  # open up login page

    def getFileData(self, pathFile):
        content = []
        with open(pathFile, "r") as f:
            while (True):
                oneLine = f.readline()
                if oneLine == "":
                    break
                if "Title" in oneLine:
                    oneLine = oneLine.split(" ")
                    oneLine = oneLine[len(oneLine)-1].split("<Title>")
                    oneLine = oneLine[len(oneLine)-1].split("</Title>")
                    content.append(oneLine[0])
                elif "BoundingBox" in oneLine:
                    oneLine = oneLine.split(" ")
                    minLat = oneLine[7].split("minx=")
                    content.append(minLat[1][1:-1])
                    minLong = oneLine[8].split("miny=")
                    content.append(minLong[1][1:-1])
                    maxLat = oneLine[9].split("maxx=")
                    content.append(maxLat[1][1:-1])
                    maxLong = oneLine[10].split("maxy=")
                    content.append(maxLong[1][1:-4])
                elif "EPSG" in oneLine:
                    oneLine = oneLine.split(" ")
                    oneLine = oneLine[len(oneLine)-1].split("<SRS>")
                    oneLine = oneLine[len(oneLine)-1].split("</SRS>")
                    oneLine = oneLine[0].split("EPSG:")
                    content.append(oneLine[1])
        content.append(time.strftime("%d/%m/%Y"))
        f.close()
        return content
