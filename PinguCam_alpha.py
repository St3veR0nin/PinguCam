import pygame, threading
import pynput, sys, os, time
from pynput.mouse import Controller
from pynput.keyboard import Listener
from screeninfo import get_monitors



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


        self.Mouse = Controller() 
        self.mousepadSize = (60,30)

        self.isMouseMoving = False
        

        self.startX = 0
        self.startY = 0
        
        self.fx = 0
        self.fy = 0

        self.keyboard_press = False

       



    def on_mouse_move(self, x, y):
 
        self.isMouseMoving = True

        deltaX = x - self.startX
        deltaY = y - self.startY

        self.fx = (deltaX*self.mousepadSize[0])/self.width
        self.fy = (deltaY*self.mousepadSize[1])/self.height
         
        #<-- self.isMouseMoving = False
        

    def on_key_press(self, key):

        self.keyboard_press = True


    def on_key_release(self, key):

        self.keyboard_press = False


    def keyboard_input_handler(self):

        with Listener(on_press=self.on_key_press,on_release=self.on_key_release) as listener:
            with pynput.mouse.Listener(on_move=self.on_mouse_move) as mlistener:
                while self.Start == True:
                    time.sleep(1)
                    if self.isMouseMoving == False:
                        self.startX, self.startY = self.Mouse.position[0], self.Mouse.position[1]
                    else:
                        self.isMouseMoving = False #<-- Should i move it at the end of on_mouse_move()?



    def init(self):

        pygame.init()
        self.display = pygame.display.set_mode((540,205))
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




    def start(self):
        
        self.Start = True

        self.init()

        thread = threading.Thread(name="Keyboard", target=self.keyboard_input_handler)
        thread.daemon = True
        thread.start()

        mStartX = 190 # HARDCODED!
        mStartY = 155 #HARDCOED!


        while self.Start:
            

            self.display.fill(self.GREEN)
            
            if self.keyboard_press == True:
                self.display.blit(self.LAYOUT_HAND_DOWN, (0,0))
            else:
                self.display.blit(self.LAYOUT_HAND_UP, (0,0))

            #Maybe have more restriction on mStartX and mStartY?

            self.display.blit(self.MOUSE, (mStartX-self.fx, mStartY-self.fy))


            #this is just a test, i promise!
            self.display.blit(self.MOUSE_HAND, (233,135))

            pygame.display.flip()

            for event in pygame.event.get():
               
                if event.type == pygame.QUIT:

                    self.stop = False
                    sys.exit(0)


            time.sleep(0.06)


#Window keeps freezing when dragged...

app = PinguCam()
main_thread = threading.Thread(name="Main", target=app.start())
main_thread.start()