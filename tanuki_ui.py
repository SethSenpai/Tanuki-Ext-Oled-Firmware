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
    lastActivity = 0
    emoteTimer = 0
    lastScancode = 0

    cardLogo = displayio.Group(y=30-16) #this is the Y clearance from the lock state indicators
    cardWPM = displayio.Group(y=36)
    wholeScreen = displayio.Group()
    cardStats = displayio.Group(y=30)
    display = None

    #updatable elements
    LabelCL = label.Label(terminalio.FONT, text = "CL", color = 0x000000, x = 2, y = 6,background_color=0xffffff, padding_left = 2, padding_right=1)
    LabelSL = label.Label(terminalio.FONT, text="SL", color = 0x000000, x = 19, y = 6, background_color=0xffffff, padding_left = 2, padding_right=1)
    LabelLayer = label.Label(terminalio.FONT, text="BOOT", color = 0x000000, x = 5 , y = 20, background_color=0xffffff, padding_left = 16, padding_right=16)
    LabelWPM = label.Label(terminalio.FONT, text="000", color = 0xFFFFFF,x=7,y=16+64)
    SparklineWPM = Sparkline(width=32, height=48, max_items=8, y_min=0, dyn_xpitch=True, y_max=200)
    LabelStats = label.Label(terminalio.FONT, text="", color = 0xFFFFFF, y = 5)
    SpriteNormal = None
    SpriteExcite = None
    SpriteQuestion = None


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
        excite = displayio.OnDiskBitmap("/tanukilogo_excite.bmp")
        self.SpriteExcite = displayio.TileGrid(excite,pixel_shader=excite.pixel_shader,x=0,y=28)
        question = displayio.OnDiskBitmap("tanukilogo_question.bmp")
        self.SpriteQuestion = displayio.TileGrid(question,pixel_shader=question.pixel_shader,x=0,y=28)
        
        self.cardLogo.append(self.SpriteNormal)
        self.cardLogo.append(self.SpriteExcite)
        self.SpriteExcite.hidden = True
        self.cardLogo.append(self.SpriteQuestion)
        self.SpriteQuestion.hidden = True
        
        #word per minute counter
        labelIndicator = label.Label(terminalio.FONT, text="WPM: ", color = 0xFFFFFF,x=5, y=64)
        self.cardWPM.append(labelIndicator)
        self.cardWPM.append(self.LabelWPM)
        self.cardWPM.append(self.SparklineWPM)

        #card for stats
        self.cardStats.append(self.LabelStats)

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
        self.wholeScreen.append(self.cardStats)
        self.display.show(self.wholeScreen)
        self.changeCard(0)
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

    def updateWPM(self,wpm,wpmNow):
        if self.cardWPM.hidden is False:
            self.LabelWPM.text = "{0:0>3}".format(wpm)
            self.SparklineWPM.add_value(wpmNow)
            self.display.refresh()

    def updateStats(self,string):
        if self.cardStats.hidden is False:
            self.LabelStats.text = string
            self.display.refresh()

    def changeCard(self,index):
        if index == 0:
            self.cardWPM.hidden = True
            self.cardLogo.hidden = False
            self.cardStats.hidden = True
        elif index == 1:
            self.cardWPM.hidden = False
            self.cardLogo.hidden = True
            self.cardStats.hidden = True
        elif index == 2:
            self.cardStats.hidden = False
            self.cardWPM.hidden = True
            self.cardLogo.hidden = True
        self.display.refresh()

    def updateActivity(self):
        self.lastActivity = ticks_ms()
        self.wholeScreen.hidden = False
        if self.wholeScreen.hidden == True:
            self.display.refresh()

    def checkTimeout(self): #Turn the OLED off after 1 minute to prevent burn-in
        ct = ticks_ms()
        if ct - self.lastActivity > 60000 or ct - self.lastActivity < 0:
            if self.wholeScreen.hidden is False:
                self.wholeScreen.hidden = True
                self.display.refresh()

    def checkEmoteTimeout(self):
        if self.cardLogo.hidden == True:
            return
        ct = ticks_ms()
        if ct - self.emoteTimer > 2500 or ct - self.emoteTimer < 0:
            self.emoteTimer = ct
            self.SpriteNormal.hidden = False
            self.SpriteQuestion.hidden = True
            self.SpriteExcite.hidden = True
            #self.display.refresh()


    def checkEmoteLayer(self,scancode):
        if self.cardLogo.hidden == True:
            return
        if scancode == 0x1e: #! pressed
            self.emoteTimer = ticks_ms()
            #self.SpriteNormal.hidden = True
            #self.SpriteQuestion.hidden = True
            #self.SpriteExcite.hidden = False
            #self.display.refresh()
        if scancode == 0x38: #? pressed
            self.emoteTimer = ticks_ms()
            #self.SpriteNormal.hidden = True
            #self.SpriteQuestion.hidden = False
            #self.SpriteExcite.hidden = True
            #self.display.refresh()