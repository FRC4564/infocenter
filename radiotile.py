import pygame
from common import *
import icons
import time
import subprocess
import os
import mpc

class RadioTile():

    def __init__(self,MPDhost='localhost'):

        # Init an empty tile        
        self.emptyTile = pygame.image.load(BACKGROUNDS_DIR + 'blank.png').convert_alpha()
        self.tile = self.emptyTile.copy()
        pygame.transform.scale(self.emptyTile,TILE_SIZE)
        # Load radio graphics - play button, stop button, etc.
        self.images = icons.loadRadioImages(RADIO_DIR)
        # Station number is 0 through 7.
        self.station = 0
        # Music playing or stopped
        self.playing = False
        # Create client connection to MPD
        self.mpc = mpc.MPC(MPDhost)
        # Volume - 0 to 100 = 0% to 100%
        self.volume = 50
        self.mpc.setvol(self.volume)
        # Empty stations from playlist and build anew
        self.mpc.clear()
        self.stations = []  #station,url,small image,large image
        #self.loadStation('Radio Paradise','http://stream-sd.radioparadise.com:8056','RadioParadise.png')
        self.loadStation('Radio Paradise','http://stream-dc1.radioparadise.com/mp3-192','RadioParadise.png')
        #self.loadStation('Ben FM','http://1741.live.streamtheworld.com:80/WCHZFMAAC_SC','BenFM.png')
        self.loadStation('977 Comedy','http://7639.live.streamtheworld.com:80/977_COMEDY_SC','977Comedy.png')
        self.loadStation('Lone Star','http://kzps-fm.akacast.akamaistream.net/7/775/20092/v1/auth.akacast.akamaistream.net/kzps-fm','LoneStar.png')
