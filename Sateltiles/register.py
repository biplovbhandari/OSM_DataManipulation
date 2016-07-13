import wx
import re
import settings
import login as log
import admin_email as adminEmail
import database_api as db
import settings as setting

class RegisterPage(wx.Frame):
    def __init__(self, parent, title):
        super(RegisterPage, self).__init__(parent, title=title, size=(400,320)
            , style=wx.MINIMIZE_BOX| wx.SYSTEM_MENU | wx.CAPTION
            | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        wx.Frame.CenterOnScreen(self)
        panel = wx.Panel(self)
        self.icon = wx.Icon("iconn.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)
        # all the buttons
        home_button = wx.Button(panel, label="BACK", pos=(20,110+130), size=(70,40)) 
        home_button.Bind(wx.EVT_BUTTON, self.backHome)
        validation_button = wx.Button(panel, label="REGISTER", pos=(310,110+130), size=(70,40)) 
        validation_button.Bind(wx.EVT_BUTTON, self.checkValidation)
        # all the labels
        wx.StaticText(panel, pos=(72,0+50), label="First name :") 
        wx.StaticText(panel, pos=(60,30+50), label="Family name :")
        wx.StaticText(panel, pos=(75,60+50), label="Username :")
        wx.StaticText(panel, pos=(78,90+50), label="Password :")
        wx.StaticText(panel, pos=(30,120+50), label="Re-enter password :")
        wx.StaticText(panel, pos=(99,150+50), label="Email :")
        # all the entries
        self.firstName_entry = wx.TextCtrl(panel, pos=(136,0+50), size=(170,20))  
        self.familyName_entry = wx.TextCtrl(panel, pos=(136,30+50), size=(170,20))  
        self.userName_entry = wx.TextCtrl(panel, pos=(136,60+50), size=(170,20))  
        self.password_entry = wx.TextCtrl(panel, pos=(136,90+50), size=(170,20),style=wx.TE_PASSWORD)  
        self.re_password_entry = wx.TextCtrl(panel, pos=(136,120+50), size=(170,20),style=wx.TE_PASSWORD)  
        self.email_entry = wx.TextCtrl(panel, pos=(136,150+50), size=(170,20)) 
        self.Show(True)

    def backHome(self, evt):
        self.Destroy() # close LoginPage
        log.LoginPage(None, title="Sateltiles")  # open up login page

    def checkValidation(self, evt):
        try:# try to connect to main database
            database = db.PostGresAPI(setting.database_name, setting.database_username
                , setting.database_password, setting.database_host, setting.database_port) 
        except:
            msg = "Can not connect to database (%s:%s)" %(setting.database_host, setting.database_port)
            wx.MessageBox(msg, "Connection error", wx.OK | wx.ICON_ERROR)
            self.Destroy() # close LoginPage
            log.LoginPage(None, title="Sateltiles")  # open up login page
        # valify email syntax
        addressToVerify = self.email_entry.GetValue()
        match = re.match("^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$", addressToVerify)
        if match == None:
            wx.MessageBox("Invalid email address, please try another email address", "Error", 
            wx.OK | wx.ICON_ERROR)
        # check if password match re-type password
        elif self.password_entry.GetValue() != self.re_password_entry.GetValue(): 
            wx.MessageBox("Mismatch password, please enter re-enter password correctly", "Error", 
            wx.OK | wx.ICON_ERROR)
        elif not(database.isRegisterValid(self.userName_entry.GetValue())):  # valify duplicate username
            wx.MessageBox("Taken username, please try another username", "Error", 
            wx.OK | wx.ICON_ERROR)
        else:
            database.saveAccountData(self.userName_entry.GetValue(), self.password_entry.GetValue()
                , self.email_entry.GetValue(), self.firstName_entry.GetValue()
                , self.familyName_entry.GetValue(), "unknown")
            try:
                emailSystem = adminEmail.Email()
                emailSystem.sendComfirmation(setting.super_admin_email, setting.super_admin_firstname
                    , setting.super_admin_lastname, self.firstName_entry.GetValue()
                    , self.familyName_entry.GetValue())
                wx.MessageBox("""Confirmation email have been sent. Your account have to be approved by
                                admin before you can login."""
                    , "Wait for approval", wx.OK | wx.ICON_INFORMATION)
            except:
                wx.MessageBox("Connection error."
                    , "Error", wx.OK | wx.ICON_ERROR)
            self.Destroy() # close LoginPage
            log.LoginPage(None, title="Sateltiles")  # open up login page
