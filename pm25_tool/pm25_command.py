#-*-coding:utf-8-*- 
import wx

def check_sum(data):
    sum = 0
    for i in range(1, 6):
        sum += data[i]
    return int_low(sum)

def int_high(n):
    if (n > 255):
        return (n >> 8) & 255 
    else:
        return 0

def int_low(n):
    if (n > 255):
        return n & 255 
    else:
        return n 



MODE = [0x00, 0x01, 0x02, 0xF1]
MODE_COMMAND = [0xC0, 0x02, 0x01, 0x00, 0x00, 0x00, 0x00, 0xAA]
PPM_COMMAND = [0xC0, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0xAA]
ADC_COMMAND = [0xC0, 0x01, 0xFD, 0x00, 0x00, 0x00, 0x00, 0xAA]
CALIBRATE_COMMAND = [0xC0, 0x01, 0xFE, 0x00, 0x00, 0x00, 0x00, 0xAA]
GET_CALIBRATE_COMMAND = [0xC0, 0x01, 0xFC, 0x00, 0x00, 0x00, 0x00, 0xAA]

class CommandSizer(wx.GridSizer):
    def __init__(self, panel):
        wx.GridSizer.__init__(self, rows=1, cols=5, hgap=10)
        font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        s1 = ModeCommand(panel)
        b2 = PPMCommand(panel)
        b3 = AdcCommand(panel)
        s4 = CalibrateCommand(panel)
        b5 = GetCalibrateValue(panel)

        self.Add(s1, 0, wx.ALIGN_CENTER|wx.ALL)
        self.Add(b2, 0, wx.ALIGN_CENTER|wx.ALL)
        self.Add(b3, 0, wx.ALIGN_CENTER|wx.ALL)
        self.Add(s4, 0, wx.ALIGN_CENTER|wx.ALL)
        self.Add(b5, 0, wx.ALIGN_CENTER|wx.ALL)
        self.SetMinSize((800, 50))
        self.Fit(panel)

class ModeCommand(wx.BoxSizer):
    def __init__(self, panel):
        wx.BoxSizer.__init__(self, wx.VERTICAL)
        self.panel = panel
        self.mode = 0xFF
        b = wx.Button(panel, -1, "Mode")
        panel.Bind(wx.EVT_BUTTON, self.OnClick, b)
        c = wx.ComboBox(panel, -1, u"选择模式", size=(100, 30),
                choices=[u"电压", u"查询", u"通知", u"调试"],
                style=wx.CB_DROPDOWN)
        panel.Bind(wx.EVT_COMBOBOX, self.OnChoice, c)
        font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        b.SetFont(font)
        c.SetFont(font)
        self.Add(b, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        self.Add(c, 0, wx.ALIGN_CENTER|wx.ALL)

    def OnClick(self, event):
        if self.mode != 0xFF:
            if self.panel.usart_handle != None and self.panel.usart_handle.isOpen():
                MODE_COMMAND[3] = MODE[self.mode]
                MODE_COMMAND[6] = check_sum(MODE_COMMAND)
                self.panel.display_queue.put(1, MODE_COMMAND)

    def OnChoice(self, event):
        self.mode = event.GetSelection() 

class PPMCommand(wx.Button):
    def __init__(self, panel):
        wx.Button.__init__(self, panel, -1, "Get PPM")
        self.panel = panel
        panel.Bind(wx.EVT_BUTTON, self.OnClick, self)
        font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        self.SetFont(font)

    def OnClick(self, event):
        if self.panel.usart_handle != None and self.panel.usart_handle.isOpen():
            PPM_COMMAND[6] = check_sum(PPM_COMMAND)
            self.panel.display_queue.put(1, PPM_COMMAND)

class AdcCommand(wx.Button):
    def __init__(self, panel):
        wx.Button.__init__(self, panel, -1, "Get ADC")
        self.panel = panel
        panel.Bind(wx.EVT_BUTTON, self.OnClick, self)
        font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        self.SetFont(font)

    def OnClick(self, event):
        if self.panel.usart_handle != None and self.panel.usart_handle.isOpen():
            ADC_COMMAND[6] = check_sum(ADC_COMMAND)
            self.panel.display_queue.put(1, ADC_COMMAND)
            PPM_COMMAND[6] = check_sum(PPM_COMMAND)
            self.panel.display_queue.put(1, PPM_COMMAND)

class CalibrateCommand(wx.BoxSizer):
    def __init__(self, panel):
        wx.BoxSizer.__init__(self, wx.VERTICAL)
        self.panel = panel
        b = wx.Button(panel, -1, "Calibration")
        panel.Bind(wx.EVT_BUTTON, self.OnClick, b)
        self.e = wx.TextCtrl(panel, -1, u"输入标定PPM", 
                style=wx.TE_CENTER|wx.TE_RICH2)
        self.e.SetInsertionPoint(0)
        self.e.SetStyle(0, self.e.GetLineLength(0),
                wx.TextAttr("RED", "YELLOW"))
        font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        b.SetFont(font)
        self.e.SetFont(font)
        self.Add(b, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        self.Add(self.e, 0, wx.ALIGN_CENTER|wx.EXPAND)

    def OnClick(self, event):
        value = self.e.GetValue()
        if value.isdigit():
            if self.panel.usart_handle != None and self.panel.usart_handle.isOpen():
                calibratePPM = int(value)
                deviceAdc = self.panel.status_adc.get_value()
                calibrate_num = int((500.0*deviceAdc-850*calibratePPM)/(500.0-calibratePPM))
                if calibrate_num < 0:
                    return
                CALIBRATE_COMMAND[3] = int_high(calibrate_num)
                CALIBRATE_COMMAND[4] = int_low(calibrate_num)
                CALIBRATE_COMMAND[6] = check_sum(CALIBRATE_COMMAND)
                self.panel.display_queue.put(1, CALIBRATE_COMMAND)

class GetCalibrateValue(wx.Button):
    def __init__(self, panel):
        wx.Button.__init__(self, panel, -1, "Get Calibrate ")
        self.panel = panel
        panel.Bind(wx.EVT_BUTTON, self.OnClick, self)
        font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        self.SetFont(font)
        
    def OnClick(self, event):
        GET_CALIBRATE_COMMAND[6] = check_sum(GET_CALIBRATE_COMMAND)
        self.panel.display_queue.put(1, GET_CALIBRATE_COMMAND)
        

