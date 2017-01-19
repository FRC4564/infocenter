import pygame
from common import *
import time
import google


class CalendarTile():

    def __init__(self):
        self.emptyTile = pygame.image.load(BACKGROUNDS_DIR + 'blank.png')
        self.tile = self.emptyTile.copy()
        pygame.transform.scale(self.emptyTile,TILE_SIZE)
        
        self.imgAlarmBell = pygame.image.load(ICONS_DIR + 'AlarmBell.png')


        #Calendar variables
        self.credentials = google.getCredentials()
        self.calendar = google.GCal(self.credentials)     #Establish connection to Google calendar
        self.CAL_UPDATE_INTERVAL = 15     #Minutes between calendar update pulls
        self.nextCalUpdate = 0            #Timestamp for next pull (0 forces immediate pull)
        self.events = []
        
        self.paintThread = Thread('')  #Empty thread, ready for use.
    

        #Clock variables
        self.nextClockUpdate = time.time()     #Clock updates will be scheduled to run every second
        self.prevTime = ''                     #HH:MM time string.
        self.timeChange = False                #Time changed to next minute


    # Return time formatted as H:MM
    def formattedTime(self):
        t = time.strftime('%I:%M')
        if t[0:1] == '0': #remove leading zero
            t = t[1:]
        return t

    # Return day of week, long form
    def dow(self):
        t = time.strftime('%A')
        return t

    # Return the next upcoming calendar event
    # Formatted as: mm/dd eventtitle (hh:mma)
    def nextEvent(self):
        text = ""
        if len(self.events) > 0:
            e = self.events[0]
            text = str(e.startmon) + "/" + str(e.startday) + "  " + e.title
            if e.starttime <> "":
                tm = e.starttime[-7:-1].lower()
                if tm[0:1] == '0':
                    tm = tm[1:]
                text = text + " @ "+tm
        return text 
    
    # React to any screen touches
    def processTouch(self,x,y):
        pass

    # Build tile and return painted surface
    def _paint(self):

         # Start with an empty tile
        tile = self.emptyTile.copy()

        # Show time
        currTime = self.formattedTime()
        rec = pygame.surface.Surface((255,130))
        rec.fill(BLACK)
        rec.set_alpha(80)
        tile.blit(rec,(60,65))        

        #text = currTime
        #if text[0:1] == '0': #remove leading zero
        #    text = text[1:]
        #x,y = textAt(60,48,text,tile,fontHuge,WHITE)
        x,y = textAt(60,48,currTime,tile,fontHuge,WHITE)
        # Show DOW 
        x,y = textAt(70,137,self.dow(),tile,fontLarge,WHITE,LEFT)
        # Show date
        rec = pygame.surface.Surface((140,43))
        rec.fill(RED)
        rec.set_alpha(100)
        tile.blit(rec,(315,65))

        rec = pygame.surface.Surface((140,87))
        rec.fill(WHITE)
        rec.set_alpha(200)
        tile.blit(rec,(315,108))

        text = time.strftime('%b')  #Month name
        x,y = textAt(385,58,text,tile,fontLarge,WHITE,CENTER)
        text = str(int(time.strftime('%d')))  #Day without leading zero 
        x,y = textAt(385,92,text,tile,fontHuge,BLACK,CENTER)       
        

        # CALENDAR EVENTS

        # When its time, update calendar event data
        if time.time() > self.nextCalUpdate:
            try:
                self.events = self.calendar.getEvents()
            except:
                print "Calendar poll failed at "+currTime
            self.nextCalUpdate = time.time() + 60 * self.CAL_UPDATE_INTERVAL

        rec = pygame.surface.Surface((395,340))
        rec.fill(BLACK)
        rec.set_alpha(80)
        tile.blit(rec,(60,212))

        #Show each event, process reminders as necessary
        count = 0
        y = 212
        timeChanged = hasTimeChanged('events')
        for event in self.events:
            secsTill = int((event.serialtime - time.time()))
            minsTill = secsTill / 60
            # If event is set for a reminder see if it is time.
            if timeChanged and event.remindermins != 0:
                # Sound chime at reminder time and scheduled time
                t = time.strftime("%Y-%m-%d %I:%M%p",time.localtime())
                if t == event.remindertime:
                        playMP3(SND_NOTIFICATION)
                if t == event.starttime:
                        playMP3(SND_ALARM)
            # If event is due, flash red every other second
            if minsTill < event.remindermins:
                if secsTill % 2 == 0:
                    shade(60,212+count*80,395,80,tile,RED,80)
            # Date
            text = event.startdow + ', ' + event.startmonth + ' ' + str(event.startday)
            textAt(70,y,text,tile,fontMedium,WHITE)
            # Show either scheduled time or days until event
            if event.starttime == '':
                days = int(minsTill / 60 / 24)
                if days == 0:
                    text = 'Tomorrow'
                elif days > 0:
                    text = str(days)+ ' days'
                else:
                    text = 'Today'
            else:
                text = event.starttime[-7:-1].lower()
                if text[0:1] == '0':
                    text = text[1:]
            x,y = textAt(450,y,text,tile,fontMedium,WHITE,RIGHT)
            if event.remindermins > 0:
                tile.blit(self.imgAlarmBell,(x-34,y-36))
            # Title
            text = event.title[0:27]
            x,y = textAt(80,y,text,tile,fontSmall,WHITE)
            # show 4 records at most
            count += 1
            if count == 4:
                break

        # Tile complete, now share the result
        with threadLock:
            self.tile = tile.copy()


    # Is paint thread running?
    def running(self):
        return self.paintThread.isAlive()


    # If we need to update the tile start a thread to paint it and return current tile
    def paint(self):
        # is it time to get a calendar update?
        if time.time() > self.nextClockUpdate:
            # if we aren't running a thread, time to start one.
            if not self.running():      #self.calendarThread.isAlive():
                self.nextClockUpdate += 1     #Reschedule to re-occur in 1 second
                self.paintThread = Thread(self._paint)
                self.paintThread.start()
        # return the current tile          
        with threadLock:
            return self.tile

