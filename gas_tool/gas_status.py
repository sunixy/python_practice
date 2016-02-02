#!/usr/bin/env python
#-*-coding:utf-8-*-

import wx
import modbus_tk.defines as cst

class StatusSizer(wx.GridSizer):
    def __init__(self, panel):
        wx.GridSizer.__init__(self, rows=2, cols=4, hgap=10, vgap=10)
        s1 = StatusItem(panel, "sensor zero voltage", "0")
        s2 = StatusItem(panel, "sensor full voltage", "0")
        s3 = StatusItem(panel, "4~20mA zero voltage", "0")
        s4 = StatusItem(panel, "4~20mA full voltage", "0")
        s5 = StatusItem(panel, "LEL", "0")
        s6 = StatusItem(panel, "sensor voltage", "0")
        s7 = StatusItem(panel, "gas detector", "normal")
        s8 = ModbusGet(panel)


        self.Add(s1, 0, wx.EXPAND|wx.ALL)
        self.Add(s3, 0, wx.EXPAND|wx.ALL)
        self.Add(s5, 0, wx.EXPAND|wx.ALL)
        self.Add(s7, 0, wx.EXPAND|wx.ALL)

        self.Add(s2, 0, wx.EXPAND|wx.ALL)
        self.Add(s4, 0, wx.EXPAND|wx.ALL)
        self.Add(s6, 0, wx.EXPAND|wx.ALL)
        self.Add(s8, 0, wx.EXPAND|wx.ALL)

class ModbusGet(wx.BoxSizer):
    def __init__(self, panel):
        wx.BoxSizer.__init__(self, wx.VERTICAL)
        self.panel = panel
        self.t = wx.TextCtrl(panel, -1, "slave address", 
                size=(-1, 30), style=wx.TE_CENTER)
        b = wx.Button(panel, -1, "Get")
        panel.Bind(wx.EVT_BUTTON, self.OnClick, b)

        self.Add(self.t, 0, wx.ALIGN_CENTRE|wx.EXPAND)
        self.Add(b, 0, wx.ALIGN_CENTRE)

    def OnClick(self, event):
        try:
            slave_addr = int(self.t.GetValue())
            if self.panel.master != None:
                ret = self.panel.master.execute(slave_addr, cst.READ_INPUT_REGISTERS, 0x0101, 7)
                print ret
        except ValueError:
            print "slave address error!"
        except:
            pass

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


