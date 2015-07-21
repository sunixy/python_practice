#-*-coding:utf-8-*-
import wx
from convert_pattern import ConvertPattern

class Pm25(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, size=(900, 570))

        outputVol = OutputVol(self, u"PM2.5输出电压转换PPM",
                                    "output voltage", "PPM")
        outputUsart = OutputUsart(self, u"PM2.5 USART读数转换PPM",
                                    "read value", "PPM")
        calibration = Calibration(self, u"输入标定PPM,设备PPM转换成标定ADC的值",
                                "calibrate and device PPM", "calibrate ADC value")
        pwmDuty = PwmDuty(self, u"PPM转换PWM的占空比", "PPM", "duty")


        ls = wx.BoxSizer(wx.VERTICAL)
        ls.Add(outputVol, 0, wx.ALL, 10)
        ls.Add(calibration, 0, wx.ALL, 10)

        rs = wx.BoxSizer(wx.VERTICAL)
        rs.Add(outputUsart, 0, wx.ALL, 10)
        rs.Add(pwmDuty, 0, wx.ALL, 10)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(ls, 0, wx.ALL, 5)
        sizer.Add(rs, 0, wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)


class OutputVol(ConvertPattern):
    def __init__(self, panel, boxName, leftName, rightName):
        super(OutputVol, self).__init__(panel, boxName, leftName, rightName)

    def Calculate(self):
        voltage = float(self.leftEdit.GetValue())
        return int((500/3.125)*(voltage-0.1)) 


class OutputUsart(ConvertPattern):
    def __init__(self, panel, boxName, leftName, rightName):
        super(OutputUsart, self).__init__(panel, boxName, leftName, rightName)

    def Calculate(self):
        ppm = int(self.leftEdit.GetValue(), 16)
        return ppm 

class Calibration(ConvertPattern):
    def __init__(self, panel, boxName, leftName, rightName):
        super(Calibration, self).__init__(panel, boxName, leftName, rightName)

    def Calculate(self):
        valueList = self.leftEdit.GetValue().split(",")
        calibratePPM = int(valueList[0])
        devicePPM = int(valueList[1])

        deviceAdc = devicePPM*700.0/500+150
        return int((500*deviceAdc-850*calibratePPM)/(500-calibratePPM))


class PwmDuty(ConvertPattern):
    def __init__(self, panel, boxName, leftName, rightName):
        super(PwmDuty, self).__init__(panel, boxName, leftName, rightName)

    def Calculate(self):
        ppm = int(self.leftEdit.GetValue())
        return ppm+16 
    

