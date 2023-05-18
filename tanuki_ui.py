import displayio
import adafruit_displayio_ssd1306
import busio
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
import terminalio



class TanukiUI:
    isSpaceLocked = True
    lstrings = ["BASE","NBRS","SMBL"] 
    layerIndex = 0

    def __init__(self,SCL,SDA):
        displayio.release_displays() #needed because the otherwise its claimed for debugging
        i2c = busio.I2C(SCL,SDA)
        display_bus = displayio.I2CDisplay(i2c,device_address=0x3c)
        global display
        display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=32,height=128, rotation=90) #this configuration only works when pulling from the latest adafruit master

    def renderUI(self,locks): 
        global display
        screen = displayio.Group()
        uiGroup = displayio.Group()
        #border = Rect(0,0,32,128, outline=0xffffff)
        #uiGroup.append(border)

        screen.append(uiGroup)

        if locks.get_caps_lock():
            ta = label.Label(terminalio.FONT, text = "CL", color = 0x000000, x = 2, y = 6,background_color=0xffffff, padding_left = 2, padding_right=1)
            screen.append(ta)

        if self.isSpaceLocked:
            ta = label.Label(terminalio.FONT, text="SL", color = 0x000000, x = 19, y = 6, background_color=0xffffff, padding_left = 2, padding_right=1)
            screen.append(ta)
        
        ll = label.Label(terminalio.FONT, text=self.lstrings[self.layerIndex], color = 0x000000, x = 5 , y = 20, background_color=0xffffff, padding_left = 16, padding_right=16)
        screen.append(ll)
        display.show(screen)

