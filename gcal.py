import gdata.calendar.client
from datetime import date
from datetime import timedelta
import time
import collections
import sqlite3

# Convert 9 tuple to yyyy-mm-dd hh:mmAM format - defaults to current time
def strTime(timetuple = None):
    if timetuple == None:
        timetuple = time.gmtime()
    return time.strftime("%Y-%m-%d %H:%M%p",timetuple)            


class GCal():

    def __init__(self,user,pw):
        self.user = user
        self.pw = pw
        self.startDate = str(date.today())
        self.endDate = str(date.today() + timedelta(60))  #60 days from today
        self.sql3 = sqlite3.connect(':memory:')
        self.sql3.execute('''CREATE TABLE events (title,desc,allday,starttime,startdow,startday,startmon,startmonth,startyear, 
                             endtime,enddow,endday,endmon,endmonth,endyear,serialtime real,remindermins int,remindertime)''')
        self.EventRecord = collections.namedtuple('EventRecord','title,desc,allday,starttime,startdow,startday,startmon,startmonth,startyear,\
                                             endtime,enddow,endday,endmon,endmonth,endyear,serialtime,remindermins,remindertime')
        

    def connect(self):
        self.client = gdata.calendar.client.CalendarClient(source='My Rasp Pi')
        self.client.ClientLogin(self.user,self.pw,self.client.source)
        self.holiday_uri = self.client.get_calendar_event_feed_uri('usa__en@holiday.calendar.google.com')
        self.calQuery = gdata.calendar.client.CalendarEventQuery(start_min=self.startDate,
                                                                 start_max=self.endDate,
                                                                 sortorder='ascend',
                                                                 orderby='starttime')



    # Convert google time format to Python struct_time format
    def parseTime(self,googletime):
        if len(googletime)>10:   #Longer the 10 chars if time is included in string
            allday = False
            tfmt = time.strptime(googletime[0:19],'%Y-%m-%dT%H:%M:%S')
            tm = time.strftime('%Y-%m-%d %I:%M%p',tfmt)
        else:
            allday = True
            tfmt = time.strptime(googletime,'%Y-%m-%d')
            tm = ''
          
        dow = time.strftime('%a',tfmt)
        day = tfmt.tm_mday  #int day
        mon = tfmt.tm_mon  #int month
        month = time.strftime('%b',tfmt)   #month abbreviation
        year  = tfmt.tm_year
        serialtime = time.mktime(tfmt)
        return allday,tm,dow,day,mon,month,year,serialtime


    # Read events from calendar
    def getEvents(self):

        calendarUris = ['','8tmnrh2n4eg2skmm064fo91898%40group.calendar.google.com','usa__en@holiday.calendar.google.com']
        for calUri in calendarUris:
            if calUri == '':
                uri = ''
            else:
                uri = self.client.get_calendar_event_feed_uri(calUri)
            feed = self.client.GetCalendarEventFeed(uri=uri,q=self.calQuery)
            for entry in feed.entry:
                when = entry.when[0]
                startallday,starttime,startdow,startday,startmon,startmonth,startyear,serialtime = self.parseTime(when.start)
                endallday,endtime,enddow,endday,endmon,endmonth,endyear,endserialtime = self.parseTime(when.end)
                remindermins = 0
                remindertime = ''
                if len(when.reminder) > 0:
                    if when.reminder[0].method == 'alert':
                        remindermins = int(when.reminder[0].minutes)
                        remindertuple = time.localtime(serialtime - (remindermins * 60))
                        remindertime = time.strftime("%Y-%m-%d %I:%M%p",remindertuple)
                self.sql3.execute("INSERT INTO events VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                                  (entry.title.text,entry.content.text,startallday,starttime,startdow,startday,startmon, \
                                  startmonth,startyear,endtime,enddow,endday,endmon,endmonth,endyear,serialtime,remindermins,remindertime)
                                  )

        self.sql3.commit()
        # Select events in time seq order that in the future or recently past (within the past 2 minutes)
        cursor = self.sql3.execute("SELECT * FROM events WHERE serialtime > "+str(time.time() - 120)+ \
                                   " AND title NOT IN ('Christmas Eve','New Year''s Eve') ORDER BY serialtime")
        events = map(self.EventRecord._make, cursor.fetchall())
        self.sql3.execute("DELETE FROM events")
        return events







""" TESTING
gc = GCal('username','password')
gc.connect()
events = gc.getEvents()
for event in events:
    print event.startmonth,event.startday,event.title,event.allday,event.starttime,event.startmon,event.startday,event.startyear
"""


