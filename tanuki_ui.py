import displayio
import adafruit_displayio_ssd1306
import busio
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
import terminalio



class TanukiUI:
    isSpaceLocked = False
    lstrings = ["BASE","SMBL","NBRS","BASE"] 
    layerIndex = 0

    cardLogo = displayio.Group(y=30) #this is the Y clearance from the lock state indicators
    cardWPM = displayio.Group(y=30)
    wholeScreen = displayio.Group()
    #updatable elements
    LabelCL = label.Label(terminalio.FONT, text = "CL", color = 0x000000, x = 2, y = 6,background_color=0xffffff, padding_left = 2, padding_right=1)
    LabelSL = label.Label(terminalio.FONT, text="SL", color = 0x000000, x = 19, y = 6, background_color=0xffffff, padding_left = 2, padding_right=1)
    LabelLayer = label.Label(terminalio.FONT, text="BOOT", color = 0x000000, x = 5 , y = 20, background_color=0xffffff, padding_left = 16, padding_right=16)

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
        display.show(self.wholeScreen)

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

    def clearAndAddUI(self):
        print("farts")
        # self.screen
        # self.screen.append(self.hr)
        # self.screen.append(self.LabelCL)
        # self.screen.append(self.LabelSL)
        # self.screen.append(self.LabelLayer)

    def changeCard(self,index):
        if index == 0:
            print("zero")
            #self.clearAndAddUI()
            #self.screen.append(self.gsprite)

        elif index == 1:
            #self.clearAndAddUI()
            print("one")
        elif index == 2:
            print("two")
            #self.updateUI(self)