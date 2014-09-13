
import pygame
from common import *

import clock
import weathertile
import calendartile
import radiotile
import fullscreen
import time
import os

#mouse or touchscreen mode?
if os.name == "nt":
    MOUSE = True   
else:
    MOUSE = False

MODE = "fullscreen"   #Mode is either 'tiled' or 'fullscreen'

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
        if MODE == 'tiled':
            img = pygame.image.load(BACKGROUNDS_DIR+'sidebyside.png').convert_alpha()
        else:
            img = pygame.image.load(BACKGROUNDS_DIR+'blackbars.png').convert_alpha()
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
        if self.leftTile <> weather and self.rightTile <> weather:
            tile = weather
        elif self.leftTile <> radio and self.rightTile <> radio:
            tile = radio
        else:
            tile = calendar
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
            if MODE == 'tiled':
                scr.blit(self.leftTile.paint(),(0,0))
                scr.blit(self.rightTile.paint(),(512,0))
            else:
                scr.blit(fullscreen.paint(),(0,0))
                weather.paint()  # Keep weather information updated

            # Calendar/Clock tile needs to update, even in background
            if calendar == self.hiddenTile() or MODE == 'fullscreen':
                tile = calendar.paint()
                # show current time in bottom-right corner
                if MODE == 'tiled':
                    t = calendar.formattedTime()   # h:mm
                    if int(time.time()) % 2 == 0:   # Flash ':' every other second
                        t = t.replace(":"," ")
                    txtRed = fontLCDMedium.render(t,1,(243,0,0))  
                    txtPink = fontLCDMedium.render(t,1,(243,140,140))  
                    w = txtRed.get_width()
                    h = txtRed.get_height()
                    scr.blit(txtPink, (1023-w,599-h))
                    scr.blit(txtRed, (1024-w,600-h))
            
            pygame.display.update()
            #throttle to 3 frames per second
            fpsClock.tick(3)    
            
# Init sound
pygame.mixer.init(22050,-16,1,1024)
wavChannel = pygame.mixer.Channel(1)    #For UI click sound
channelChime = pygame.mixer.Channel(2)  #For chimes
channelGong = pygame.mixer.Channel(3)   #For hourly gongs

clock = clock.Clock(channelChime,channelGong)

touched = 0   #=0 not touched, 1=touched - resets to zero when released

# Init music
musicIndex = 0
musicMax = 6

# Init the display
pygame.init()

scr = pygame.display.set_mode(DISPLAY_RES)
pygame.mouse.set_visible(MOUSE)

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
backgrounds.append(pygame.image.load(BACKGROUNDS_DIR + 'BlueGraph.jpg').convert())
backgrounds[len(backgrounds)-1] = pygame.transform.scale(backgrounds[len(backgrounds)-1],DISPLAY_RES)
backgrounds.append(pygame.image.load(BACKGROUNDS_DIR + 'BlackCube.jpg').convert())
backgrounds[len(backgrounds)-1] = pygame.transform.scale(backgrounds[len(backgrounds)-1],DISPLAY_RES)
backgrounds.append(pygame.image.load(BACKGROUNDS_DIR + 'BrownLeaves.jpg').convert())
backgrounds[len(backgrounds)-1] = pygame.transform.scale(backgrounds[len(backgrounds)-1],DISPLAY_RES)
backgrounds.append(pygame.image.load(BACKGROUNDS_DIR + 'Wave.png').convert())
backgrounds[len(backgrounds)-1] = pygame.transform.scale(backgrounds[len(backgrounds)-1],DISPLAY_RES)
backgrounds.append(pygame.image.load(BACKGROUNDS_DIR + 'GreenLeather.png').convert())
backgrounds[len(backgrounds)-1] = pygame.transform.scale(backgrounds[len(backgrounds)-1],DISPLAY_RES)
backgrounds.append(pygame.image.load(BACKGROUNDS_DIR + 'JapaneseLilacs.jpg').convert())
backgrounds[len(backgrounds)-1] = pygame.transform.scale(backgrounds[len(backgrounds)-1],DISPLAY_RES)
backgrounds.append(pygame.image.load(BACKGROUNDS_DIR + 'SummerSun.png').convert())
backgrounds[len(backgrounds)-1] = pygame.transform.scale(backgrounds[len(backgrounds)-1],DISPLAY_RES)
backgrounds.append(pygame.image.load(BACKGROUNDS_DIR + 'RainDrops.jpg').convert())
backgrounds[len(backgrounds)-1] = pygame.transform.scale(backgrounds[len(backgrounds)-1],DISPLAY_RES)
# Init tiles
calendar   = calendartile.CalendarTile()
weather    = weathertile.WeatherTile()
if os.name == "nt":  #for PC, connect to networked MPD host
    radio  = radiotile.RadioTile('infocenter')
