import urllib2
import json

"""Yahoo weather giving current conditions and 5 day forecast.

Usage example:

    w = yahooweather.Weather('Brewer,ME')   #Create weather instance based on zipcode
    w.fetch()                           #Fetch weather update
    print w.current('temp')             #Current temperature
    print w.forecast('day',0)           #Current day of week
    print w.forecast('high',1)          #Tomorrow's High
    print w.wind('chill')               #Wind chill
"""

class Weather():

    def __init__(self,location='Brewer,ME'):
        #self.url = 'http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20location%3D%22'+zip+'%22&format=json'
        self.url = "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text=%22"+location+"%22)&format=json"

    # Fetch the weather from Yahoo
    # Returns True if successful
    def fetch(self):
        try:
            http = urllib2.urlopen(self.url)
            self.jsonweather = json.loads(http.read())
            http.close()
            self.current()  #Test to see if result is parsable.  Error will trap otherwise.
            return True
        except:
            return False

    # Current conditions (items: code, date, temp, text)
    def current(self,item='temp'):
        x = self.jsonweather['query']['results']['channel']['item']['condition']
        return x[item]

    # 5 day forcast - day 0=today (items: code, date, day, low, high, text)
    def forecast(self,item='text',day=0):
        x = self.jsonweather['query']['results']['channel']['item']['forecast']
        return x[day][item]

    # Wind (items: speed, direction, chill)
    def wind(self,item='speed'):
        x = self.jsonweather['query']['results']['channel']['wind']
        return x[item]

    # Astronomy (items: sunrise, sunset)
    def astronomy(self,item='sunrise'):
        x = self.jsonweather['query']['results']['channel']['astronomy']
        return x[item]

    # Location (items: city, region, country, lat, long)
    def location(self,item='city'):
        if item == 'lat':
            x = self.jsonweather['query']['results']['channel']['item']['lat']           
        elif item == 'long':
            x = self.jsonweather['query']['results']['channel']['item']['lon']
        else:
            x = self.jsonweather['query']['results']['channel']['location']

    # Atmosphere (items: pressure, rising, visibility, humidity)
    def atmosphere(self,item='pressure'):
        x = self.jsonweather['query']['results']['channel']['atmosphere']
        return x[item]
        
    # Info (items: title,builddate,pubdate,icon,ttl)
    def info(self,item='title'):
        i = item
        if item == 'title':
            return self.jsonweather['query']['results']['channel']['item']['title']
        elif item == 'builddate':
            return self.jsonweather['query']['results']['channel']['lastBuildDate']
        elif item == 'pubdate':
            return self.jsonweather['query']['results']['channel']['item']['pubDate']
        elif item == 'ttl':  #time to live before weather update
            return self.jsonweather['query']['results']['channel']['ttl']
        else:
            return self.jsonweather['query']['results']['channel']['image']['url']

    # Units (items: distance, speed, temperature, pressure)            
    def units(self,item='temperature'):
        x = self.jsonweather['query']['results']['channel']['units']
        return x[item]
    
