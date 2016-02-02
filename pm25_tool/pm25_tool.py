#!/usr/bin/env python
#-*-coding:utf-8-*- 
import wx
import os
from pm25_status import StatusSizer
from pm25_command import CommandSizer
from pm25_usart import UsartSizer

class HKFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, u"PM2.5 Tool", 
                style=wx.DEFAULT_FRAME_STYLE, size=(820, 640))
        panel = wx.Panel(self, size=(820, 640))
        panel.SetBackgroundColour("Aquamarine")
        icon = wx.Icon("resource"+os.sep+"hk.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)
        sizer = wx.BoxSizer(wx.VERTICAL)
        status = StatusSizer(panel)
        command = CommandSizer(panel)
        usart = UsartSizer(panel)
        sizer.Add(status, 0, wx.ALL, 5)
        sizer.Add(command, 0, wx.ALL, 5)
        sizer.Add(usart, 0, wx.ALL, 5)
        self.SetMaxSize((820, 640))
        self.SetSizer(sizer)
        sizer.Fit(panel)
        #self.Fit()



if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = HKFrame()
    frame.Show()
    app.MainLoop()