#        self.loadStation('The Smooth Lounge','http://listen.radionomy.com/the-smooth-lounge','SmoothLounge.png')
        self.loadStation('BNR - Coffee House','http://173.192.32.199:7160','BNR-Coffee House.png')
        self.loadStation('TWiT','http://twit.am/listen','TWiT.png')
        self.loadStation('Big Classic Hits','http://bigclassichits.akacast.akamaistream.net/7/921/61098/v1/auth.akacast.akamaistream.net/bigclassichits','BigClassicHits.png')
        self.loadStation('Acoustic FM','http://listen.radionomy.com/acoustic-fm','AcousticFM.png')
        self.loadStation('WERU Blue Hill','http://stream.weru.org:80/weru-high.mp3','WERU.png')
        # Create threading variable
        self.thread = Thread('')  #Empty thread ready for use.
        # Force repaint of tile
        self.repaint = True

    # Create Radio Stations array and load icons
    def loadStation(self,title,url,image):
        imgSmall = pygame.image.load(RADIO_DIR + image).convert_alpha()
        imgLarge = pygame.transform.scale(imgSmall,(80,80))
        self.stations.append([title,url,imgSmall,imgLarge])
        # Add to play list
        self.mpc.add(url)


    # Increase volume by 10%
    def volumeUp(self):
        self.volume = self.mpc.volume + 10
        if self.volume > 100:
            self.volume = 100
        self.mpc.setvol(self.volume)
        self.repaint = True
        
    # Decrease volume by 10%
    def volumeDown(self):
        self.volume = self.mpc.volume - 10
        if self.volume < 0:
            self.volume = 0
        self.mpc.setvol(self.volume)
        self.repaint = True

    # Start/Stop playback
    def togglePlay(self):
        self.playing = not self.playing
        if self.playing:
            self.mpc.play(self.station)
        else:
            self.mpc.stop()
        self.refresh()

    # Select station (0 - 7) and start playing
    def selectStation(self,station):
        self.station = station
        self.mpc.stop()
        self.mpc.play(self.station)
        self.playing = True
        self.refresh()

    # Return icon of current station or play button
    def icon(self):
        if self.mpc.playing:
            img = self.stations[self.mpc.track][2]
        else:
            img = self.images['PlayButton']
            img = pygame.transform.scale(img,(64,64))
        return img

    # Return artist and song formatted with hyphen.  "" if not playing.
    def artist_song(self):
        if self.mpc.playing:
            if self.mpc.song == "":
                t = self.mpc.artist
            else:
                t = self.mpc.artist + " - " + self.mpc.song
        else:
            t = ""
        return t
        
    # Process the touch input (or click) at x,y relative to top left corner of tile
    def processTouch(self,x,y):
        # In Stations grid?
        if y > 190 and y <412:
            # y is within stations grid. 1st or 2nd row?
            if y < 300:
                row = 0
            else:
                row = 1
            # column?
            if x > 48 and x < 480:
                col = (x - 48) / 108
                # select the station
                self.station = row * 4 + col
                self.selectStation(self.station)
        # Play or Stop button
        elif x > 75 and x < 180 and y > 420 and y < 550:
            self.togglePlay()
        # Volume down
        elif x > 200 and x <300 and y > 420 and y < 550:
            self.volumeDown()
        # Volume up
        elif x > 360 and x < 470 and y > 420 and y < 550:
            self.volumeUp()
            

    # Paints entire tile. This should happen whenever station changes.
    def _paint(self):
        # start with empty tile
        tile = self.emptyTile.copy()
        # Shaded rectangle for Station and Song title
        shade(55,55,410,125,tile,BLACK,80)
        # Show selected station image 
        tile.blit(self.stations[self.station][3],(400,32))
        # Show two rows of 4 station buttons
        pos = 0
        for row in range(0,2):
            for col in range (0,4):
                x = col * 109 + 60
                y = row * 114 + 205
                # show station logo
                tile.blit(self.stations[pos][2],(x+7,y+7))
                # show border around station
                if pos == self.station:
                    # "Selected" tile is a bit bigger and must be offset a bit
                    tile.blit(self.images['SelectedStation'],(x-10,y-10))
                else:
                    tile.blit(self.images['UnselectedStation'],(x,y))
                # next station
                pos += 1
        # Show Play or Stop button
        if self.playing:
            tile.blit(self.images['StopButton'],(55,429))
        else:
            tile.blit(self.images['PlayButton'],(76,405))
        # Volume level
	self.volume = self.mpc.volume
	level = int(self.volume/10)
        for i in range (0,10):
            x = i * 24 + 220
            if i < level:
                tile.fill(WHITE,(x,448,12,60))
            else:
                pygame.draw.rect(tile,WHITE,(x,448,13,60),1)
        # minus sign
        pygame.draw.line(tile,WHITE,(220,526),(240,526),5)
        # plus sign
        pygame.draw.line(tile,WHITE,(425,526),(450,526),5)
        pygame.draw.line(tile,WHITE,(438,514),(438,538),5)
        # Tile complete, now share the result
        with threadLock:
            self.tile = tile.copy()


    # If we need to update the tile start a thread to paint it, but return current tile
    def paint(self):
        # Whenever play state, station, volume is changed or repaint flagged, start painting the tile
        if not self.thread.isAlive():   #As long as we don't have a thread already painting
            if self.playing <> self.mpc.playing or self.volume <> self.mpc.volume or self.station <> self.mpc.track or self.repaint:
                self.repaint = False  #This satifies a repaint request
                self.playing = self.mpc.playing
                self.volume = self.mpc.volume
                self.station = self.mpc.track
                self.thread = Thread(self._paint)
                self.thread.start()
        # return the most recently updated tile
        with threadLock:
            tile = self.tile.copy()
        # Show Radio station, Album and Song
        x,y = textAt(64,60,self.stations[self.station][0],tile,fontMedium,WHITE)
        x,y = textAt(64,y,self.mpc.artist,tile,fontSmall,WHITE)
        x,y = textAt(64,y,self.mpc.song,tile,fontSmall,WHITE)
        # return the constructed tile surface
        return tile

    # Switching channel, pausing or playing requires repaint and clearing titles
    def refresh(self):
        self.album = ''
        self.song = ''
        self.repaint = True


                
    def close(self):
	self.mpc.stop()
	self.mpc.close()
