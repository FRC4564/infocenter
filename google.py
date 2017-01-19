import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime
import time

import collections
import sqlite3

# Oath scope settings
# If modifying these scopes, delete your previously saved credentials
# client_secret.json file, within your home directory in the folder .credentials
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Infocenter'

def getCredentials():
    """ Connect to Google account using OAuth
    Returns connection object.
    """
    #See if '.credentials' folder exists and create if not
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    #Attempt to get credentials
    credential_path = os.path.join(credential_dir,'calendar.json')
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    #If no valid credentials, prepare to get them.
    #This will launch a web browser to get user authorization and show the
    #URL in the console, so that it can be entered manually into a brower.
    #The 'flow' that runs will wait for authorization to complete before continuing.
    #Untested: The --noauth_local_webserver parameter should stop browser from launching.
    if not credentials or credentials.invalid:
        #Oauth flow requires 'flags' from python to launch broswer for authorization
        import argparse
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store, flags)
    return credentials


class GCal():
    """ Connect to Google calendar service and obtains a list of visible calendars.
    Calling getEvents() will provide upto 5 future events sorted chronologically.
    
    """
    def __init__(self,credentials):
        self.credentials = credentials
        #
        # We should now have credentials...connect to calendar service
        http = self.credentials.authorize(httplib2.Http())
        self.service = discovery.build('calendar', 'v3', http=http)
        # Get a calendar list and create a list of calendarIds
        self.calendarList = self.service.calendarList().list().execute()
        self.calendarIds = []
        for item in self.calendarList.get('items'):
             self.calendarIds.append(item.get('id'))


    # Split google time string into components
    # Ignores timezone data from end of string (assumes time is local)
    # allday = True when event for a date range rather than time range
    # tm - time formatted as YYYY-MM-DD HH:MMAM
    # dow - day of week short name (Sun)
    # day - day integer
    # mon - month integer
    # month - month short name (Jan)
    # year - year intger (2015)
    # serialtime - SEconds since epoch (double)
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


    # Parse a calendars events and add them to the SQL table
    def _parseEvents(self,eventsResult):
        events = eventsResult.get('items', [])
        for event in events:
            # Parse start datetime or for all-day events, the start date.
            t = event['start'].get('dateTime',event['start'].get('date'))
            startallday,starttime,startdow,startday,startmon,startmonth,startyear,startserialtime = self.parseTime(t)
            # Parse end datetime or for all-day events, the start date.
            t = event['end'].get('dateTime',event['end'].get('date'))
            endallday,endtime,enddow,endday,endmon,endmonth,endyear,endserialtime = self.parseTime(t)
            #
            # Determine if event has reminder notification
            remindermins = 0  #Number of minutes before event start for reminder to sound
            remindertime = '' #Reminder time in "YYYY-MM-DD H:MMa" format
            # Which reminder settings apply, default or event specific.  
            reminders = eventsResult.get('defaultReminders')
            if event.get('reminders',[]) != []:
                if event.get('useDefault',True) != True:
                    reminders = event.get('reminders').get('overrides')
            # Walk through reminders and find one that is a 'popup'
            for reminder in reminders:
                if reminder.get('method') == 'popup':
                    remindermins = int(reminder.get('minutes'))
                    remindertuple = time.localtime(startserialtime - (remindermins * 60))
                    remindertime = time.strftime("%Y-%m-%d %I:%M%p",remindertuple)
                    break
            # Store the event details
            self.sql3.execute("INSERT INTO events VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                              (event['summary'],'',startallday,starttime,startdow,startday,startmon, \
                              startmonth,startyear,endtime,enddow,endday,endmon,endmonth,endyear,startserialtime,remindermins,remindertime)
                              )
        #
        self.sql3.commit()

                        

    # Read events that are upcoming (or in the past 5 minutes) from all calendars.
    # Results are stored and sorted in a collection defined as:
    #
    def getEvents(self):
        # Prepare SQL table to hold events
        self.sql3 = sqlite3.connect(':memory:')
        self.sql3.execute('''CREATE TABLE events (title,desc,allday,starttime,startdow,startday,startmon,startmonth,startyear, 
                             endtime,enddow,endday,endmon,endmonth,endyear,serialtime real,remindermins int,remindertime)''')
        self.EventRecord = collections.namedtuple('EventRecord','title,desc,allday,starttime,startdow,startday,startmon,startmonth,startyear,\
                                             endtime,enddow,endday,endmon,endmonth,endyear,serialtime,remindermins,remindertime')
        # Process each calendar
        for id in self.calendarIds:
            # get events for the calendar that are 5 mins past and forward upto 60 days
            startTime = datetime.datetime.utcnow() - datetime.timedelta(minutes=5)
            endTime = datetime.datetime.utcnow() + datetime.timedelta(days=60)
            isoStart = startTime.isoformat() + "Z"   #Google will see this a UTC
            isoEnd = endTime.isoformat() + "Z"
            eventsResult = self.service.events().list(
                calendarId=id ,timeMin=isoStart, timeMax=isoEnd, maxResults=5, singleEvents=True,
                orderBy='startTime', fields='defaultReminders,items(description,end,reminders,start,summary)').execute()
            #print eventsResult
            self._parseEvents(eventsResult)
        # Extract events in chronological sequence from SQL
        cursor = self.sql3.execute("SELECT * FROM events WHERE" + \
                                   " title NOT IN ('Christmas Eve','New Year''s Eve') ORDER BY serialtime")
        events = map(self.EventRecord._make, cursor.fetchall())
        self.sql3.execute("DELETE FROM events")
        return events


"""
### Testing
cal = GCal()
# See what calendars will are available (not hidden)
print cal.calendarIds
print cal.getEvents()
"""        
