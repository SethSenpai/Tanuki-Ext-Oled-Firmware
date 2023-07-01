import displayio
import adafruit_displayio_ssd1306
import busio
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
import terminalio
from supervisor import ticks_ms


class TanukiUI:
    isSpaceLocked = False
    lstrings = ["BASE","SMBL","NBRS","BASE"] 
    layerIndex = 0
    lastActivity = 0

    cardLogo = displayio.Group(y=30-16) #this is the Y clearance from the lock state indicators
    wholeScreen = displayio.Group()
    display = None

    #updatable elements
    LabelCL = label.Label(terminalio.FONT, text = "CL", color = 0x000000, x = 2, y = 6,background_color=0xffffff, padding_left = 2, padding_right=1)
    LabelSL = label.Label(terminalio.FONT, text="SL", color = 0x000000, x = 19, y = 6, background_color=0xffffff, padding_left = 2, padding_right=1)
    LabelLayer = label.Label(terminalio.FONT, text="BOOT", color = 0x000000, x = 5 , y = 20, background_color=0xffffff, padding_left = 16, padding_right=16) 
    SpriteNormal = None



    def __init__(self,SCL,SDA):
        #initialize hardware display
        displayio.release_displays() #needed because the otherwise its claimed for debugging
        i2c = busio.I2C(SCL,SDA)
        display_bus = displayio.I2CDisplay(i2c,device_address=0x3c)
        self.display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=32,height=128, rotation=90) #this configuration only works when pulling from the latest adafruit master
        self.display.brightness = 0.2 #set brightness lower to extend lifetime of the OLED
        self.display.auto_refresh = False
        #display.refresh(minimum_frames_per_second=2, target_frames_per_second=2)

        #logo card initialization
        normal = displayio.OnDiskBitmap("/tanukilogo.bmp")
        self.SpriteNormal = displayio.TileGrid(normal,pixel_shader=normal.pixel_shader,x=0,y=28) #place the logo in the center of the leftover screen space
        self.cardLogo.append(self.SpriteNormal)

        #lock and layer status initialisation
        lockAndLayer = displayio.Group()
        hr = Rect(0,28,32,1, outline=0xffffff)
        lockAndLayer.append(hr)
        lockAndLayer.append(self.LabelCL)
        lockAndLayer.append(self.LabelSL)
        lockAndLayer.append(self.LabelLayer)

        #add all groups to the encompassing group
        self.wholeScreen.append(lockAndLayer)
        self.wholeScreen.append(self.cardLogo)
        self.display.show(self.wholeScreen)
        self.display.refresh()

    def updateUI(self,locks):
        if locks.get_caps_lock(): #capslock block
            self.LabelCL.text = "CL"
            self.LabelCL.background_color=0xffffff
        else:
            self.LabelCL.text = ""
            self.LabelCL.background_color=0x000000
        if self.isSpaceLocked: #spacelock block
            self.LabelSL.text = "SL"
            self.LabelSL.background_color=0xffffff
        else:
            self.LabelSL.text = ""
            self.LabelSL.background_color=0x000000
        
        self.LabelLayer.text = self.lstrings[self.layerIndex]
        self.display.refresh()

    def updateActivity(self):
        self.lastActivity = ticks_ms()
        if self.wholeScreen.hidden == False:
            return
        else:
            self.wholeScreen.hidden = False
            self.display.refresh()
        if self.wholeScreen.hidden == True:
            self.display.refresh()

    def checkTimeout(self): #Turn the OLED off after 1 minute to prevent burn-in
        ct = ticks_ms()
        if ct - self.lastActivity > 60000 or ct - self.lastActivity < 0:
            if self.wholeScreen.hidden is False:
                self.wholeScreen.hidden = True
                self.display.refresh()
