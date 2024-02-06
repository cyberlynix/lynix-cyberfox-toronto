from is31fl3737 import is31fl3737
from touch import TouchController
from random import random
import time
import gc

class animation_rainbow_down:
    def __init__(self, badge):
        self.badge = badge
        self.offset = 0.0
    
    def update(self):
        self.offset -= 0.5
        for i in range(48):
            self.badge.disp.downward[i].hsv(self.badge.pallet[int(1024*(i+self.offset)/100)&0x3FF][0], 1.0, 100)
            
def pallet_rainbow(target):
    for i in range(len(target)):
        target[i][0] = i/len(target)
        target[i][1] = 1.0
        target[i][2] = 255

class badge(object):
    def __init__(self):
        # Display
        self.disp = is31fl3737()
        
        # Pallet
        self.pallet = [[0.0,0.0,0.0] for i in range(1024)]
        self.offset = 0.0
        self.pallet_index = 0
        self.pallet_functions = [pallet_rainbow]
        self.pallet_functions[self.pallet_index](self.pallet)
        
        # Touch Sensors
        self.touch = TouchController((4,5,6,7))
        self.touch.channels[0].level_lo = 15000
        self.touch.channels[0].level_hi = 20000
        self.touch.channels[1].level_lo = 15000
        self.touch.channels[1].level_hi = 20000
        self.touch.channels[2].level_lo = 15000
        self.touch.channels[2].level_hi = 20000
        self.touch.channels[3].level_lo = 15000
        self.touch.channels[3].level_hi = 20000
        
        self.anim_index = 0
        self.animations = [animation_rainbow_down(self)]
        
        # Variables
        self.currentConsent = True
        self.isBooped = False
        self.last_boop_time = 0
        self.boop_cooldown = 10  # Cooldown period in seconds
        
        print("Lynxes are cute!")
    
    def boop_checker(self):
        # Check if boop detected and cooldown has passed
        if (self.touch.channels[0].level > 0.3 or self.touch.channels[1].level > 0.3) and not self.isBooped:
            current_time = time.time()
            if current_time - self.last_boop_time > self.boop_cooldown:
                self.isBooped = True
                print("Boop Detected!")
                for led in self.disp.cheak1:
                    led.hsv(0/360, 1.0, 200)
                for led in self.disp.cheak2:
                    led.hsv(0/360, 1.0, 200)
                #for led in range(48):
                #    self.disp.leds[led].hsv(0/360, 1.0, 200)  # Set LEDs to red
                self.disp.update()
                time.sleep(2)
                self.isBooped = False
                self.last_boop_time = current_time  # Update last boop time
                
    def consent_change(self):
         if (self.touch.channels[2].level > 0.3):
             self.currentConsent = True
             print("True")
         if (self.touch.channels[3].level > 0.3):
             self.currentConsent = False
             print("false")
        
    def update(self, *args):
        #for led in range(48):
        #    if self.currentConsent == True:
        #        self.disp.downward[led].hsv(self.pallet[int(1024*(led+self.offset)/100)&0x3FF][0]/360, 1.0, 100)
        #    else:
        #       self.disp.leds[led].hsv(0/360, 1.0, 200) # Set LEDs to red
            
        if self.currentConsent == True:
            self.animations[self.anim_index].update()
        else:
            for led in range(48):
                self.disp.leds[led].hsv(0/360, 1.0, 200)
                
        self.disp.eye1.hsv(182/360, 1.0, 200)
        self.disp.eye2.hsv(122/360, 1.0, 200)
        self.disp.update()
        
        # Check if boop detected then send request to boop.lynix.ca/booped?MD5_HASH=(BadgeHash)
        self.boop_checker()
        
        self.consent_change()
        
        gc.collect()
        
    def run(self):
        while True:
            self.touch.update()
            self.update()
            time.sleep(1/60)

# Instantiate the badge and run it
global t
t = badge()
t.run()
