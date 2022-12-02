import time
import machine
import neopixel
import math

SLEEP_TIME = 3
rgb_color = [(0,0,255),(255, 0 ,0)]

class PixelStrip:
    def __init__(self, data_pin, num_pixels):
        self.num_pixels = num_pixels
        self.pixels = neopixel.NeoPixel(machine.Pin(data_pin), num_pixels)
        
        self.color = (255, 255, 255)
        self.preset = 0

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
    
        # Fades all pixels off logarithmically
    def fadeOff(self):
        for i in range(99, 10, -1):
            allOff = 0
            multiplier = math.log10(i/10)
            
            for j in range(self.num_pixels):
                self.pixels[j] = tuple(int(multiplier * elem) for elem in self.pixels[j])
                if self.pixels[j] != (0, 0, 0):
                    allOff = 0
                else:
                    allOff = 1
                    
            self.pixels.write()
            if allOff == 1:
                self.off()
                break
            time.sleep(0.0025)
            
    def fadeOn(self, color):
        for i in range(11, 100, 1):
            allOn = 0
            multiplier = math.log10(i/10)
            
            for j in range(self.num_pixels):
                if self.pixels[j] == color[j]:
                    allOn = 1
                else:
                    pass
                self.pixels[j] = tuple(int(multiplier * elem) for elem in color[j])
                
            self.pixels.write()
            if allOn == 1:
                break
            time.sleep(0.0025)

    # Cycles the rainbow accross the length of the pixels
    def rainbow_cycle(self):
        init_color = [0] * self.num_pixels      
        for i in range(self.num_pixels):
            pixel_index = (i * 256 // self.num_pixels) + 0
            init_color[i] = self.wheel(pixel_index & 255)
        self.fadeOn(init_color)
        time.sleep(.025)
    
        for j in range(1, 255, 1):
            for i in range(self.num_pixels):
                pixel_index = (i * 256 // self.num_pixels) + j
                self.pixels[i] = self.wheel(pixel_index & 255)
            self.pixels.write()
            time.sleep(.025)
        self.fadeOff()

    # Spreads a color accross the length of the pixels, with second color transition
    def alt_color(self):
        for x in range(self.num_pixels):
            for y in range(len(rgb_color)):
                if x < self.num_pixels:
                    self.pixels[x] = rgb_color[y]
                    x = x + 1
                    
            self.pixels.write()
            time.sleep(0.025)
            
        time.sleep(SLEEP_TIME)
        self.fadeOff()
        
    def color_wipe(self):
        for i in range(self.num_pixels):
            for j in range(2):
                multiplier = math.log10(10/(1 + i))
                if i + j < self.num_pixels:
                    self.pixels[i + j] = tuple(int(multiplier * elem) for elem in self.color)
            self.pixels.write()
            time.sleep(0.025)
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
        
    def set_color(self, color):
        self.color = (color[0], color[2], color[1])
        self.pixels.fill((self.color[0], self.color[1], self.color[2]))
        self.pixels.write()
        time.sleep(1)
        self.off()
        
    def set_preset(self, preset):
        self.preset = preset
        self.run()
        
    def client_connected(self):
        for i in range(3):
            self.pixels.fill((0, 0, 255))
            self.pixels.write()
            time.sleep(0.25)
            self.off()
            time.sleep(0.25)
        time.sleep(1)
        
    def run(self):
        if self.preset == 0:
            self.color_wipe()
        elif self.preset == 1:
            self.rainbow_cycle()
        elif self.preset == 2:
            self.alt_color()