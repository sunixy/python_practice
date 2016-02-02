#-*-coding:utf-8-*- 
import wx
import serial
import threading
from Queue import Queue
import time

GET_PM25 = 0
GET_ADC = 1
CALIBRATE = 2
DATA_DELIVER = 3
PM25_NOTIFY = 4
ERROR_NOTIFY = 5
GET_CALIBRATE = 6

COMMAND_MAP = {(0x01, 0x01):GET_PM25, (0x01, 0xFD):GET_ADC, (0x01, 0xFE):CALIBRATE,
        (0x02, 0x01):DATA_DELIVER, (0x04, 0x01):PM25_NOTIFY, (0x04, 0xFF):ERROR_NOTIFY,
        (0x01, 0xFC):GET_CALIBRATE}

pm25_queue = Queue()

def char_to_int(hign, low):
    value = 0
    value = hign << 8
    value += low
    return value

class WorkMsg(object):
    def __init__(self):
        self.op = 0
        self.msg = None

class DisplayQueue(threading.Thread):
    def __init__(self, panel):
        threading.Thread.__init__(self)
        self.panel = panel

    def run(self):
        global pm25_queue
        while True:
            try:
                item = WorkMsg()
                item = pm25_queue.get(True, 0.2)
            except:
                if self.panel.exit == True:
                    break
                continue
            if item.op == 1:
                self.panel.usart_handle.write(bytearray(item.msg))
                self.panel.usart_output.SetStyle(0, -1, wx.TextAttr("purple"))
            elif item.op == 2:
                self.panel.usart_output.SetStyle(0, -1, wx.TextAttr("blue"))
                self.parse_receive(item.msg)
            else:
                continue

            text = time.strftime("%X | ")
            text += self.command_format(item.msg)
            text += "\n"
            self.panel.usart_output.AppendText(text)

    def put(self, op, msg):
        global pm25_queue
        if (op == 1):
            item = WorkMsg()
            item.op = 1
            item.msg = msg
            pm25_queue.put(item)
        elif (op == 2):
            item = WorkMsg()
            item.op =2
            item.msg = msg
            pm25_queue.put(item)

    def command_format(self, msg):
        cmd = "[ "
        for i in msg:
            cmd += "0x%02x " % i  
        cmd += "]"
        return cmd
    def parse_receive(self, msg):
        code = COMMAND_MAP[(msg[1], msg[2])]
        if code == GET_PM25:
            if msg[3] == 1:
                value = char_to_int(msg[4], msg[5])
                self.panel.status_ppm.set_value(str(value))
                vol = value * 3.125 / 500 + 0.1
                v = "%.2f" % vol
                self.panel.status_voltage.set_value(v)
        elif code == GET_ADC:
            if msg[3] == 1:
                value = char_to_int(msg[4], msg[5])
                self.panel.status_adc.set_value(str(value))
        elif code == CALIBRATE:
            if msg[3] == 1:
                value = char_to_int(msg[4], msg[5])
                self.panel.status_calibrate.set_value(str(value))
        elif code == DATA_DELIVER:
            if msg[4] == 0:
                self.panel.status_mode.set_value(u"电压")
            elif msg[4] == 1:
                self.panel.status_mode.set_value(u"查询")
            elif msg[4] == 2:
                self.panel.status_mode.set_value(u"通知")
            elif msg[4] == 0xF1:
                self.panel.status_mode.set_value(u"调试")
        elif code == PM25_NOTIFY:
            value = char_to_int(msg[3], msg[4])
            self.panel.status_ppm.set_value(str(value))
            vol = value * 3.125 / 500 + 0.1
            v = "%.2f" % vol
            self.panel.status_voltage.set_value(v)
        elif code == ERROR_NOTIFY:
            self.panel.usart_output.SetStyle(0, -1, wx.TextAttr("red"))
        elif code == GET_CALIBRATE:
            if msg[3] == 1:
                value = char_to_int(msg[4], msg[5])
                self.panel.status_calibrate.set_value(str(value))


class UsartReceive(threading.Thread):
    def __init__(self, panel):
        threading.Thread.__init__(self)
        self.panel = panel

    def run(self):
        global pm25_queue
        while True:
            read_buf = self.panel.usart_handle.read(8)
            if self.panel.exit == True:
                break
            if len(read_buf):
                msg = list(read_buf)
                msg = [ord(i) for i in msg]
                self.panel.display_queue.put(2, msg)



