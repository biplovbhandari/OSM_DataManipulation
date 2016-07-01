import wx
import admin_email as adminEmail
import login as log
import database_api as db

class GetPasswordPage(wx.Frame):
    def __init__(self, parent, title):
        super(GetPasswordPage, self).__init__(parent, title=title, size=(400,320), style=wx.MINIMIZE_BOX| wx.SYSTEM_MENU | wx.CAPTION
                                        | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        wx.Frame.CenterOnScreen(self)
        panel = wx.Panel(self)
        self.icon = wx.Icon("iconn.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)

        home_button = wx.Button(panel, label="BACK", pos=(20,110+130), size=(70,40)) # all the buttons
        home_button.Bind(wx.EVT_BUTTON, self.backHome)
        home_button = wx.Button(panel, label="OK", pos=(170,50+130), size=(70,40))
        home_button.Bind(wx.EVT_BUTTON, self.retrievePassword)


        wx.StaticText(panel, pos=(50,40+50), label="Username :") # all the labels
        wx.StaticText(panel, pos=(195,70+50), label="AND") 
        wx.StaticText(panel, pos=(75,95+50), label="Email :") 

        self.userName_entry = wx.TextCtrl(panel, pos=(120,40+50), size=(170,20))  # all the entries
        self.email_entry = wx.TextCtrl(panel, pos=(120,95+50), size=(170,20))

        
        self.Show(True)

    def backHome(self, evt):
        self.Destroy() # close LoginPage
        log.LoginPage(None, title="LoginPage")  #open up login page

    def retrievePassword(self, evt):
        database_name = "gdal2tiles"
        database_username = "postgres"
        database_password = "polpol01"
        database_host = "203.159.29.196"
        database_port = "5432"
        try:
            database = db.PostGresAPI(database_name, database_username, database_password, database_host, database_port) # connect to main database
        except:
            print("Can not connect to database (" + str(database_host) + ":" + str(database_port))
            
        if (self.userName_entry.GetValue() == "") or (self.email_entry.GetValue() == ""):
            wx.MessageBox("Please enter username and email", "Invalid", 
            wx.OK | wx.ICON_ERROR)
        else:
            emailSystem = adminEmail.Email()
            userPassword = database.getPassword(self.userName_entry.GetValue(), self.email_entry.GetValue())
            userData = database.getUserData(self.userName_entry.GetValue())
            if userPassword == None or userData == None:
                wx.MessageBox("Incorrect username or email. Please try agian", "Error", 
                wx.OK | wx.ICON_ERROR)
            else:
                emailSystem.sendPassword(self.email_entry.GetValue(), userData[0], userData[1], userPassword) # send user password by email
                wx.MessageBox("Your password has been sent to your email. Please check your email.", "Successful", 
                wx.OK | wx.ICON_INFORMATION)
                
                self.Destroy() # close LoginPage
                log.LoginPage(None, title="LoginPage")  # open up login page
