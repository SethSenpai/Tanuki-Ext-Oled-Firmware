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

    screen = displayio.Group()
    #updatable elements
    LabelCL = label.Label(terminalio.FONT, text = "CL", color = 0x000000, x = 2, y = 6,background_color=0xffffff, padding_left = 2, padding_right=1)
    LabelSL = label.Label(terminalio.FONT, text="SL", color = 0x000000, x = 19, y = 6, background_color=0xffffff, padding_left = 2, padding_right=1)
    LabelLayer = label.Label(terminalio.FONT, text="BOOT", color = 0x000000, x = 5 , y = 20, background_color=0xffffff, padding_left = 16, padding_right=16)
        

    def __init__(self,SCL,SDA):
        displayio.release_displays() #needed because the otherwise its claimed for debugging
        i2c = busio.I2C(SCL,SDA)
        display_bus = displayio.I2CDisplay(i2c,device_address=0x3c)
        display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=32,height=128, rotation=90) #this configuration only works when pulling from the latest adafruit master

        sprite = displayio.OnDiskBitmap("/tanukilogo.bmp")
        tsprite = displayio.TileGrid(sprite,pixel_shader=sprite.pixel_shader,x=0,y=64)
        gsprite = displayio.Group()
        gsprite.append(tsprite)   
        self.screen.append(gsprite)
        hr = Rect(0,28,32,1, outline=0xffffff)
        self.screen.append(hr)
        self.screen.append(self.LabelCL)
        self.screen.append(self.LabelSL)
        self.screen.append(self.LabelLayer)
        display.show(self.screen)

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
        #print(len(self.screen))

   