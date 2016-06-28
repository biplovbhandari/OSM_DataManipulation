import wx

import login as log

class GetPasswordPage(wx.Frame):
    def __init__(self, parent, title):
        super(GetPasswordPage, self).__init__(parent, title=title, size=(400,320), style=wx.MINIMIZE_BOX| wx.SYSTEM_MENU | wx.CAPTION
                                        | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        wx.Frame.CenterOnScreen(self)
        panel = wx.Panel(self)
        self.icon = wx.Icon('iconn.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)

        home_button = wx.Button(panel, label='BACK', pos=(20,110+130), size=(70,40)) #back home buttons
        home_button.Bind(wx.EVT_BUTTON, self.backHome)

        home_button = wx.Button(panel, label='OK', pos=(170,50+130), size=(70,40)) #back home buttons
        home_button.Bind(wx.EVT_BUTTON, self.retrievePassword)


        wx.StaticText(panel, pos=(50,40+50), label='Username :') # All the labels
        wx.StaticText(panel, pos=(195,70+50), label='OR') # All the labels
        wx.StaticText(panel, pos=(75,95+50), label='Email :') # All the labels

        self.userName_entry = wx.TextCtrl(panel, pos=(120,40+50), size=(170,20))  # All the entries
        self.email_entry = wx.TextCtrl(panel, pos=(120,95+50), size=(170,20))

        
        self.Show(True)

    def backHome(self, evt):
        self.Destroy() # close LoginPage
        log.LoginPage(None, title='LoginPage')  #open up login page

    def retrievePassword(self, evt):
        if (self.userName_entry.GetValue() == '') and (self.email_entry.GetValue() == ''):
            wx.MessageBox('Please enter username or email', 'Invalid', 
            wx.OK | wx.ICON_ERROR)
        else:
            print "11111"
