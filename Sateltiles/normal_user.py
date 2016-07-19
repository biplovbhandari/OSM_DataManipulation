import wx
import os
from init import *
import login as log
import settings as setting
import database_api as db

class NormalUserPage(wx.Frame):
    def __init__(self, parent, title):
        super(NormalUserPage, self).__init__(parent, title=title, size=(600,400)
            , style=wx.MINIMIZE_BOX| wx.SYSTEM_MENU | wx.CAPTION
            | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        wx.Frame.CenterOnScreen(self)
        panel = wx.Panel(self)
        self.icon = wx.Icon("iconn.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)
        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(25)
        existing_label = wx.StaticText(panel, pos=(20,20), label="Existing TMS")
        existing_label.SetFont(font)
        getLink_button = wx.Button(panel, label="GET TMS LINK", pos=(470,190+130), size=(100,40)) 
        getLink_button.Bind(wx.EVT_BUTTON, self.getTMS_Link)
        back_button = wx.Button(panel, label="BACK", pos=(20,190+130), size=(100,40)) # back home buttons
        back_button.Bind(wx.EVT_BUTTON, self.backHome)
        self.list = wx.ListCtrl(panel,pos=(20,0+50), size=(550,260), style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        colName = ["Name", "Min lat", "Max lat", "Min long", "Max long", "EPSG", "Create by", "Create on"]
        # Insert column
        for i in range(8):
            self.list.InsertColumn(i,colName[i])
        try:
            database = db.PostGresAPI(setting.database_name, setting.database_username
                , setting.database_password, setting.database_host, setting.database_port) # connect to main database
            self.table = database.getTileData()
            for row in range(len(self.table)):
                if self.table[row][9] == "1": # hide = 1 (don't show to normal user)
                    continue
                pos = self.list.InsertStringItem(row, self.table[row][1])
                self.list.SetStringItem(pos, 1, self.table[row][2])
                self.list.SetStringItem(pos, 2, self.table[row][4])
                self.list.SetStringItem(pos, 3, self.table[row][3])
                self.list.SetStringItem(pos, 4, self.table[row][5])
                self.list.SetStringItem(pos, 5, self.table[row][6])
                self.list.SetStringItem(pos, 6, self.table[row][7])
                self.list.SetStringItem(pos, 7, self.table[row][8])
            self.tif_path = ""
            self.save_path = ""
            self.list.Show(True)
            self.Show(True)
        except:
            msg = "Can not connect to database (%s:%s)" %(setting.database_host, setting.database_port)
            wx.MessageBox(msg, "Connection error", wx.OK | wx.ICON_ERROR)
            self.Destroy() # close LoginPage
            log.LoginPage(None, title="Sateltiles")  # open up login page

    def backHome(self, evt):
        self.Destroy() # close LoginPage
        log.LoginPage(None, title="Sateltiles")  # open up login page

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
