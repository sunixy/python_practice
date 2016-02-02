#!/usr/bin/env python
#-*-coding:utf-8-*-

import wx
import os
import sys
from gas_status import StatusSizer
from gas_usart import UsartSizer

class RedirctText(object):
    def __init__(self, text):
        self.out = text

    def write(self, string):
        self.out.WriteText(string)


class HKFrame(wx.Frame):
    def __init__(self, title, bg_color):
        wx.Frame.__init__(self, None, -1, title, 
                style=wx.DEFAULT_FRAME_STYLE, size=(820, 640))
        panel = wx.Panel(self, size=(820, 640))
        panel.SetBackgroundColour(bg_color)
        icon = wx.Icon("resource"+os.sep+"hk.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)
        sizer = wx.BoxSizer(wx.VERTICAL)
        status = StatusSizer(panel)
        usart = UsartSizer(panel)
        sizer.Add(status, 0, wx.ALL|wx.EXPAND)
        sizer.Add(usart, 0, wx.ALL|wx.EXPAND)
        self.SetMaxSize((820, 640))
        self.SetSizer(sizer)
        #sizer.Fit(panel)
        self.Fit()

        redir = RedirctText(panel.log)
        sys.stdout = redir
        sys.stderr = redir

if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = HKFrame(u"Gas Tool", "Aquamarine")
    frame.Show()
    app.MainLoop()

