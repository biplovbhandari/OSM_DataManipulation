import wx
import os
from init import *
import login as log

class NormalUserPage(wx.Frame):
    def __init__(self, parent, title):
        super(NormalUserPage, self).__init__(parent, title=title, size=(600,400), style=wx.MINIMIZE_BOX| wx.SYSTEM_MENU | wx.CAPTION
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

        for i in range(100):
            pos = self.list.InsertStringItem(i,"Bangkok") # 0 will insert at the start of the list
            self.list.SetStringItem(pos,1,"80")
            self.list.SetStringItem(pos,2,"26.45") # add values in the other columns on the same row
            self.list.SetStringItem(pos,3,"88.183333")
            self.list.SetStringItem(pos,4,"30.45")
            self.list.SetStringItem(pos,5,"900913")
            self.list.SetStringItem(pos,6,"Jimmy")
            self.list.SetStringItem(pos,7,"28-06-2016")
            self.list.SetStringItem(pos,8,"0")

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
                print (item_data)
                info = wx.AboutDialogInfo()
                info.SetName("TMS link")
                info.SetWebSite("www.google.com.au")
                wx.AboutBox(info)
                break
