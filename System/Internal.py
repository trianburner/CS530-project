RGB = [255, 255, 255]
alarmWindow = ["00:00", "06:00"]

def changeRGB(self, newRGB):
    self.RGB = newRGB

def changeAlarmStart(self, startStr):
    self.alarmWindow[0] = startStr

def changeAlarmEnd(self, endStr):
    self.alarmWindow[1] = endStr


