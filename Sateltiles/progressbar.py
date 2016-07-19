import wx

class ProgressBar(wx.Frame):
   def __init__(self, parent, ID, title):
      super(ProgressBar, self).__init__(parent, title=title, size=(380,200)
            , style=wx.MINIMIZE_BOX| wx.SYSTEM_MENU | wx.CAPTION
            | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
      self.icon = wx.Icon("iconn.ico", wx.BITMAP_TYPE_ICO)
      self.SetIcon(self.icon)
      self.halfDone = False
      self.timer = wx.Timer(self, 1)
      self.count = 0
      self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
      panel = wx.Panel(self, -1)
      self.gauge = wx.Gauge(panel, -1, 100, size=(250, 25), pos=(70,60))

      self.count = 0
      self.Centre()
      self.Show(True)

   def OnStart(self, event):
      self.timer.Start(100)

   def OnTimer(self, event):
      if self.count >= 100:
         self.timer.Stop()
         self.text.SetLabel("Task Completed")
         self.btn1.Show(False)
      
   def changeValue(self,value):
      if value*0.5 < self.gauge.GetValue():
         self.halfDone = True
      if self.halfDone == False:
         self.gauge.SetValue(value*0.5)
      else:
         self.gauge.SetValue(50+(value*0.5))
      if self.gauge.GetValue() == 100:
         self.Destroy()
      self.count = value
      
