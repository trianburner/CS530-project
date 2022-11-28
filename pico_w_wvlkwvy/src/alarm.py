""" Alarm class for interfacing with the pin controlling the transistor-switched audible alarm

    Provide easy methods for controlling the device, also allows multiple objects as a class in case
    there are mutliple alarms in the system
 """
import machine, time
from machine import Pin

class Alarm:
    # Initialize object and trigger pin
    def __init__(self, trigger_pin):
        self.trigger = Pin(trigger_pin, Pin.OUT, Pin.PULL_DOWN)
        self.trigger.value(0)
    
    # Turn the alarm on
    def on(self):
        self.trigger.value(1)
        
    # Turne the alarm off
    def off(self):
        self.trigger.value(0)