
import pygame
from common import *

import weathertile
import calendartile
import radiotile
import time
import os

# Combines background images with left and right tiles and refreshes display
# at a set periodic rate, when 'continuous' is called as a thread.
class Painter():

    def __init__(self,leftTile,rightTile):
        self.background=''
        self.change=True    #Schedule background to change
        self.leftTile=leftTile
        self.rightTile=rightTile

    # Set background image with overlay and save copy for normal refresh cycles
    def setBackground(self):
        img = backgrounds[backgroundIndex]
        scr.blit(img,(0,0))
        img = pygame.image.load(BACKGROUNDS_DIR+'sidebyside.png').convert_alpha()
        scr.blit(img,(0,0))
        self.background = scr.copy().convert()  #Grab a copy of this to start each future frame

    # Schedule background to change on next refresh
    def changeBackground(self):
        self.change=True

    # Assign tile to left side
    def setLeftTile(self,tile):
        self.leftTile = tile

    # Assign tile to right side
    def setRightTile(self,tile):
        self.rightTile = tile

    # Returns which tile is currently not showing
    def hiddenTile(self):
        if self.leftTile <> w and self.rightTile <> w:
            tile = w
        elif self.leftTile <> r and self.rightTile <> r:
            tile = r
        else:
            tile = c
        return tile
            
    def continuous(self):
        fpsClock=pygame.time.Clock()
        while True:
            #Has a background change been requested
            if self.change:
                self.change = False
                self.setBackground()
            else:    
                scr.blit(self.background,(0,0))
            # paint tiles on background
            scr.blit(self.leftTile.paint(),(0,0))
            #tile = w.paint()
            scr.blit(self.rightTile.paint(),(512,0))

            # Calendar/Clock tile needs to update, even in background
            if c == self.hiddenTile():
                tile = c.paint()
                # show current time in bottom-right corner
                t = c.formattedTime()
                txtImg = fontLarge.render(t,1,WHITE)
                w = txtImg.get_width()
                h = txtImg.get_height()
                recw = w*1.1
                rech = h*0.9
                shade(1024-recw,600-rech,recw,rech,scr,GREY,70)
                pygame.draw.rect(scr, WHITE, (1024-recw,600-rech,recw+3,rech+3),2)
                #textAt(1023,550,t,scr,fontLarge,BLACK,align=RIGHT)
                #textAt(1022,549,t,scr,fontLarge,WHITE,align=RIGHT)
                scr.blit(txtImg, (1023-w,600-h))

            #mx,my = pygame.mouse.get_pos()
            #s=str(mx)+", "+str(my)
            #txtImg = fontSmall.render(s,1,WHITE)
            #scr.blit(txtImg,(0,0))
            
            pygame.display.update()
            #throttle to 3 frames per second
            fpsClock.tick(3)    
            
# Init sound
pygame.mixer.init(22050,-16,1,1024)
wavChannel = pygame.mixer.Channel(1)
touched = 0   #=0 not touched, 1=touched - resets to zero when released

# Init music
musicIndex = 0
musicMax = 6

# Init the display
pygame.init()
#pygame.mouse.set_visible(False)
scr = pygame.display.set_mode(DISPLAY_RES)

