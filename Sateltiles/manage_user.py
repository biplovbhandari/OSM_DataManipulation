import wx
import database_api as db
import login as log

class ManageUser(wx.Frame):
    def __init__(self, parent, title):
        super(ManageUser, self).__init__(parent, title=title, size=(600,400), style=wx.MINIMIZE_BOX| wx.SYSTEM_MENU | wx.CAPTION
                                        | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        wx.Frame.CenterOnScreen(self)
        self.panel = wx.Panel(self)
        self.icon = wx.Icon("iconn.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)

        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(25)
        existing_label = wx.StaticText(self.panel, pos=(20,20), label="Waiting list")
        existing_label.SetFont(font)

        back_button = wx.Button(self.panel, label="BACK", pos=(20,190+130), size=(100,40)) # back home buttons
        back_button.Bind(wx.EVT_BUTTON, self.backHome)

        ok_button = wx.Button(self.panel, label="OK", pos=(470,190+130), size=(100,40)) # back home buttons
        ok_button.Bind(wx.EVT_BUTTON, self.submit)

        self.approved = wx.RadioButton(self.panel,12, label = "Approve", pos = (150,210+130), style = wx.RB_GROUP)
        self.rejected = wx.RadioButton(self.panel,12, label = "Reject", pos = (240,210+130), style = wx.RB_GROUP)
        self.approved_all = wx.RadioButton(self.panel,12, label = "Approve all", pos = (150,190+130), style = wx.RB_GROUP)
        self.rejected_all = wx.RadioButton(self.panel,12, label = "Reject all", pos = (240,190+130), style = wx.RB_GROUP)
        self.set_admin = wx.RadioButton(self.panel,12, label = "Admin", pos = (320,210+130), style = wx.RB_GROUP)
        self.set_user = wx.RadioButton(self.panel,12, label = "Normal user", pos = (380,210+130), style = wx.RB_GROUP)
        self.approved.SetValue(True)
        self.rejected.SetValue(False)
        self.approved_all.SetValue(False)
        self.rejected_all.SetValue(False)
        self.set_admin.SetValue(False)
        self.set_user.SetValue(True)
        self.Bind(wx.EVT_RADIOBUTTON, self.OnRadiogroup)

        self.ap = True
        self.ap_all = False
        self.rj = False
        self.rj_all = False
        self.admin = False
        self.norm_user = True
        
        self.createTable()

        
        self.tif_path = ""
        self.save_path = ""
    
        self.Show(True)


    def createTable(self):
        self.list = wx.ListCtrl(self.panel,pos=(20,0+50), size=(550,260), style=wx.LC_REPORT 
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
        self.list.InsertColumn(0,"Username", width = 150)
        self.list.InsertColumn(1,"First name", width = 150)
        self.list.InsertColumn(2,"Last name", width = 150)
        self.list.InsertColumn(3,"Email", width = 200)

        # database admin/information
        database_name = "gdal2tiles"
        database_username = "postgres"
        database_password = "polpol01"
        database_host = "203.159.29.196"
        database_port = "5432"
        try:
            self.database = db.PostGresAPI(database_name, database_username, database_password, database_host, database_port) # connect to main database
        except:
            print("Can not connect to database (" + str(database_host) + ":" + str(database_port))

        amount_of_users = self.database.countUnknown() # get amount of user who are not approved yet by super admin
        userData = self.database.getUnknown()

        for i in range(amount_of_users):
            pos = self.list.InsertStringItem(i,userData[i][0]) # 0 will insert at the start of the list
            self.list.SetStringItem(pos,1,userData[i][3])
            self.list.SetStringItem(pos,2,userData[i][4]) # add values in the other columns on the same row
            self.list.SetStringItem(pos,3,userData[i][2])
            
        self.list.Show(True)
    
    def OnRadiogroup(self, e): 
        rb = e.GetEventObject()

        if rb.GetLabel() == "Approve":
            self.ap = True
            self.ap_all = False
            self.rj = False
            self.rj_all = False
            self.rejected.SetValue(False)
            self.rejected_all.SetValue(False)
            self.approved_all.SetValue(False)

        elif rb.GetLabel() == "Reject":
            self.ap = False
            self.ap_all = False
            self.rj = True
            self.rj_all = False
            self.approved.SetValue(False)
            self.approved_all.SetValue(False)
            self.rejected_all.SetValue(False)
        elif rb.GetLabel() == "Approve all":
            self.ap = False
            self.ap_all = True
            self.rj = False
            self.rj_all = False
            self.rejected.SetValue(False)
            self.rejected_all.SetValue(False)
            self.approved.SetValue(False)
        elif rb.GetLabel() == "Reject all":
            self.ap = False
            self.ap_all = False
            self.rj = False
            self.rj_all = True
            self.approved.SetValue(False)
            self.approved_all.SetValue(False)
            self.rejected.SetValue(False)
        elif rb.GetLabel() == "Admin":
            self.admin = True
            self.norm_user = False
            self.set_user.SetValue(False)
        elif rb.GetLabel() == "Normal user":
            self.admin = False
            self.norm_user = True
            self.set_admin.SetValue(False)
    
    def backHome(self, evt):
        self.Destroy() # close LoginPage
        log.LoginPage(None, title="LoginPage")  # open up login page


    def submit(self, evt):
        count = self.list.GetItemCount()
        item_data = []
        for row in range(count):
            if self.list.IsSelected(row): # get selected item data
                for k in range(self.list.GetColumnCount()):
                    item = self.list.GetItem(itemId=row, col=k) # add item element in item_data list
                    item_data.append(item.GetText())
                break
            
        if self.ap == True and item_data != "":            
            if self.admin == True:
                self.database.changeRole(item_data[0] ,"admin")
            elif self.norm_user == True:
                self.database.changeRole(item_data[0] ,"normal")
                
        elif self.rj == True and item_data != "":
            self.database.changeRole(item_data[0] ,"ban")
            
        elif self.ap_all == True and item_data != "": # approve all
            for l in range(count):
                element = self.list.GetItem(itemId=l, col=0)
                if self.admin == True:
                    self.database.changeRole(element.GetText() ,"admin")
                elif self.norm_user == True:
                    self.database.changeRole(element.GetText() ,"normal")
        elif self.rj_all == True and item_data != "": # reject all
            for l in range(count):
                element = self.list.GetItem(itemId=l, col=0)
                self.database.changeRole(element.GetText() ,"ban")

        self.list.Destroy()
        self.createTable()
            

##if __name__ == "__main__":
##    app = wx.App()
##    ManageUser(None, "Sateltiles")
##    app.MainLoop()
