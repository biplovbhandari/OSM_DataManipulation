import wx
import login as start
import admin_user as admin
import normal_user as norm

if __name__ == "__main__":
    app = wx.App()
    start.LoginPage(None, title="Sateltiles")
    app.MainLoop()
