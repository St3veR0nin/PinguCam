import pygame
import pynput, sys, os, time
from pynput.mouse import Controller
from pynput.keyboard import Listener
from screeninfo import get_monitors
from _thread import start_new as thread
import pyaudio
from array import array
import cv2
from gaze_tracking import GazeTracking



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
        
        self.gaze = GazeTracking()
        self.webcam = cv2.VideoCapture(0)
        
        self.x = 0
        self.y = 0
        self.keyboard_press = False

        self.isTalking = False
    
        self.eye_horizontal_ratio = 0.0
        self.eye_vertical_ratio = 0.0


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

    
    def voice_handler(self):

        CHUNK_SIZE = 1024
        MIN_VOLUME = 150

        BUF_MAX_SIZE = CHUNK_SIZE * 10


        stream = pyaudio.PyAudio().open(
                format=pyaudio.paInt16,
                channels=2,
                rate=44100,
                input=True,
                frames_per_buffer=1024,
            )

        while self.Start:

            chunk = array('h', stream.read(CHUNK_SIZE))
            vol = max(chunk)
            if vol >= MIN_VOLUME:
                self.isTalking = True
            else:
                self.isTalking = False


    def eye_tracker(self):
        
        while self.Start:

            _, frame = webcam.read()
            gaze.refresh(frame)

            hr, vr =  gaze.horizontal_ratio(), gaze.vertical_ratio()
            if hr != None and vr != None:
                self.eye_horizontal_ratio = hr
                self.eye_vertical_ratio = vr

                #gaze.pupil_left_coords()
                #gaze.pupil_right_coords()
                # If not None, the return value of these functions represents the current coords of the pupils.


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

        self.MOUTH_OPEN = pygame.image.load(os.path.join("images", "mouth_open.png"))
        self.MOUTH_OPEN.convert_alpha()

        self.PUPIL = pygame.image.load(os.path.join("images", "pupil.png"))


        # Mousepad coordinates
        self.TOP_LEFT = 210, 175 
        self.TOP_RIGHT= 155, 160
        self.BOTTOM_LEFT = 245, 165
        self.BOTTOM_RIGHT = 170, 140
        self.remap = lambda x, amin, amax, bmin, bmax: (x - amin) * (bmax - bmin) / (amax - amin) + bmin

        #eyes rectangles coordinates

        self.LE_TOP_LEFT = 365, 45
        self.LE_TOP_RIGHT = 345, 45
        self.LE_BOTTOM_LEFT = 365, 65
        self.LE_BOTTOM_RIGHT = 345, 65 

        self.RE_TOP_LEFT = 300, 35
        self.RE_TOP_RIGHT = 290, 35
        self.RE_BOTTOM_LEFT = 300, 55
        self.RE_BOTTOM_RIGHT = 290, 55 



    def remap_mousepad(self, x, y):
        ya = self.remap(y, 0, self.height, self.TOP_LEFT[0], self.BOTTOM_LEFT[0]), self.remap(y, 0, self.height, self.TOP_LEFT[1], self.BOTTOM_LEFT[1])
        yb = self.remap(y, 0, self.height, self.TOP_RIGHT[0], self.BOTTOM_RIGHT[0]), self.remap(y, 0, self.height, self.TOP_RIGHT[1], self.BOTTOM_RIGHT[1])
        return self.remap(x, 0, self.width, ya[0], yb[0]), self.remap(x, 0, self.width, ya[1], yb[1])




    def start(self):
        self.Start = True
        self.init()

        thread(self.keyboard_input_handler, ())

        thread(self.voice_handler, ())

        thread(self.eye_tracker, ())


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

            #Blit the pupils according to coords or horizontal/vertical ratio...
            #self.display.blit(self.PUPIL, ())
            #self.display.blit(self.PUPIL, ())

            if self.isTalking:
                self.display.blit(self.MOUTH_OPEN, (280,55))

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
