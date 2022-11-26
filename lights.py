import time
import machine
import neopixel

sensor = False
rgb_color = [(0,0,255),(255, 0 ,0)]
alarm_Mode = False
pixel_pin = machine.Pin(7)

# The number of NeoPixels
num_pixels = 50

# Initialize the pixels
pixels = neopixel.NeoPixel(pixel_pin, num_pixels)

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, b, g)

# Cycles the rainbow accross the length of the pixels
def rainbow_cycle():
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.write()
        time.sleep(.1)
    #waitTime()

# Spreads a color accross the length of the pixels, with second color transition
def alt_color():
    for x in range(num_pixels):
        for y in range(len(rgb_color)):
            if x < 50:
                pixels[x] = rgb_color[y]
                x = x + 1
        pixels.write()
        time.sleep(0.1)
    #waitTime()

# Turns all pixels off
def off():
    pixels.fill((0,0,0))
    pixels.write()
    
# Fades all pixels off
def fadeOff():
    for dim in range(200, 0, -1):
        allOff = 0
        for j in range(num_pixels):
            if pixels[j][0] != 0 or pixels[j][1] != 0 or pixels[j][2] != 0:
                allOff = 0
            else:
                allOff = 1
            pixels[j] = (int(pixels[j][0] * (dim/200)), int(pixels[j][1] * (dim/200)), int(pixels[j][2] * (dim/200)))
        pixels.write()
        if allOff == 1:
            break
        time.sleep(0.001)
        
    
def waitTime():
    time.sleep(7)
'''
while True:
    if(sensor):
        if(alarm_Mode):
            GPIO.output(buzzer, GPIO.HIGH)
            pixels.fill(255,0,0)
        else:
            alt_color(rgb_color)
'''