else:
    radio  = radiotile.RadioTile()
fullscreen = fullscreen.Fullscreen(calendar,weather,radio)

#Foreground user interface clock FPS clock
uiClock = pygame.time.Clock()  

# Continuously paint the display in a thread
painter=Painter(radio,weather)  
painterThread = Thread(painter.continuous)
painterThread.start()

# MAIN LOOP
done = False
try:
    while not done:
        clock.refresh()
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
                # Use mouse or touch coordinates
                if MOUSE:  #use mouse coordinates for touch
                    tx = mx
                    ty = my
                else:      #calibrate for touch panel
                    tx = int(mx * 1.11)
                    ty = int(600 - my)
                #if touched in lower right corner, exit
                if tx > 950 and ty > 525:
                    done = True
                #if touched in top-center, switch between fullscreen and tiled mode
                elif tx >= 450 and tx <= 560 and ty < 50:
                    if MODE == 'tiled':
                        MODE = 'fullscreen'
                    else:
                        MODE = 'tiled'
                    painter.changeBackground()
                #if center is pressed, change background image
                elif tx >= 450 and tx <= 560 and ty > 250 and ty < 350:
                    backgroundIndex = (backgroundIndex + 1) % len(backgrounds)
                    painter.changeBackground()
                #if left border touch, swap tile
                elif tx <= 40 and MODE == 'tiled':
                    painter.setLeftTile(painter.hiddenTile())
                #if right border touch, swap tile
                elif tx >= 984 and MODE == 'tiled':
                    painter.setRightTile(painter.hiddenTile())
                # Left tile touched?
                elif touched == 1 and tx > 40 and tx <= 511 and MODE == 'tiled':
                    painter.leftTile.processTouch(tx,ty)
                # Right tile touched?
                elif touched == 1 and tx >= 512 and tx < 984 and MODE == 'tiled':
                    painter.rightTile.processTouch(tx-512,ty)
                # Bottom-left of full screen touched?
                elif tx < 64 and ty > 540 and MODE == 'fullscreen':
                    radio.togglePlay()
        else:
            touched = 0

        # Process Keyboard input
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                wavChannel.set_volume(0.3)
                wavChannel.play(pygame.mixer.Sound(SOUNDS_DIR+'click.wav') )
                if event.key == pygame.K_PAGEDOWN:
                    backgroundIndex = (backgroundIndex + 1) % len(backgrounds)
                    painter.changeBackground()
                elif event.key == pygame.K_PAGEUP:
                    backgroundIndex = backgroundIndex - 1
                    if backgroundIndex < 0: backgroundIndex = len(backgrounds) - 1
                    painter.changeBackground()
                elif event.key == pygame.K_LEFT:
                    painter.setLeftTile(painter.hiddenTile())
                elif event.key == pygame.K_RIGHT:
                    painter.setRightTile(painter.hiddenTile())
                elif event.key == pygame.K_UP:
                    radio.volumeUp()
                elif event.key == pygame.K_DOWN:
                    radio.volumeDown()
                elif event.key == pygame.K_SPACE:
                    radio.togglePlay()
                elif event.key >=pygame.K_1 and event.key <= pygame.K_8:
                    radio.selectStation(event.key - pygame.K_1)
                elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    done = True
                elif event.key == pygame.K_m:
                    if MOUSE:
                        MOUSE = False
                    else:
                        MOUSE = True
                    pygame.mouse.set_visible(MOUSE)
                elif event.key == pygame.K_f:
                    if MODE == 'tiled':
                        MODE = 'fullscreen'
                    else:
                        MODE = 'tiled'
                    painter.changeBackground()



        # Throttle loop to 15 frames per second
        uiClock.tick(15)
        #s="fps:"+str(uiClock.get_fps())
        #txtImg = fontSmall.render(s,1,WHITE)
        #scr.blit(txtImg,(0,0))


        
        
finally:
    radio.close()
    pygame.display.quit()
    pygame.quit()




        
        