# Load background images
backgroundIndex = 0
backgrounds = []
backgrounds.append(pygame.image.load(BACKGROUNDS_DIR + 'BlueSweep.png').convert())
backgrounds[len(backgrounds)-1] = pygame.transform.scale(backgrounds[len(backgrounds)-1],DISPLAY_RES)
backgrounds.append(pygame.image.load(BACKGROUNDS_DIR + 'RainbowWaves.jpg').convert())
backgrounds[len(backgrounds)-1] = pygame.transform.scale(backgrounds[len(backgrounds)-1],DISPLAY_RES)
backgrounds.append(pygame.image.load(BACKGROUNDS_DIR + 'CloudyMoon.png').convert())
backgrounds[len(backgrounds)-1] = pygame.transform.scale(backgrounds[len(backgrounds)-1],DISPLAY_RES)
backgrounds.append(pygame.image.load(BACKGROUNDS_DIR + 'GreenFabric.png').convert())
backgrounds[len(backgrounds)-1] = pygame.transform.scale(backgrounds[len(backgrounds)-1],DISPLAY_RES)
backgrounds.append(pygame.image.load(BACKGROUNDS_DIR + 'BlueLeaf.jpg').convert())
backgrounds[len(backgrounds)-1] = pygame.transform.scale(backgrounds[len(backgrounds)-1],DISPLAY_RES)
backgrounds.append(pygame.image.load(BACKGROUNDS_DIR + 'StarField.png').convert())
backgrounds[len(backgrounds)-1] = pygame.transform.scale(backgrounds[len(backgrounds)-1],DISPLAY_RES)
backgrounds.append(pygame.image.load(BACKGROUNDS_DIR + 'BlackLeather.jpg').convert())
backgrounds[len(backgrounds)-1] = pygame.transform.scale(backgrounds[len(backgrounds)-1],DISPLAY_RES)
backgrounds.append(pygame.image.load(BACKGROUNDS_DIR + 'OrangeGlow.jpg').convert())
backgrounds[len(backgrounds)-1] = pygame.transform.scale(backgrounds[len(backgrounds)-1],DISPLAY_RES)
backgrounds.append(pygame.image.load(BACKGROUNDS_DIR + 'BlackCube.jpg').convert())
backgrounds[len(backgrounds)-1] = pygame.transform.scale(backgrounds[len(backgrounds)-1],DISPLAY_RES)
backgrounds.append(pygame.image.load(BACKGROUNDS_DIR + 'BrownLeaves.jpg').convert())
backgrounds[len(backgrounds)-1] = pygame.transform.scale(backgrounds[len(backgrounds)-1],DISPLAY_RES)
backgrounds.append(pygame.image.load(BACKGROUNDS_DIR + 'Wave.png').convert())
backgrounds[len(backgrounds)-1] = pygame.transform.scale(backgrounds[len(backgrounds)-1],DISPLAY_RES)
backgrounds.append(pygame.image.load(BACKGROUNDS_DIR + 'GreenLeather.png').convert())
backgrounds[len(backgrounds)-1] = pygame.transform.scale(backgrounds[len(backgrounds)-1],DISPLAY_RES)
# Init tiles
w=weathertile.WeatherTile()
c=calendartile.CalendarTile()
r=radiotile.RadioTile()
uiClock = pygame.time.Clock()  #Foreground user interface clock

# Continuously paint the display in a thread
painter=Painter(r,w)  
painterThread = Thread(painter.continuous)
painterThread.start()

done = False
try:
    while not done:
        # Build the Screen
        
        # sample code to fade in 'tile' using alpha channel
        #offset = time.time() * 60 % 200 + 55   
        #fade = scr.subsurface((512,0,512,600)).copy()
        #fade.set_alpha(offset)
        #fade.blit(tile,(0,0))
        #scr.blit(fade,(512,0))


        
        # Get mouse position
        mx,my = pygame.mouse.get_pos()
        # touch screen will trigger left mouse press
        if pygame.mouse.get_pressed()[0]:
            # Is this touch just starting?  Then process it.
            if touched == 0:
                wavChannel.set_volume(0.3)
                wavChannel.play(pygame.mixer.Sound(SOUNDS_DIR+'click.wav') )
                touched = 1
                #calibrate input to touch screen
                tx = int(mx * 1.11)
                ty = int(600 - my)
                #if touched in lower right corner, exit
                if tx > 950 and ty > 525:
                    done = True
                #if center is pressed, change background image
                elif tx >= 450 and tx <= 560 and ty > 250 and ty < 350:
                    backgroundIndex = (backgroundIndex + 1) % len(backgrounds)
                    painter.changeBackground()
                #if left border touch, swap tile
                elif tx <= 40:
                    painter.setLeftTile(painter.hiddenTile())
                #if right border touch, swap tile
                elif tx >= 984:
                    painter.setRightTile(painter.hiddenTile())
                # Left tile touched?
                elif touched == 1 and tx > 40 and tx <= 511:
                    painter.leftTile.processTouch(tx,ty)
                # Right tile touched?
                elif touched == 1 and tx >= 512 and tx < 984:
                    painter.rightTile.processTouch(tx-512,ty)
        else:
            touched = 0

        # Process Keyboard input
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_DOWN]:
                    backgroundIndex = (backgroundIndex + 1) % len(backgrounds)
                    painter.changeBackground()
                if keys[pygame.K_q]:
                    done = True
                if keys[pygame.K_UP]:
                    backgroundIndex = (backgroundIndex + 1) % len(backgrounds)
                    painter.changeBackground()


        # Throttle loop to 15 frames per second
        uiClock.tick(15)
        #s="fps:"+str(uiClock.get_fps())
        #txtImg = fontSmall.render(s,1,WHITE)
        #scr.blit(txtImg,(0,0))


        
        
finally:
    os.system('mpc stop')
    pygame.display.quit()
    pygame.quit()




        
        
