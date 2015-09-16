#-*-coding:utf-8-*- 
import wx
import serial
from list_ports_windows import comports
from pm25_work import DisplayQueue, UsartReceive

class UsartSizer(wx.BoxSizer):
    def __init__(self, panel):
        wx.BoxSizer.__init__(self, wx.HORIZONTAL)
        panel.usart_output = wx.TextCtrl(panel, -1,
                size=(500, 410), style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_RICH2)
        #panel.usart_output.SetDefaultStyle(wx.TextAttr("blue"))
        o = UsartOperation(panel)

        self.Add(panel.usart_output, 0, wx.ALIGN_LEFT|wx.ALL, 10)
        self.Add(o, 0, wx.ALIGN_LEFT|wx.ALL) 
        self.Fit(panel)


class UsartOperation(wx.BoxSizer):
    def __init__(self, panel):
        wx.BoxSizer.__init__(self, wx.VERTICAL)
        self.panel = panel
        self.panel.usart_handle = None
        l = wx.StaticText(panel, -1, u"  输入发送数据：", style=wx.ALIGN_LEFT)
        self.send = wx.TextCtrl(panel, -1, size=(220, 30))
        btn_send = wx.Button(panel, -1, "Send")
        panel.Bind(wx.EVT_BUTTON, self.OnClickSend, btn_send)
        open_usart = OpenUsart(panel)
        btn_clear = wx.Button(panel, -1, "Clear")
        panel.Bind(wx.EVT_BUTTON, self.OnClickClear, btn_clear)


        font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        l.SetFont(font)
        self.send.SetFont(font)
        btn_send.SetFont(font)
        btn_clear.SetFont(font)
        self.Add(l, 0, wx.ALIGN_LEFT|wx.ALL, 3)
        self.Add(self.send, 0, wx.ALIGN_LEFT|wx.ALL, 3)
        self.Add(btn_send, 0, wx.ALIGN_RIGHT|wx.ALL, 10)
        self.Add(open_usart, 0, wx.ALIGN_LEFT|wx.ALL, 3)
        self.Add(btn_clear, 0, wx.TOP, 220)

    def OnClickSend(self, event):
        send_buf = self.send.GetValue()
        if len(send_buf) > 0:
            #print [int(i) for i in send_buf.split(" ")]
            if self.panel.usart_handle != None and self.panel.usart_handle.isOpen():
                try:
                    self.panel.display_queue.put(1, [int(i, 16) for i in send_buf.split(" ")])
                except ValueError:
                    self.panel.display_queue.put(1, [int(i, 16) for i in send_buf.strip(" ").split(" ")])


    def OnClickClear(self, event):
        self.panel.usart_output.Clear()


class OpenUsart(wx.BoxSizer):
    def __init__(self, panel):
        wx.BoxSizer.__init__(self, wx.HORIZONTAL)
        self.panel = panel
        self.port_index = 0xFF
        self.port_list = []
        self.generate_com_list()

        c = wx.ComboBox(panel, -1, u"选择串口", size=(100, 30),
                choices=self.port_list, style=wx.CB_DROPDOWN)
        panel.Bind(wx.EVT_COMBOBOX, self.OnChoice, c)
        self.btn_open = wx.Button(panel, -1, "Open")
        panel.Bind(wx.EVT_BUTTON, self.OnClickOpen, self.btn_open)
        btn_close = wx.Button(panel, -1, "Close")
        panel.Bind(wx.EVT_BUTTON, self.OnClickClose, btn_close)

        font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        c.SetFont(font)
        btn_close.SetFont(font)
        self.btn_open.SetFont(font)
        self.Add(c, 0, wx.ALIGN_LEFT|wx.ALL, 5)
        self.Add(self.btn_open, 0, wx.ALIGN_LEFT|wx.ALL, 5)
        self.Add(btn_close, 0, wx.ALIGN_LEFT|wx.ALL, 5)

    def OnChoice(self, event):
        self.port_index = event.GetSelection()

    def OnClickOpen(self, event):
        if 0xFF != self.port_index:
            try:
                self.panel.usart_handle = serial.Serial(
                    self.port_list[self.port_index], 19200, timeout=0.2)
                self.btn_open.SetBackgroundColour("Green")
                self.panel.exit = False
                self.panel.display_queue = DisplayQueue(self.panel)
                self.panel.display_queue.start()
                self.panel.usart_receive = UsartReceive(self.panel)
                self.panel.usart_receive.start()
            except serial.SerialException:
                self.btn_open.SetBackgroundColour("Red")
                self.panel.usart_output.AppendText(u"%s 打开失败！\n"
                        % self.port_list[self.port_index])
                self.port_index = 0xFF

    def generate_com_list(self):
        for port, desc, hwid in sorted(comports()):
            #print "%s: %s %s" % (port, desc, hwid)
            self.port_list.append(port)
			
    def OnClickClose(self, event):
        if self.panel.usart_handle != None:
            self.btn_open.SetBackgroundColour("Default")
            self.panel.exit = True
            self.panel.display_queue.join()
            self.panel.usart_receive.join()
            self.panel.usart_handle.close()
            self.panel.usart_handle = None


