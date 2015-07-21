#-*-coding:utf-8-*-
import wx

class ConvertPattern(wx.BoxSizer):
    def __init__(self, panel, boxName, leftName, rightName):
        wx.BoxSizer.__init__(self, wx.VERTICAL)
        box = wx.StaticBox(panel, -1, boxName, size=(800, 50))
        bsizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)

        leftText = wx.StaticText(panel, -1, leftName)
        self.leftEdit = wx.TextCtrl(panel, -1, "-", style=wx.TE_CENTER)

        convert = wx.Button(panel, -1, "convert")

        rightText = wx.StaticText(panel, -1, rightName)
        self.rightOutput = wx.TextCtrl(panel, -1, "---", style=wx.TE_CENTER|wx.TE_READONLY)
        self.rightOutput.SetMaxLength(8)

        gs1 = wx.FlexGridSizer(2, 1, 5, 5)
        gs1.AddMany([(leftText, 0, wx.ALIGN_CENTER),
                (self.leftEdit, 0, wx.EXPAND|wx.ALL)])
        gs2 = wx.FlexGridSizer(2, 1, 5, 5)
        gs2.AddMany([(rightText, 0, wx.ALIGN_CENTER),
                (self.rightOutput, 0, wx.EXPAND|wx.ALL)])

        bsizer.Add(gs1, 0, wx.ALL, 10)
        bsizer.Add(convert, 0, wx.ALIGN_CENTER|wx.ALL, 10)
        bsizer.Add(gs2, 0, wx.ALL, 10)
        self.Add(bsizer, 0, wx.ALL, 10)
        convert.Bind(wx.EVT_BUTTON, self.OnClickConvert, convert)
        
    def OnClickConvert(self, event):
        self.rightOutput.Clear();
        self.rightOutput.WriteText(str(self.Calculate()))

    def Calculate(self):
        return "None!"

