#!/usr/bin/env python
#-*-coding:utf-8-*-

import wx
import os
import serial
import logging

import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_rtu as modbus_rtu

logger = modbus_tk.utils.create_logger("console")

if os.name == "nt":
    from list_ports_windows import comports
if os.name == "posix":
    from list_ports_posix import comports

class UsartSizer(wx.BoxSizer):
    def __init__(self, panel):
        wx.BoxSizer.__init__(self, wx.HORIZONTAL)
        text = UsartText(panel)
        operation = UsartOperation(panel)

        self.Add(text, 0, wx.ALIGN_LEFT|wx.ALL, 10)
        self.Add(operation, 0, wx.EXPAND|wx.ALL, 5)

class UsartText(wx.BoxSizer):
    def __init__(self, panel):
        wx.BoxSizer.__init__(self, wx.VERTICAL)
        self.output = wx.TextCtrl(panel, -1,
            size=(550, 410), style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_RICH2)
        panel.log = self.output
        btn_clear = wx.Button(panel, -1, "Clear")
        panel.Bind(wx.EVT_BUTTON, self.OnClickClear, btn_clear)
        self.Add(self.output, 0, wx.EXPAND|wx.ALL, 5)
        self.Add(btn_clear, 0, wx.ALIGN_RIGHT|wx.ALL, 5)

    def OnClickClear(self, event):
        self.output.Clear()

class UsartOperation(wx.BoxSizer):
    def __init__(self, panel):
        wx.BoxSizer.__init__(self, wx.VERTICAL)
        self.port_list = []
        self.generate_port_list()
        self.master = None
        self.panel = panel

        self.port = wx.ComboBox(panel, -1, u"选择串口", size=(100, 30),
                choices=self.port_list, style=wx.CB_DROPDOWN)
        panel.Bind(wx.EVT_COMBOBOX, self.OnChoice, self.port)
        9
        btn_open = wx.Button(panel, -1, "Open")
        panel.Bind(wx.EVT_BUTTON, self.OnClickOpen, btn_open)

        btn_close = wx.Button(panel, -1, "Close")
        panel.Bind(wx.EVT_BUTTON, self.OnClickClose, btn_close)

        btn_update = wx.Button(panel, -1, "Update")
        panel.Bind(wx.EVT_BUTTON, self.OnClickUpdate, btn_update)


        self.Add(btn_open, 0, wx.ALIGN_TOP|wx.EXPAND|wx.ALL, 5)
        self.Add(btn_close, 0, wx.ALIGN_TOP|wx.EXPAND|wx.ALL, 5)
        self.Add(self.port, 0, wx.ALIGN_TOP|wx.EXPAND|wx.ALL, 5)
        self.Add(btn_update, 0, wx.ALIGN_TOP|wx.EXPAND|wx.ALL, 5)

    def generate_port_list(self):
        for port, desc, hwid in sorted(comports()):
            self.port_list.append(port)

    def OnChoice(self, event):
        self.port_index = event.GetSelection()

    def OnClickOpen(self, event):
        self.master = modbus_rtu.RtuMaster(serial.Serial(port=self.port_list[self.port_index], 
            baudrate=19200, bytesize=8, parity='E', stopbits=1, xonxoff=0))
        self.panel.master = self.master
        self.master.set_timeout(5.0)
        self.master.set_verbose(True)

    def OnClickClose(self, event):
        if self.master != None:
            self.master.close()

    def OnClickUpdate(self, event):
        self.generate_port_list()
        self.port.SetItems(self.port_list)



