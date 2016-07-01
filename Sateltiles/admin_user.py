import wx
import os
from init import *
import login as log
import manage_user as manage
import database_api as db

class AdminUserPage(wx.Frame):
    def __init__(self, parent, role, title):
        super(AdminUserPage, self).__init__(parent, title=title, size=(600,520), style=wx.MINIMIZE_BOX| wx.SYSTEM_MENU | wx.CAPTION
                                        | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        wx.Frame.CenterOnScreen(self)
        panel = wx.Panel(self)
        self.icon = wx.Icon("iconn.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)

        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(25)
        existing_label = wx.StaticText(panel, pos=(20,20), label="Existing TMS")
        existing_label.SetFont(font)

        generate_label = wx.StaticText(panel, pos=(20,200+130), label="Generate TMS")
        generate_label.SetFont(font)

        source_filePath_label = wx.StaticText(panel, pos=(10,230+130), label="Source file (.tif) : ") 
        self.source_filePath_entry = wx.TextCtrl(panel, pos=(100,230+130), size=(165,20)) # sorce file path entries

        save_filePath_label = wx.StaticText(panel, pos=(20,260+130), label="Save location : ")
        self.save_filePath_entry = wx.TextCtrl(panel, pos=(100,260+130), size=(165,20)) # destination file path entries

        getLink_button = wx.Button(panel, label="GET TMS LINK", pos=(470,190+130), size=(100,40)) 
        getLink_button.Bind(wx.EVT_BUTTON, self.getTMS_Link)

        back_button = wx.Button(panel, label="BACK", pos=(10,310+130), size=(100,40)) # back home buttons
        back_button.Bind(wx.EVT_BUTTON, self.backHome)

        source_button = wx.Button(panel, label="Browse", pos=(280,227+130), size=(90,25)) 
        source_button.Bind(wx.EVT_BUTTON, self.browseSourceFile)

        save_button = wx.Button(panel, label="Browse", pos=(280,257+130), size=(90,25)) 
        save_button.Bind(wx.EVT_BUTTON, self.browseSaveFile)

        generate_button = wx.Button(panel, label="GENERATE", pos=(175,285+130), size=(90,30)) 
        generate_button.Bind(wx.EVT_BUTTON, self.generateTMS)

        manage_button = wx.Button(panel, label="Manage user", pos=(470,310+130), size=(100,40)) 
        manage_button.Bind(wx.EVT_BUTTON, self.manageUser)

        # database admin/information
        database_name = "gdal2tiles"
        database_username = "postgres"
        database_password = "polpol01"
        database_host = "203.159.29.196"
        database_port = "5432"
        try:
            database = db.PostGresAPI(database_name, database_username, database_password, database_host, database_port) # connect to main database
        except:
            print("Can not connect to database (" + str(database_host) + ":" + str(database_port))

        if role != "superadmin":  # only super admin can see this button
            manage_button.Show(False)
        
        self.list = wx.ListCtrl(panel,pos=(20,0+50), size=(550,260), style=wx.LC_REPORT 
                                 | wx.BORDER_SUNKEN
                                 #| wx.BORDER_NONE         <<< This is up to your style uncomment # to enable
                                 #| wx.LC_EDIT_LABELS
                                 #| wx.LC_SORT_ASCENDING
                                 #| wx.LC_NO_HEADER
                                 #| wx.LC_VRULES
                                 #| wx.LC_HRULES
                                 #| wx.LC_SINGLE_SEL
                                  )
        
        # Insert column
        self.list.InsertColumn(0,"Name")
        self.list.InsertColumn(1,"Min lat")
        self.list.InsertColumn(2,"Max lat")
        self.list.InsertColumn(3,"Min long")
        self.list.InsertColumn(4,"Max long")
        self.list.InsertColumn(5,"EPSG")
        self.list.InsertColumn(6,"Create by")
        self.list.InsertColumn(7,"Create on")
        self.list.InsertColumn(8,"Hide")
        
        table = database.getTileData()

        for row in range(len(table)):
            pos = self.list.InsertStringItem(row, table[row][1])
            self.list.SetStringItem(pos, 1, table[row][2])
            self.list.SetStringItem(pos, 2, table[row][4])
            self.list.SetStringItem(pos, 3, table[row][3])
            self.list.SetStringItem(pos, 4, table[row][5])
            self.list.SetStringItem(pos, 5, table[row][6])
            self.list.SetStringItem(pos, 6, table[row][7])
            self.list.SetStringItem(pos, 7, table[row][8])
            self.list.SetStringItem(pos, 8, table[row][9])
            

        self.tif_path = ""
        self.save_path = ""
    
        self.list.Show(True)
        self.Show(True)

    def backHome(self, evt):
        self.Destroy() # close LoginPage
        log.LoginPage(None, title="LoginPage")  # open up login page

    def getTMS_Link(self, evt):
        count = self.list.GetItemCount()
        item_data = []
        for row in range(count):
            if self.list.IsSelected(row): # get selected item data
                print ("You have selected item " + str(row+1))
                for k in range(self.list.GetColumnCount()):
                    item = self.list.GetItem(itemId=row, col=k) # add item element in item_data list
                    item_data.append(item.GetText())
##                print (item_data)
##                info = wx.AboutDialogInfo()
##                info.SetName('TMS link')
##                info.SetWebSite('www.google.com.au')
##                wx.AboutBox(info)
                break

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
            print ("Generating TMS from file in \'" + self.tif_path + "\' to folder \'" + self.save_path + "\'")

    def manageUser(self, evt):
        manage.ManageUser(None, title="ManageUserPage")  # open up login page
        

            
