#-*-coding:utf-8-*- 
import wx

class StatusSizer(wx.GridSizer):
    def __init__(self, panel):
        wx.GridSizer.__init__(self, rows=1, cols=5, hgap=10)

        s1 = StatusItem(panel, u"模式", u"电压")
        s2 = StatusItem(panel, "PPM", "0")
        s3 = StatusItem(panel, u"电压输出", "0")
        s4 = StatusItem(panel, u"AD采样值", "0")
        s5 = StatusItem(panel, u"标定值", "0")

        self.Add(s1, 0, wx.EXPAND|wx.ALL)
        self.Add(s2, 0, wx.EXPAND|wx.ALL)
        self.Add(s3, 0, wx.EXPAND|wx.ALL)
        self.Add(s4, 0, wx.EXPAND|wx.ALL)
        self.Add(s5, 0, wx.EXPAND|wx.ALL)
        panel.status_mode = s1
        panel.status_ppm = s2
        panel.status_voltage = s3
        panel.status_adc = s4
        panel.status_calibrate = s5
        self.SetMinSize((800, 50))
        self.Fit(panel)


class StatusItem(wx.BoxSizer):
    def __init__(self, panel, label, text):
        wx.BoxSizer.__init__(self, wx.VERTICAL)
        l = wx.StaticText(panel, -1, label, 
                size=(-1, 30), style=wx.ALIGN_CENTER)
        font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        l.SetFont(font)
        self.t = wx.TextCtrl(panel, -1, text, 
                size=(-1, 30), style=wx.TE_CENTER|wx.TE_READONLY)
        self.t.SetFont(font)
        self.Add(l, 0, wx.ALIGN_CENTER)
        self.Add(self.t, 0, wx.ALIGN_CENTER)

    def set_value(self, value):
        self.t.SetValue(value)
    def get_value(self):
        return int(self.t.GetValue())

