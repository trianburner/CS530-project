import time
import machine
import neopixel

SLEEP_TIME = 1
rgb_color = [(0,0,255),(255, 0 ,0)]

class PixelStrip:
    def __init__(self, data_pin, num_pixels):
        self.num_pixels = num_pixels
        self.pixels = neopixel.NeoPixel(machine.Pin(data_pin), num_pixels)
        
        self.color = (255, 255, 255)

    def wheel(self, pos):
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
    def rainbow_cycle(self):
        for j in range(255):
            for i in range(self.num_pixels):
                pixel_index = (i * 256 // self.num_pixels) + j
                self.pixels[i] = self.wheel(pixel_index & 255)
            self.pixels.write()
            time.sleep(.1)
        self.fadeOff()

    # Spreads a color accross the length of the pixels, with second color transition
    def alt_color(self):
        for x in range(self.num_pixels):
            for y in range(len(rgb_color)):
                if x < 50:
                    self.pixels[x] = rgb_color[y]
                    x = x + 1
            self.pixels.write()
            time.sleep(0.05)
        time.sleep(SLEEP_TIME)
        self.fadeOff()
        
    def color_wipe(self):
        for i in range(self.num_pixels):
            self.pixels[i] = self.color
            self.pixels.write()
            time.sleep(0.05)
        time.sleep(SLEEP_TIME)
        self.fadeOff()
        
    def alarm(self):
        for i in range(10):
            self.pixels.fill((255, 0, 0))
            self.pixels.write()
            time.sleep(0.25)
            self.pixels.fill((255, 255, 255))
            self.pixels.write()
            time.sleep(0.25)
        self.off()

    # Turns all pixels off
    def off(self):
        self.pixels.fill((0,0,0))
        self.pixels.write()
        
    # Fades all pixels off
    def fadeOff(self):
        for dim in range(200, 0, -1):
            allOff = 0
            for j in range(self.num_pixels):
                if self.pixels[j][0] != 0 or self.pixels[j][1] != 0 or self.pixels[j][2] != 0:
                    allOff = 0
                else:
                    allOff = 1
                self.pixels[j] = (int(self.pixels[j][0] * (dim/200)), int(self.pixels[j][1] * (dim/200)), int(self.pixels[j][2] * (dim/200)))
            self.pixels.write()
            if allOff == 1:
                break
            time.sleep(0.001)
            
    def run(self, preset = 0, color = (255, 255, 255)):
        if preset == 0:
            self.color = (color[0], color[2], color[1])
            self.color_wipe()
        elif preset == 1:
            self.color_wipe()
        elif preset == 2:
            self.alarm()
        elif preset == 3:
            self.rainbow_cycle()