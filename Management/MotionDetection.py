"""
MotionDetection.py implements subsequent logic & script
"""
from time import sleep
from machine import RTC
from System import Components, Internal

def pollSensor(socket):
    """
    pollSensor() continuously checks the HCSR04 Sensor to detect motion. If tripped, the time is also compared to
    discern whether an alarm should sound.
    :param socket:
    :return:
    """
    wallDistance = 10
    rtc = RTC()

    while True:
        distance = Components.sensor.distance_cm() # distance currently measured
        if (distance > 0) and (distance < wallDistance): # if less than 10, sensor is being blocked
            current_time = rtc.datetime()
            current_time = (current_time[4] * 60) + current_time[5] # current time (mins)

            # is current time within security Alarm window?
            if current_time > Internal.alarmWindow[0] or current_time < Internal.alarmWindow[1]:
                socket.send("Alarm!") # ping phone

                Components.alarm.on()
                Components.lights.run(1) # alarm LED lighting
                Components.alarm.off()
            else:
                Components.lights.run(0) # normal LED lighting
        sleep(.1)