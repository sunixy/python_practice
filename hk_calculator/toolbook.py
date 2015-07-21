
import wx
from pm25 import * 
from hcho import *

book_list = ["PM2.5", "HCHO"]
img_list = ["img/LB01.png", "img/LB02.png"]

class MyToolbook(wx.Toolbook):
    def __init__(self, parent):
        wx.Toolbook.__init__(self, parent, -1, style=wx.BK_DEFAULT,size=(900, 600))
        count = self.GenerateImageList(img_list)
        imageGenerator = GetNextImageId(count)
        for book in book_list:
            p = self.MakeBookPanel()
            self.AddPage(p, book, imageId=imageGenerator.next())

            if (book == "PM2.5"):
                Pm25(p.win) 
            elif (book == "HCHO"):
                Hcho(p.win)

        #self.Bind(wx.EVT_TOOLBOOK_PAGE_CHANGED, self.OnPageChanged)
        #self.Bind(wx.EVT_TOOLBOOK_PAGE_CHANGING, self.OnPageChanging)

    def MakeBookPanel(self):
        p = wx.Panel(self, -1, size=(900, 600))
        p.win = wx.Window(p, -1, style=wx.SIMPLE_BORDER, size=(900, 570)) 
        p.win.SetBackgroundColour("Aquamarine")
        def OnCPSize(evt, win=p.win):
            win.SetPosition((0,0))
            win.SetSize(evt.GetSize())
        p.Bind(wx.EVT_SIZE, OnCPSize)
        return p

    def GenerateImageList(self, names):
        imgList = wx.ImageList(32, 32)
        for name in names:
            img = wx.Image(name, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
            imgList.Add(img)

        self.AssignImageList(imgList)
        return imgList.GetImageCount()

def GetNextImageId(count):
    imId = 0
    while True:
        yield imId
        imId += 1
        if imId == count:
            imId = 0
        




