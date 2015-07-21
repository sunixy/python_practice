#-*-coding:utf-8-*-
import wx
from convert_pattern import ConvertPattern

class Hcho(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, size=(900, 570))

        volToPPM = VolToPPM(self, u"输出电压转换PPM",
                                    "voltage", "PPM")
        volToAdc = VolToAdc(self, u"输出电压转换成ADC采样值",
                                    "voltage", "adc")
        adcToVol = AdcToVol(self, u"ADC采样值转换成电压",
                                    "adc", "voltage")


        ls = wx.BoxSizer(wx.VERTICAL)
        ls.Add(volToPPM, 0, wx.ALL, 10)
        ls.Add(adcToVol, 0, wx.ALL, 10)

        rs = wx.BoxSizer(wx.VERTICAL)
        rs.Add(volToAdc, 0, wx.ALL, 10)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(ls, 0, wx.ALL, 5)
        sizer.Add(rs, 0, wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)



class VolToPPM(ConvertPattern):
    def __init__(self, panel, boxName, leftName, rightName):
        super(VolToPPM, self).__init__(panel, boxName, leftName, rightName)

    def Calculate(self):
        voltage = float(self.leftEdit.GetValue())
        if voltage <= 1.235:
            ppm = 0.0
        else:
            ppm = 2.5*(voltage-1.235)

        if ppm <= 0.3:
            ppm /= 3
            if ppm < 0.01 and ppm > 0.004:
                ppm = 0.01
        elif ppm <= 0.6:
            ppm -= 0.2
        elif ppm <= 0.9:
            ppm = (ppm*5/3)-0.6
        elif ppm > 5.0:
            ppm = 5.0

        return ppm

class VolToAdc(ConvertPattern):
    def __init__(self, panel, boxName, leftName, rightName):
        super(VolToAdc, self).__init__(panel, boxName, leftName, rightName)

    def Calculate(self):
        voltage = float(self.leftEdit.GetValue())
        if voltage > 4.096:
            return hex(1023)
        else:
            return hex(int(voltage/0.004))

class AdcToVol(ConvertPattern):
    def __init(self, panel, boxName, leftName, rightName):
        super(AdcToVol, self).__init__(panel, boxName, leftName, rightName)

    def Calculate(self):
        adc = int(self.leftEdit.GetValue())
        return adc*0.004



