import pygame
from common import *
#import yahooweather
import openweather
import icons
import time

class WeatherTile():

    def __init__(self):
        self.emptyTile = pygame.image.load(BACKGROUNDS_DIR + 'blank.png')
        self.tile = self.emptyTile.copy()
        pygame.transform.scale(self.emptyTile,TILE_SIZE)

        # Load weather codes and images
        #self.icons,self.codes = icons.loadWeatherCodes(ICONS_DIR)
        self.images = icons.loadWeatherCodes(ICONS_DIR)

        # setup weather object

        self.weather = openweather.Weather()
        self.UPDATE_INTERVAL = 15    #Minutes between weather update pulls
        self.nextUpdate = 0          #Timestamp for next pull (0 forces immediate pull)

        self.paintThread = Thread('')  #Empty thread, ready for use.
        self.fetchSuccess = False      #True if the weather fetch was successful
 
    def refresh(self):
        if self.nextUpdate < time.time():
            self.weather.fetch()
            

    # React to any screen touches
    def processTouch(self,x,y):
        pass
    
    # Build tile based on weather and return painted surface
    def _paint(self):
        # time to fetch the weather?
        if time.time() > self.nextUpdate:
            self.fetchSuccess = self.weather.fetch()
            with threadLock:
                if self.fetchSuccess:
                    # Success - No need to fetch again for a while
                    self.nextUpdate = time.time() + 60 * self.UPDATE_INTERVAL
                else:
                    # Failed - Try again in 10 seconds. Skip painting.
                    self.nextUpdate = time.time() + 60
        # If we got weather data, paint the tile.
        if self.fetchSuccess:
            # Start with an empty tile
            tile = self.emptyTile.copy()
            # Show current weather icon
            """
            daytime = self.weather.current['daytime']
            if daytime:
                img = self.images[self.weather.current['imageday']]
            else:
                img = self.images[self.weather.current['imagenight']]
            """
            img = self.images[self.weather.current['image']]
            tile.blit(img,(0,15))
            # Show current temp
            text = str(self.weather.current['temp'])
            textAt(432,33,text,tile,fontGiant,BLACK,RIGHT)
            textAt(430,30,text,tile,fontGiant,WHITE,RIGHT)
            textAt(432,68,"O",tile,fontLarge,BLACK)
            textAt(430,65,"O",tile,fontLarge)
            # Show weather description text
            text = self.weather.current['description']
            x,y = textAt(35,232,text,tile,fontMedium)
            if self.weather.current['windchill'] != self.weather.current['temp']:
                newx,newy = textAt(35,285,"Feels like ",tile,fontSmall)
                text = str(self.weather.current['windchill']) + u'\u00B0'
                textAt(newx,275-7,text,tile,fontLarge)
            # Show Wind direction and speed
            if self.weather.current['windspeed'] == '0':
                newx,newy = textAt(465,232,'Calm',tile,fontMedium,WHITE,RIGHT)
            else:
                text =  str(self.weather.current['windspeed'])
                if self.weather.units == "imperial":
                    newx,newy = textAt(465,239,' mph',tile,fontSmall,WHITE,RIGHT)
                else:
                    newx,newy = textAt(465,239,' kph',tile,fontSmall,WHITE,RIGHT)                    
                newx,newy = textAt(newx,222,text,tile,fontLarge,WHITE,RIGHT)
                text = compass(self.weather.current['winddirection'])
                textAt(465,newy,text,tile,fontMedium,WHITE,RIGHT)
            # Show low and high temps
            starty = 330
            startx = 20
            shade(startx+5,starty+4,90*5-5,36,tile,BLACK,60)
            for i in range(0,5):
                centerx = startx + 45 + i * 90
                f = self.weather.forecasts[i]
                text = f['dow']
                x,y = textAt(centerx,starty,text,tile,fontMedium,WHITE,CENTER)
                # Show icon
                imgFile = 'sml'+ f['image']
                img = self.images[imgFile]
                tile.blit(img,(centerx-25,y))
                # High and Low temps
                y += 50
                text = str(f['hightemp']) + u'\u00B0'
                x,y = textAt(centerx+5,y,text,tile,fontLarge,WHITE,CENTER)
                text = str(f['lowtemp']) + u'\u00B0'
                textAt(centerx+5,y,text,tile,fontMedium,WHITE,CENTER)
            # Show last update info
            # text = self.weather.info('title')
            # text = text[15:]    #remove 'Conditions for ' from front of text
            # textAt(250,530,text,tile,fontTiny,GREY,CENTER)

            # Tile complete, now share the result
            with threadLock:
                self.tile = tile.copy()

    # Is paint thread running?
    def running(self):
        return self.paintThread.isAlive()

    # If we need to update the tile start a thread to paint it and return current tile
    def paint(self):
        # is it time to get a weather update?
        if time.time() > self.nextUpdate:
            # if we aren't running a thread to get weather, start one.
            if not self.running():
                self.paintThread = Thread(self._paint)
                self.paintThread.start()
        # return the current weather tile     
        with threadLock:
            return self.tile

    """        
    # Daytime calculation based on sunrise/sunset
    def dayTime(self):
        try:
            daystart = time2hours(self.weather.astronomy('sunrise'))
            dayend = time2hours(self.weather.astronomy('sunset'))
            now = time2hours(time.strftime('%I:%M %p'))
            if now >= daystart and now <= dayend:
                dayTime = True
            else:
                dayTime = False
            return dayTime
        except:
            return True
    """
    
    # Returns medium-sized icon image for current conditions and time of day
    def icon(self):
        try:
            img = self.images[self.weather.current['image']]
            img = pygame.transform.scale(img,(80,80))
            return img
        except:
            return None


    #
    def temperature(self):
        try:
            return int(self.weather.current['temp'])
        except:
            return None

    """

    # Returns current temperature as text
    def temperature(self):
        try:
            text = str(self.weather.current('temp'))
            return text
        except:
            return None


"""

"""
# test
pygame.init()
scr = pygame.display.set_mode(DISPLAY_RES)
img = pygame.image.load(BACKGROUNDS_DIR+'BlueSweep.png').convert()
scr.blit(img,(0,0))
img = pygame.image.load(BACKGROUNDS_DIR+'sidebyside.png')
scr.blit(img,(0,0))
pygame.display.update()
time.sleep(2)
background = scr.copy()

w=WeatherTile()

try:
    while True:
        scr.blit(background,(0,0))
        #shade(530,40,452,520,scr,(0,0,70),80)

        tile = w.paint()

        offset = time.time() * 60 % 200   

        fade = scr.subsurface((512,0,512,600)).copy()
        fade.set_alpha(offset)
        fade.blit(tile,(0,0))
        scr.blit(fade,(512,0))

        pygame.display.update()

        time.sleep(1.0/60)
finally:
    pygame.display.quit()
    pygame.quit()
"""
