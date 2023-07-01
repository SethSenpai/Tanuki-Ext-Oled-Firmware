import microcontroller
from supervisor import ticks_ms

class Devicestats():
    def __init__(self,ui,tempavgsamples = 5,refresh = 5) -> None:
        self.cpuTemp = microcontroller.cpu.temperature
        self.cpuFreq = microcontroller.cpu.frequency
        self.cpuVolt = microcontroller.cpu.voltage
        self.cpuRest = microcontroller.cpu.reset_reason
        self.tempAvg = []
        self.tempAvg.append(self.cpuTemp)
        self.tempSamples = tempavgsamples
        self.refresh = refresh * 1000 #convert seconds to ms
        self.oldTime = 0
        self.ui = ui

    def getCpuTemp(self) -> float:
        return self.cpuTemp
    
    def getCpuTempAvg(self) -> float:
        return sum(self.tempAvg) / len(self.tempAvg)
    
    def aquireStatString(self) -> str:
        string = "TEMP: \n" + '%.2f' %self.getCpuTempAvg() + "\n"
        string = string + "VOLT:\n" + str(self.cpuVolt) + "\n"
        split = str(microcontroller.cpu.reset_reason).split('.')
        string = string + "RST:\n" + split[2] + "\n"
        return string

    def checkTimeout(self) -> None:
        ct = ticks_ms()
        if ct - self.oldTime > self.refresh:
            self.oldTime = ct
            self.cpuTemp = microcontroller.cpu.temperature
            self.cpuFreq = microcontroller.cpu.frequency
            self.cpuVolt = microcontroller.cpu.voltage
            self.cpuRest = microcontroller.cpu.reset_reason
            self.tempAvg.append(self.cpuTemp)
            if(len(self.tempAvg) > self.tempSamples):
                self.tempAvg.pop(0)
            self.ui.updateStats(self.aquireStatString())