import pygame
from common import *

class Fullscreen():

    def __init__(self,calendarTile,weatherTile,radioTile):
        self.calendarTile = calendarTile
        self.weatherTile = weatherTile
        self.radioTile = radioTile
        #
        self.emptyScreen = pygame.image.load(BACKGROUNDS_DIR + 'blank.png')
        pygame.transform.scale(self.emptyScreen,DISPLAY_RES)
        self.screen = self.emptyScreen.copy() #painted screen is stored here
        

    # React to any screen touches
    def processTouch(self,x,y):
        pass

    
    # Build screen using clock, weather and radio information
    def _paint(self):
        # Start with an empty screen
        screen = self.emptyScreen.copy()
        # Determine x coordinate to right-align time to
        t = self.calendarTile.formattedTime()
        if len(t) == 4:  #if one-digit hour
            x = 887
        else:
            x = 950
        # Show current time as a huge font
        # Show it parital brightness and then show again with or without ":"
        textAt(x,107,t,screen,fontFullscreen,WHITE,RIGHT,alpha=150)
        if int(time.time()) % 2 == 0:   # Flash ':' every other second
            t = t.replace(":"," ")
        textAt(x,107,t,screen,fontFullscreen,WHITE,RIGHT,alpha=80)
        # Show day of week just above time
        t = self.calendarTile.dow()
        textAt(x-25,128,t,screen,fontVeryLarge,WHITE,RIGHT,alpha=200)
        # Show temp in upper-right
        text = self.weatherTile.temperature()
        if text <> None:
            #textAt(1006,-6,text,screen,fontVeryLarge,BLACK,RIGHT)
            textAt(1006,-8,text,screen,fontVeryLarge,WHITE,RIGHT)
            #textAt(1006,-9,"o",screen,fontMedium,BLACK)
            textAt(1006,-11,"o",screen,fontMedium,WHITE)
        # Show weather icon in lower-right
        img = self.weatherTile.icon()
        if img <> None:
            screen.blit(img,(940,519))
        # Show radio icon in lower-left
        screen.blit(self.radioTile.icon(),(0,536))
        # Show artist and title, if playing
        t = self.radioTile.artist_song()
        textAt(72,548,t,screen,fontMedium,WHITE)
        # Show date in top-left
        rec = pygame.surface.Surface((77,30))
        rec.fill(RED)
        rec.set_alpha(100)
        screen.blit(rec,(0,0))

        rec = pygame.surface.Surface((77,52))
        rec.fill(WHITE)
        rec.set_alpha(200)
        screen.blit(rec,(0,31))

        text = time.strftime('%b')  #Month name
        textAt(37,-4,text,screen,fontSmall,WHITE,CENTER)
        text = str(int(time.strftime('%d')))  #Day without leading zero 
        textAt(37,27,text,screen,fontLarge,BLACK,CENTER)
        # Show the upcoming calendar event at the top of the screen
        textAt(100,0,self.calendarTile.nextEvent(),screen,fontMedium,WHITE)
        # Paint complete, now share the result
        with threadLock:
            self.screen = screen.copy()

    # If we need to update the tile start a thread to paint it and return current tile
    def paint(self):
        # if we aren't running a _paint thread, start one.
        if not 'paintThread' in locals() or not paintThread.isAlive():
             paintThread = Thread(self._paint)
             paintThread.start()
        # return the current weather tile          
        with threadLock:
            return self.screen

            
