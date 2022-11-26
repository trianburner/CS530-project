import machine, time
from machine import Pin

class Alarm:
    def __init__(self, trigger_pin):
        # Initialize trigger pin
        self.trigger = Pin(trigger_pin, Pin.OUT, Pin.PULL_DOWN)
        self.trigger.value(0)
        
    def on(self):
        self.trigger.value(1)
        
    def off(self):
        self.trigger.value(0)