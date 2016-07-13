import wx

class ProgressTMS(wx.Frame):
   def __init__(self, parent, ID, title):
      super(ProgressTMS, self).__init__(parent, title=title, size=(380,200)
            , style=wx.MINIMIZE_BOX| wx.SYSTEM_MENU | wx.CAPTION
            | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
      self.icon = wx.Icon("iconn.ico", wx.BITMAP_TYPE_ICO)
      self.SetIcon(self.icon)
      self.halfDone = False
      self.timer = wx.Timer(self, 1)
      self.count = 0
      self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
      panel = wx.Panel(self, -1)
      font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
      font.SetPointSize(25)
      self.file_text = wx.StaticText(panel, -1, "", pos=(90,70))
      self.file_text.SetFont(font)
      self.count = 0
      self.Centre()
      self.Show(True)

   def OnStart(self, event):
      self.timer.Start(100)
      
   def OnTimer(self, event):
      if self.count >= 100:
         self.timer.Stop()
      
   def changeValue(self, value):
      self.file_text.SetLabel(value)

