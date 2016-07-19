import wx
import register as regis
import getPassword as getPass
import admin_user as admin
import normal_user as norm
import database_api as db
import settings as setting

class LoginPage(wx.Frame):
    def __init__(self, parent, title):
        super(LoginPage, self).__init__(parent, title=title, size=(400,320)
            , style=wx.MINIMIZE_BOX| wx.SYSTEM_MENU | wx.CAPTION
            | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        wx.Frame.CenterOnScreen(self)
        panel = wx.Panel(self)
        self.icon = wx.Icon("iconn.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)
        self.userName_entry = wx.TextCtrl(panel, pos=(35+80,20+100), size=(155,20))  # entries
        self.password_entry = wx.TextCtrl(panel, pos=(35+80,50+100), size=(155,20),style=wx.TE_PASSWORD)
        wx.StaticText(panel, pos=(45,20+100), label="Username :")
        wx.StaticText(panel, pos=(50,50+100), label="Password :")
        login_button = wx.Button(panel, label="Login", pos=(280,0+115), size=(60,60))
        register_button = wx.Button(panel, label="Register", pos=(35+80,80+100), size=(50,25))
        forgot_password_button = wx.Button(panel, label="Forgot password?", pos=(90+80,80+100), size=(100,25))
        login_button.Bind(wx.EVT_BUTTON, self.checkValidation) # all the button commands
        register_button.Bind(wx.EVT_BUTTON, self.register)
        forgot_password_button.Bind(wx.EVT_BUTTON, self.getPassword)
        self.Show(True)
        
    def checkValidation(self, evt):
        try:
            database = db.PostGresAPI(setting.database_name, setting.database_username
                , setting.database_password, setting.database_host
                , setting.database_port) # connect to main database
        except:
            database = None
            msg = "Can not connect to database (%s:%s)" %(setting.database_host, setting.database_port)
            wx.MessageBox(msg, "Connection error", wx.OK | wx.ICON_ERROR)
            self.Destroy() # close LoginPage
            LoginPage(None, title="Sateltiles")  # open up login page
        if (self.userName_entry.GetValue() == "") and (self.password_entry.GetValue() == ""):
            wx.MessageBox("Please enter username and password", "Invalid", 
            wx.OK | wx.ICON_ERROR)
        elif (self.userName_entry.GetValue() == "") and not(self.password_entry.GetValue() == ""):
            wx.MessageBox("Please enter username", "Invalid", 
            wx.OK | wx.ICON_ERROR)
        elif not(self.userName_entry.GetValue() == "") and (self.password_entry.GetValue() == ""):
            wx.MessageBox("Please enter password", "Invalid", 
            wx.OK | wx.ICON_ERROR)
        elif database != None:  
            if database.isLoginValid(self.userName_entry.GetValue(), self.password_entry.GetValue()) == "Invalid_username":
                wx.MessageBox("Invalid username", "Invalid", 
                wx.OK | wx.ICON_ERROR)
            elif database.isLoginValid(self.userName_entry.GetValue(), self.password_entry.GetValue()) == "Invalid_password":
                wx.MessageBox("Invalid password", "Invalid", 
                wx.OK | wx.ICON_ERROR)
            elif database.isLoginValid(self.userName_entry.GetValue(), self.password_entry.GetValue()) == "Valid":
                self.Destroy() # close LoginPage
                role = database.checkRole(self.userName_entry.GetValue())
                if role == "admin" or role == "superadmin":
                    # admin user
                    admin.AdminUserPage(None, role, self.userName_entry.GetValue(), "Sateltiles")
                elif role == "normal":
                    # normal user
                    norm.NormalUserPage(None, title="Sateltiles")
                elif role == "unknown":
                    # can't login
                    wx.MessageBox("Your account has to be approved by admin before you can login.", "Wait for approval", 
                    wx.OK | wx.ICON_ERROR)
                elif role == "ban":
                    wx.MessageBox("Your account has been rejected by admin.", "Baned account", 
                    wx.OK | wx.ICON_ERROR)

    def register(self, evt):
        self.Destroy() # close LoginPage
        regis.RegisterPage(None, title="Sateltiles")  # open up register page

    def getPassword(self, evt):
        self.Destroy() # close LoginPage
        getPass.GetPasswordPage(None, title="Sateltiles")  # open up getPasswordPage
