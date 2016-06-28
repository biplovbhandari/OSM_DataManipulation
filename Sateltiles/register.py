import wx

import login as log


class RegisterPage(wx.Frame):
    def __init__(self, parent, title):
        super(RegisterPage, self).__init__(parent, title=title, size=(400,320), style=wx.MINIMIZE_BOX| wx.SYSTEM_MENU | wx.CAPTION
                                        | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        wx.Frame.CenterOnScreen(self)
        panel = wx.Panel(self)
        self.icon = wx.Icon('iconn.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)

        home_button = wx.Button(panel, label='BACK', pos=(20,110+130), size=(70,40)) #back home buttons
        home_button.Bind(wx.EVT_BUTTON, self.backHome)

        validation_button = wx.Button(panel, label='REGISTER', pos=(310,110+130), size=(70,40)) #check registration buttons
        validation_button.Bind(wx.EVT_BUTTON, self.checkValidation)

        wx.StaticText(panel, pos=(72,0+50), label='First name :') # All the labels
        wx.StaticText(panel, pos=(60,30+50), label='Family name :')
        wx.StaticText(panel, pos=(75,60+50), label='Username :')
        wx.StaticText(panel, pos=(78,90+50), label='Password :')
        wx.StaticText(panel, pos=(30,120+50), label='Re-enter password :')
        wx.StaticText(panel, pos=(99,150+50), label='Email :')

        self.firstName_entry = wx.TextCtrl(panel, pos=(136,0+50), size=(170,20))  # All the entries
        self.familyName_entry = wx.TextCtrl(panel, pos=(136,30+50), size=(170,20))  
        self.userName_entry = wx.TextCtrl(panel, pos=(136,60+50), size=(170,20))  
        self.password_entry = wx.TextCtrl(panel, pos=(136,90+50), size=(170,20),style=wx.TE_PASSWORD)  
        self.re_password_entry = wx.TextCtrl(panel, pos=(136,120+50), size=(170,20),style=wx.TE_PASSWORD)  
        self.email_entry = wx.TextCtrl(panel, pos=(136,150+50), size=(170,20)) 
        
        self.Show(True)

    def backHome(self, evt):
        self.Destroy() # close LoginPage
        
        log.LoginPage(None, title='LoginPage')  #open up login page

    def checkValidation(self, evt):
        print "Check validation.."
        wx.MessageBox('Please use only letter', 'Invalid', 
        wx.OK | wx.ICON_ERROR)
