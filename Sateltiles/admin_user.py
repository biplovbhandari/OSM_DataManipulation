import wx
import os

from init import *
import login as log

class AdminUserPage(wx.Frame):
    def __init__(self, parent, title):
        super(AdminUserPage, self).__init__(parent, title=title, size=(600,520), style=wx.MINIMIZE_BOX| wx.SYSTEM_MENU | wx.CAPTION
                                        | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        wx.Frame.CenterOnScreen(self)
        panel = wx.Panel(self)
        self.icon = wx.Icon('iconn.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)

        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(25)
        existing_label = wx.StaticText(panel, pos=(20,20), label='Existing TMS')
        existing_label.SetFont(font)

        generate_label = wx.StaticText(panel, pos=(20,200+130), label='Generate TMS')
        generate_label.SetFont(font)

        source_filePath_label = wx.StaticText(panel, pos=(10,230+130), label='Source file (.tif) : ') 
        self.source_filePath_entry = wx.TextCtrl(panel, pos=(100,230+130), size=(165,20)) # sorce file path entries

        save_filePath_label = wx.StaticText(panel, pos=(20,260+130), label='Save location : ')
        self.save_filePath_entry = wx.TextCtrl(panel, pos=(100,260+130), size=(165,20)) # destination file path entries

        getLink_button = wx.Button(panel, label='GET TMS LINK', pos=(470,190+130), size=(100,40)) 
        getLink_button.Bind(wx.EVT_BUTTON, self.getTMS_Link)

        back_button = wx.Button(panel, label='BACK', pos=(10,310+130), size=(100,40)) #back home buttons
        back_button.Bind(wx.EVT_BUTTON, self.backHome)

        source_button = wx.Button(panel, label='Browse', pos=(280,227+130), size=(90,25)) 
        source_button.Bind(wx.EVT_BUTTON, self.browseSourceFile)

        save_button = wx.Button(panel, label='Browse', pos=(280,257+130), size=(90,25)) 
        save_button.Bind(wx.EVT_BUTTON, self.browseSaveFile)

        generate_button = wx.Button(panel, label='GENERATE', pos=(175,285+130), size=(90,30)) 
        generate_button.Bind(wx.EVT_BUTTON, self.generateTMS)

        id=wx.NewId()
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
        

        self.list.InsertColumn(0,"Min lat")
        self.list.InsertColumn(1,"Max lat")
        self.list.InsertColumn(2,"Min long")
        self.list.InsertColumn(3,"Max long")
        self.list.InsertColumn(4,"EPSG")
        self.list.InsertColumn(5,"Create by")
        self.list.InsertColumn(6,"Create on")
        self.list.InsertColumn(7,"Hide")


        for i in range(100):
            pos = self.list.InsertStringItem(i,"80") # 0 will insert at the start of the list
            self.list.SetStringItem(pos,1,"26.45") # add values in the other columns on the same row
            self.list.SetStringItem(pos,2,"88.183333")
            self.list.SetStringItem(pos,3,"30.45")
            self.list.SetStringItem(pos,4,"900913")
            self.list.SetStringItem(pos,5,"Jimmy")
            self.list.SetStringItem(pos,6,"28-06-2016")
            self.list.SetStringItem(pos,7,"0")

        self.tif_path = ""
        self.save_path = ""
    
        self.list.Show(True)
        self.Show(True)

    def backHome(self, evt):
        self.Destroy() # close LoginPage
        log.LoginPage(None, title='LoginPage')  #open up login page

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
            wx.MessageBox('Please include both file path source file(.tif) and save file', 'Invalid', 
            wx.OK | wx.ICON_ERROR)
        else:
            print ("Generating TMS from file in \'" + self.tif_path + "\' to folder \'" + self.save_path + "\'")
            





















                
