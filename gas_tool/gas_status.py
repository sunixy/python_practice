#!/usr/bin/env python
#-*-coding:utf-8-*-

import wx
import modbus_tk.defines as cst

class StatusSizer(wx.GridSizer):
    def __init__(self, panel):
        wx.GridSizer.__init__(self, rows=2, cols=4, hgap=10, vgap=10)
        self.sensor_zero = StatusItem(panel, "sensor zero voltage", "0")
        self.sensor_full = StatusItem(panel, "sensor full voltage", "0")
        self.output_zero = StatusItem(panel, "4~20mA zero voltage", "0")
        self.output_full = StatusItem(panel, "4~20mA full voltage", "0")
        self.lel = StatusItem(panel, "LEL", "0")
        self.vol = StatusItem(panel, "sensor voltage", "0")
        self.status = StatusItem(panel, "gas detector", "normal")
        s8 = ModbusGet(panel, self)


        self.Add(self.sensor_zero, 0, wx.EXPAND|wx.ALL)
        self.Add(self.output_zero, 0, wx.EXPAND|wx.ALL)
        self.Add(self.lel, 0, wx.EXPAND|wx.ALL)
        self.Add(self.status, 0, wx.EXPAND|wx.ALL)

        self.Add(self.sensor_full, 0, wx.EXPAND|wx.ALL)
        self.Add(self.output_full, 0, wx.EXPAND|wx.ALL)
        self.Add(self.vol, 0, wx.EXPAND|wx.ALL)
        self.Add(s8, 0, wx.EXPAND|wx.ALL)

class ModbusGet(wx.BoxSizer):
    def __init__(self, panel, status):
        wx.BoxSizer.__init__(self, wx.VERTICAL)
        self.panel = panel
        self.status = status
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
                values = self.panel.master.execute(slave_addr, cst.READ_INPUT_REGISTERS, 0x0101, 7)
                for index, i in enumerate(values):
                    if 0 == index:
                        self.status.sensor_zero.set_value(str(i))
                    elif 1 == index:
                        self.status.sensor_full.set_value(str(i))
                    elif 2 == index:
                        self.status.output_zero.set_value(str(i))
                    elif 3 == index:
                        self.status.output_full.set_value(str(i))
                    elif 5 == index:
                        if i >= 32768:
                            i = i - 65536
                        self.status.lel.set_value(str(i))
                    elif 4 == index:
                        self.status.vol.set_value(str(i))
                    elif 6 == index:
                        self.status.status.set_value(str(i))
                    else:
                        pass
        except ValueError:
            print "slave address error!"
        except Exception ,e:
            print e
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


