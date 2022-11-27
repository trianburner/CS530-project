"""
Components.py contains all the instantiated objects representing the product's external devices
"""

from Management.Alarm import Alarm
from Management.Lights import PixelStrip
from hcsr04 import HCSR04

SENSOR_TRIGGER_PIN = 15
SENSOR_ECHO_PIN = 14
ALARM_TRIGGER_PIN = 13
NEOPIXEL_DATA_PIN = 7
NEOPIXEL_NUM_PIXELS = 50

sensor = HCSR04(trigger_pin = SENSOR_TRIGGER_PIN, echo_pin = SENSOR_ECHO_PIN, echo_timeout_us = 10000)
alarm = Alarm(trigger_pin = ALARM_TRIGGER_PIN)
lights = PixelStrip(data_pin = NEOPIXEL_DATA_PIN, num_pixels = NEOPIXEL_NUM_PIXELS)