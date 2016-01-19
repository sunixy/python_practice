#!/usr/bin/env python
#-*-coding:utf-8-*-

import wx
from toolbook import *


class HkFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, u"公式换算器",
                style=wx.DEFAULT_FRAME_STYLE)
        self.SetSize((900, 600))
        self.tb = MyToolbook(self)

if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = HkFrame()
    frame.Show()
    app.MainLoop()

