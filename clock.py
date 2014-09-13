import pygame
import time
from common import *

# Provides clock and chime functions

class Clock():

    def __init__(self,chChime,chGong):

        # CHIME VARIABLES
        # Pygame mixer channels must be reserved. Calling routine must setup channels
        # using pygame.mixer.Channel(x). Provide those channel references.
        self.chChime = chChime
        self.chGong = chGong
        # Interval at which chimes play
        self.chimeInterval=30      #0=disabled, 15=quarter hour, 30=half hour, 60=hourly
        # What hours of the day can chimes play?
        self.chimeHourStart = 5    #Hour at which chimes can start to play (1=1:00am)
        self.chimeHourEnd = 24     #Last hour at which chimes can play (24=midnight)
        # After chimes play, should gongs sound the hour?
        # 3-gong splits day into 4 3-hour segments...
        # ...sounds three times at 3,6,9,12, once at 1,4,7,9, twice at 2,5,8,10
        self.gongPref = 3  #0=disable, 3=3 gong, 12=12 hour count

        # Load chime sounds
        self.sndChimeShort = pygame.mixer.Sound(SOUNDS_DIR+'ChimeShort.wav')
        self.sndChimeMedium = pygame.mixer.Sound(SOUNDS_DIR+'ChimeMedium.wav')
        self.sndChimeLong = pygame.mixer.Sound(SOUNDS_DIR+'ChimeMedium.wav')
        self.sndChimeBday = pygame.mixer.Sound(SOUNDS_DIR+'happybday.wav')
        #
        self.sndChimePref = 1  # Hourly chime preference 0=Short, 1=Medium, 2=Long

        # GONG VARIABLES
        # Load gong sounds
        self.sndGongs = []   # 1 through 12 will be loaded, 0 will be empty
        for n in range(0,13):
            self.sndGongs.append(pygame.mixer.Sound(SOUNDS_DIR+str(n)+"gong.wav"))
        self.gongTime = 0    #Time when gongs should start
        self.gongCount = 0   #Number of gongs to play

        self.chimeVolume = 0.3   # Chime/Gong volume - 0.0 to 1.0
        self.setVolume(self.chimeVolume)


    # Set volume of chimes and gongs. Volume values between 0.0 (silent) and 1.0 (full)
    def setVolume(self,vol):
        self.chimeVolume = vol
        self.sndChimeShort.set_volume(vol)
        self.sndChimeMedium.set_volume(vol)
        self.sndChimeLong.set_volume(vol)
        self.sndChimeBday.set_volume(vol)
        for n in range(1,4):
            self.sndGongs[n].set_volume(vol)

    # Get the current chime/gong volume
    def getVolume(self):
        return self.chimeVolume



    # Determine if chime needs to play and start it, if time.
    # Current time, chime hours, chime interval are used to make decisison.
    # Chime is initiated based on full, half or quarter hour.
    # 
    def _checkChime(self):
        if self.chimeInterval > 0 and hasTimeChanged("chime"):  #if chimes are enabled and time has changed
            # Are we within start/end hour range
            hour = int(time.strftime("%H"))         # Hour in military (0-23)
            if hour >= self.chimeHourStart:      # On or after Start
                if (hour <= self.chimeHourEnd) or (hour == 0 and self.chimeHourEnd == 24):  # and on or before End
                    # Check minutes to see if chime should sound
                    mins = int(time.strftime("%M"))
                    if mins == 0:
                        self._startChime(hour,mins)
                    elif self.chimeInterval < 60 and mins == 30:  #Interval is 30 or 15 and its half-past the hour
                        self._startChime(hour,mins)
                    elif self.chimeInterval == 15 and (mins == 15 or mins == 45): #Interval is quarter-hour, and time is at quarter.
                        self._startChime(hour,mins)
                                

    # Begin the chime.  Minutes and ChimePref determine length of chime to play.
    # If at top of the hour, then gongs will be scheduled to play based on GongPref.
    # Call refresh() at least once per second to have gongs initiate.
    #
    def _startChime(self,hour,mins):                           
        #Top of the hour?  Chime and gong, as appropriate
        if mins == 0:
            #Birthday today?
            dt = time.strftime("%m%d")
            if dt == "0723" or dt == "0818" or dt == "0215" or dt=="0423":
                self.chChime.play(self.sndChimeBday)
                self.gongTime = time.time() + 13
            else:
                # select lead-in chime and set a delay time for gong
                
                if self.sndChimePref == 0:
                    self.chChime.play(self.sndChimeShort)
                    self.gongTime = time.time() + 6
                    
                elif self.sndChimePref == 1:
                    self.chChime.play(self.sndChimeMedium)
                    self.gongTime = time.time() + 10
                    
                else:
                    self.chChime.play(self.sndChimeLong)
                    self.gongTime = time.time() + 10
                    
            # select number of gongs
            if self.gongPref == 3:
               self.gongCount = (hour + 2) % 3 + 1
               
            elif self.gongPref == 12:
                self.gongCount = (hour + 12) % 12 + 1
                
            else:
                self.gongTime=0
                self.gongCount=0
                
        #Half-past the hour? Sound appropriate chime            
        elif mins == 30: 
            if self.sndChimePref == 0:
                self.chChime.play(self.sndChimeShort)
            else:
                self.chChime.play(self.sndChimeMedium)
                
        #Must be quarter-hour, play short chime        
        else:
            self.chChime.play(self.sndChimeShort)

    # Chime and gong processing.  Call at lest once every second.
    def refresh(self):
        # Have we reached a scheduled Gong time?
        if self.gongCount > 0 and self.gongTime > 0 and time.time() > self.gongTime:
            self.chGong.play(self.sndGongs[self.gongCount])
            self.gongCount = 0
            self.gongTime = 0
        else:
            # Otherwise, check to see if it is time to chime
            self._checkChime()
