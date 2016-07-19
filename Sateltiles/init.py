import wx
import login as start

if __name__ == "__main__":
    app = wx.App()
    start.LoginPage(None, "Sateltiles")
    app.MainLoop()
