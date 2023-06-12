from supervisor import ticks_ms
from kmk.kmk_keyboard import KMKKeyboard
from kmk.modules import Module

class WPM(Module):
    def __init__(self, ui, timeout = 10, averages = 10):
        self.wordCounter = 0
        self.lastCharacter = 0
        self.wpm = 0
        self.startTime = 0
        self.spaceTime = 0
        self.wpmAverage = [0]
        self.timeOut = timeout * 1000 # from seconds to ms
        self.averaging = averages
        self.checkTime = 0
        self.ui = ui

        self.wordEndingCharacterList = [ #list of scan numbers includes number, alpha's and symbols thanks chatgpt
            0x04, 0x05, 0x06, 0x07, 0x08, 
            0x09, 0x0A, 0x0B, 0x0C, 0x0D, 
            0x0E, 0x0F, 0x10, 0x11, 0x12, 
            0x13, 0x14, 0x15, 0x16, 0x17, 
            0x18, 0x19, 0x1A, 0x1B, 0x1C, 
            0x1D, 0x27, 0x1E, 0x1F, 0x20, 
            0x21, 0x22, 0x23, 0x24, 0x25, 
            0x26, 0x37, 0x36, 0x1E, 0x34, 
            0x1F, 0x20, 0x21, 0x22, 0x23, 
            0x24, 0x25, 0x26, 0x27, 0x2D, 
            0x2D, 0x2E, 0x2E, 0x2F, 0x30, 
            0x2F, 0x30, 0x38, 0x31, 0x31, 
            0x33, 0x33, 0x36, 0x37, 0x35, 
            0x35, 0x2F, 0x30
        ]

    def nextKey(self, character):
        if character > 1000: #ignore the special layer keystrokes
            return
        if character == 44 or character == 0x28 and self.lastCharacter in self.wordEndingCharacterList:
            self.wordCounter = self.wordCounter + 1
            self.lastCharacter = character
            self.spaceTime = ticks_ms()
            #self.calculateWPM()
            self.startTime = 0
            #print(self.wordCounter)
            #avg = self.getWPM()
            #print(avg)
        else:
            self.lastCharacter = character
            ct = ticks_ms()
            if ct - self.startTime > self.timeOut:
                #timeout reset counter
                self.startTime = ct

    def getWPMAveraged(self) -> int:
        avg = sum(self.wpmAverage) / len(self.wpmAverage)
        return int(avg)

    def getWPM(self) -> int:
        return self.wpm

    def checkTimeout(self):
        ct = ticks_ms()
        if ct - self.checkTime > self.timeOut:
            wordPerSecond = float(self.wordCounter) / (float(self.timeOut) / 1000.0)
            self.wpm = wordPerSecond * 60.0
            self.wpmAverage.append(self.wpm)
            if(len(self.wpmAverage) > self.averaging - 1):
                self.wpmAverage.pop(0)
            self.wordCounter = 0
            self.checkTime = ct
            self.ui.updateWPM(self.getWPMAveraged(),self.getWPM())