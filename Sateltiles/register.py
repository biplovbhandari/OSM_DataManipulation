import wx
import re
import login as log
import admin_email as adminEmail
import database_api as db

class RegisterPage(wx.Frame):
    def __init__(self, parent, title):
        super(RegisterPage, self).__init__(parent, title=title, size=(400,320), style=wx.MINIMIZE_BOX| wx.SYSTEM_MENU | wx.CAPTION
                                        | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        wx.Frame.CenterOnScreen(self)
        panel = wx.Panel(self)
        self.icon = wx.Icon("iconn.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)

        home_button = wx.Button(panel, label="BACK", pos=(20,110+130), size=(70,40)) # back home buttons
        home_button.Bind(wx.EVT_BUTTON, self.backHome)

        validation_button = wx.Button(panel, label="REGISTER", pos=(310,110+130), size=(70,40)) # check registration buttons
        validation_button.Bind(wx.EVT_BUTTON, self.checkValidation)

        wx.StaticText(panel, pos=(72,0+50), label="First name :") # All the labels
        wx.StaticText(panel, pos=(60,30+50), label="Family name :")
        wx.StaticText(panel, pos=(75,60+50), label="Username :")
        wx.StaticText(panel, pos=(78,90+50), label="Password :")
        wx.StaticText(panel, pos=(30,120+50), label="Re-enter password :")
        wx.StaticText(panel, pos=(99,150+50), label="Email :")

        self.firstName_entry = wx.TextCtrl(panel, pos=(136,0+50), size=(170,20))  # All the entries
        self.familyName_entry = wx.TextCtrl(panel, pos=(136,30+50), size=(170,20))  
        self.userName_entry = wx.TextCtrl(panel, pos=(136,60+50), size=(170,20))  
        self.password_entry = wx.TextCtrl(panel, pos=(136,90+50), size=(170,20),style=wx.TE_PASSWORD)  
        self.re_password_entry = wx.TextCtrl(panel, pos=(136,120+50), size=(170,20),style=wx.TE_PASSWORD)  
        self.email_entry = wx.TextCtrl(panel, pos=(136,150+50), size=(170,20)) 
        
        self.Show(True)

    def backHome(self, evt):
        self.Destroy() # close LoginPage
        log.LoginPage(None, title="LoginPage")  # open up login page

    def checkValidation(self, evt):
        database_name = "gdal2tiles"
        database_username = "postgres"
        database_password = "polpol01"
        database_host = "203.159.29.196"
        database_port = "5432"
        try:
            database = db.PostGresAPI(database_name, database_username, database_password, database_host, database_port) # connect to main database
        except:
            print("Can not connect to database (" + str(database_host) + ":" + str(database_port))

        # valify email syntax
        addressToVerify = self.email_entry.GetValue()
        match = re.match("^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$", addressToVerify)
        if match == None:
            wx.MessageBox("Invalid email address, please try another email address", "Error", 
            wx.OK | wx.ICON_ERROR)
        elif self.password_entry.GetValue() != self.re_password_entry.GetValue(): # check if password match re-type password
            wx.MessageBox("Mismatch password, please enter re-enter password correctly", "Error", 
            wx.OK | wx.ICON_ERROR)
        elif not(database.isRegisterValid(self.userName_entry.GetValue())):  # valify duplicate username
            wx.MessageBox("Taken username, please try another username", "Error", 
            wx.OK | wx.ICON_ERROR)
        else:
            database.saveAccountData(self.userName_entry.GetValue(), self.password_entry.GetValue()
                                     , self.email_entry.GetValue(), self.firstName_entry.GetValue()
                                     , self.familyName_entry.GetValue(), "unknown")
            emailSystem = adminEmail.Email()
            super_admin_email = "horizonte-1233@hotmail.com"
            super_admin_firstname = "Solo"
            super_admin_lastname = "Horizonte"
            emailSystem.sendComfirmation(super_admin_email, super_admin_firstname, super_admin_lastname)
            wx.MessageBox("Confirmation email have been sent. Your account have to be approved by admin before you can login.", "Wait for approval", 
            wx.OK | wx.ICON_INFORMATION)
            self.Destroy() # close LoginPage
            log.LoginPage(None, title="LoginPage")  # open up login page
