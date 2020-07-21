import pygame
import pynput, sys, os, time
from pynput.mouse import Controller
from pynput.keyboard import Listener
from screeninfo import get_monitors
from _thread import start_new as thread


class PinguCam:
    def __init__(self):
        self.Start = False
        self.GREEN = (39, 217, 42)
        self.width = 0
        self.height = 0

        for mon in get_monitors():
            self.width += mon.width
            if self.height <= mon.height:
                self.height = mon.height
        
        self.x = 0
        self.y = 0
        self.keyboard_press = False

    def on_mouse_move(self, x, y):
        self.x = x
        self.y = y
         
    def on_key_press(self, key):
        self.keyboard_press = True

    def on_key_release(self, key):
        self.keyboard_press = False

    def keyboard_input_handler(self):
        with Listener(on_press=self.on_key_press,on_release=self.on_key_release) as listener:
            with pynput.mouse.Listener(on_move=self.on_mouse_move) as mlistener:
                while self.Start:
                    pass

    def init(self):

        pygame.init()
        self.display = pygame.display.set_mode((540,205))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("PinguCam")
 
        #Test set up images, maybe add more customization options?

        self.display.fill(self.GREEN)

        self.LAYOUT_HAND_UP = pygame.image.load(os.path.join("images","layout_hand_up.png"))
        self.LAYOUT_HAND_UP.convert_alpha()
        
        self.LAYOUT_HAND_DOWN =  pygame.image.load(os.path.join("images","layout_hand_down.png"))
        self.LAYOUT_HAND_DOWN.convert_alpha()

        self.MOUSE = pygame.image.load(os.path.join("images","mouse.png"))
        self.MOUSE.convert_alpha()

        self.MOUSE_HAND = pygame.image.load(os.path.join("images","mouse_hand.png"))
        self.MOUSE_HAND.convert_alpha()

        # Mousepad coordinates
        self.TOP_LEFT = 217, 195 
        self.TOP_RIGHT= 118, 176
        self.BOTTOM_LEFT = 271, 165
        self.BOTTOM_RIGHT = 170, 140
        self.remap = lambda x, amin, amax, bmin, bmax: (x - amin) * (bmax - bmin) / (amax - amin) + bmin

    def remap_mousepad(self, x, y):
        ya = self.remap(y, 0, self.height, self.TOP_LEFT[0], self.BOTTOM_LEFT[0]), self.remap(y, 0, self.height, self.TOP_LEFT[1], self.BOTTOM_LEFT[1])
        yb = self.remap(y, 0, self.height, self.TOP_RIGHT[0], self.BOTTOM_RIGHT[0]), self.remap(y, 0, self.height, self.TOP_RIGHT[1], self.BOTTOM_RIGHT[1])
        return self.remap(x, 0, self.width, ya[0], yb[0]), self.remap(x, 0, self.width, ya[1], yb[1])

    def start(self):
        self.Start = True
        self.init()

        thread(self.keyboard_input_handler, ())

        while self.Start:
            self.display.fill(self.GREEN)
            
            if self.keyboard_press == True:
                self.display.blit(self.LAYOUT_HAND_DOWN, (0,0))
            else:
                self.display.blit(self.LAYOUT_HAND_UP, (0,0))

            #Maybe have more restriction on mStartX and mStartY?
            m = self.remap_mousepad(self.x, self.y)
            self.display.blit(self.MOUSE, (m[0]-self.MOUSE.get_width()//2, m[1]-self.MOUSE.get_height()//2))

            #this is just a test, i promise!
            self.display.blit(self.MOUSE_HAND, (233,135))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop = False
                    pygame.quit()
                    sys.exit(0)
            self.clock.tick(60)


#Window keeps freezing when dragged...

app = PinguCam()
app.start()
