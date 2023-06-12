import displayio
import adafruit_displayio_ssd1306
import busio
from adafruit_display_text import label
from adafruit_display_shapes.sparkline import Sparkline
from adafruit_display_shapes.rect import Rect
import terminalio
from supervisor import ticks_ms


class TanukiUI:
    isSpaceLocked = False
    lstrings = ["BASE","SMBL","NBRS","BASE"] 
    layerIndex = 0

    cardLogo = displayio.Group(y=30) #this is the Y clearance from the lock state indicators
    cardWPM = displayio.Group(y=36)
    wholeScreen = displayio.Group()
    #updatable elements
    LabelCL = label.Label(terminalio.FONT, text = "CL", color = 0x000000, x = 2, y = 6,background_color=0xffffff, padding_left = 2, padding_right=1)
    LabelSL = label.Label(terminalio.FONT, text="SL", color = 0x000000, x = 19, y = 6, background_color=0xffffff, padding_left = 2, padding_right=1)
    LabelLayer = label.Label(terminalio.FONT, text="BOOT", color = 0x000000, x = 5 , y = 20, background_color=0xffffff, padding_left = 16, padding_right=16)
    LabelWPM = label.Label(terminalio.FONT, text="000", color = 0xFFFFFF,x=7,y=16+64)

    SparklineWPM = Sparkline(width=32, height=48, max_items=8, y_min=0, dyn_xpitch=True, y_max=200)

    def __init__(self,SCL,SDA):
        #initialize hardware display
        displayio.release_displays() #needed because the otherwise its claimed for debugging
        i2c = busio.I2C(SCL,SDA)
        display_bus = displayio.I2CDisplay(i2c,device_address=0x3c)
        display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=32,height=128, rotation=90) #this configuration only works when pulling from the latest adafruit master
        display.brightness = 0.2 #set brightness lower to extend lifetime of the OLED

        #logo card initialization
        sprite = displayio.OnDiskBitmap("/tanukilogo.bmp")
        tsprite = displayio.TileGrid(sprite,pixel_shader=sprite.pixel_shader,x=0,y=28) #place the logo in the center of the leftover screen space
        self.cardLogo.append(tsprite)   
        
        #word per minute counter
        labelIndicator = label.Label(terminalio.FONT, text="WPM: ", color = 0xFFFFFF,x=5, y=64)
        self.cardWPM.append(labelIndicator)
        self.cardWPM.append(self.LabelWPM)
        self.cardWPM.append(self.SparklineWPM)

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
        self.wholeScreen.append(self.cardWPM)
        display.show(self.wholeScreen)

        self.changeCard(0)

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
            #print(len(self.wholeScreen))

    def updateWPM(self,wpm,wpmNow):
        self.LabelWPM.text = "{0:0>3}".format(wpm)
        self.SparklineWPM.add_value(wpmNow)

    def changeCard(self,index):
        if index == 0:
            print("zero")
            self.cardWPM.hidden = True
            self.cardLogo.hidden = False

        elif index == 1:
            #self.clearAndAddUI()
            print("one")
            self.cardWPM.hidden = False
            self.cardLogo.hidden = True
        elif index == 2:
            print("two")
            #self.updateUI(self)