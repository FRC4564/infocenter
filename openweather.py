import json
import time
import requests
import icons

def epochStr(epoch):
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(epoch))


class Weather():

    def __init__(self):  
        #Load configuration file
        try:
            f=open('openweather.id','r')
            f.readline()  #skip comment line
            self.appID = f.readline().rstrip()
            self.locationID = f.readline().rstrip()
            self.units = f.readline().rstrip()
            f.close()
        except:
            print("Error: openweather.py unable to process 'openweather.id' configuration file")
            raise
        self.nextUpdate = 0
        self.updateInterval = 15 * 60  #In seconds
        self.currentURL = ""
        self.forecastURL = ""
        self.setLocationByID(self.locationID)
        self.current = {}    #Current weather
        self.forecasts = []   #Forecast for next 5 days

    def setLocationByID(self, locationID):
        baseURL = "http://api.openweathermap.org/data/2.5"
        self.currentURL = "{}/weather?APPID={}&id={}&units={}".format(baseURL,self.appID,locationID,self.units)
        self.forecastURL = "{}/forecast?APPID={}&id={}&units={}".format(baseURL,self.appID,locationID,self.units)
        self.nextUpdate = 0  #force next update to allow pull
        
    def windchill(self, temp, windspeed):
        wc = temp
        if self.units == "imperial":
            if temp <= 50 and windspeed >= 3:
                wc = 35.74 + 0.6215*temp - 35.75*windspeed**0.16 + 0.4275*temp*windspeed**0.16
        else:
            if temp <= 10 and windspeed >= 4.8:
                wc = 13.12 + 0.6215*temp - 11.37*windspeed**0.16 + 0.3965*temp*windspeed**0.16
        return wc

    def fetch(self):
        if self.nextUpdate < time.time():
            self.nextUpdate = time.time() + self.updateInterval
            return self._fetch()
        else:
            return False

    def _fetch(self):
        if (self._loadCurrent() and self._loadForecast()):
            return True
        else:
            return False

    def _loadCurrent(self):
        resp = requests.get(self.currentURL)
        if resp.status_code == 200:
            curr = resp.json()
            # current temp/humidity
            temp = round(curr['main']['temp'])
            humidity = round(curr['main']['humidity'])
            tempMin = round(curr['main']['temp_min'])
            tempMax = round(curr['main']['temp_max'])
            # wind
            windSpeed = round(curr['wind']['speed'])
            windDeg = round(curr['wind']['deg'])
            try:
                windGust = round(curr['wind']['gust'])
            except:
                windGust = 0
            windChill = round(self.windchill(temp, windSpeed))
            # time of day
            sunriseEpoch = curr['sys']['sunrise']
            sunrise = epochStr(sunriseEpoch)
            sunsetEpoch = curr['sys']['sunset']
            sunset = epochStr(sunsetEpoch)
            if time.time() >= sunriseEpoch and time.time() <= sunsetEpoch:
                daytime = True
            else:
                daytime = False
            # description and icon
            weatherID = curr['weather'][0]['id']
            if icons.weatherIDs.get(weatherID) == None: #if ID is not known, then assume "Clear Sky"
                weatherID = 800
            description = icons.weatherIDs[weatherID]['description']
            if daytime:
                image = icons.weatherIDs[weatherID]['imageday']
            else:
                image = icons.weatherIDs[weatherID]['imagenight']
            placeName = curr['name']
            self.current = {'temp': int(temp), 'tempmin': int(tempMin), 'tempmax': int(tempMax), 'humidity': int(humidity),
                            'windspeed': int(windSpeed), 'winddirection': windDeg, 'windgust': int(windGust), 'windchill': int(windChill),
                            'sunrise': sunrise, 'sunset': sunset, 'daytime': daytime,
                            'description': description, 'image': image, 'placename': placeName}
            return True
        else:
            return False

    def _loadForecast(self):
        self.forecasts = []
        resp = requests.get(self.forecastURL)
        if resp.status_code == 200:
            fore = resp.json()
            ymdCurrent = time.strftime("%Y-%m-%d", time.localtime())
            dowBreak = ""
            for c in range(fore['cnt']):
                l = fore['list'][c]
                ymd = time.strftime("%Y-%m-%d", time.localtime(l['dt']))
                if ymd > ymdCurrent:  #Only process forecasts for tomorrow and forward
                    dow = time.strftime("%a", time.localtime(l['dt']))
                    #print("  ymd: ",ymd, " temp ", l['main']['temp'], " id ", l['weather'][0]['id'])
                    # Break process whenever ymd changes
                    if dow != dowBreak:
                        if dowBreak != "":
                            forecast = self._processBreak(dowBreak, IDs, lowTemp, highTemp)
                        dowBreak = dow
                        lowTemp = 999
                        highTemp = -999
                        IDs = []
                    # Low and High temps
                    temp = round(l['main']['temp'])
                    if temp < lowTemp:
                        lowTemp = temp
                    if temp > highTemp:
                        highTemp = temp
                    # Accumulate array of IDs for this current date
                    weatherID = l['weather'][0]['id']
                    IDs.append(weatherID)                

            self._processBreak(dow, IDs, lowTemp, highTemp)
            return True
        else:
            return False

            
    def _processBreak(self, dow, IDs, lowTemp, highTemp):
        weatherID = self._mostFrequent(IDs)
        description = icons.weatherIDs[weatherID]['description']
        image = icons.weatherIDs[weatherID]['imageday']
        f = {'dow': dow, 'id': weatherID, 'description': description, 'image': image,
             'lowtemp': int(lowTemp), 'hightemp': int(highTemp)}
        self.forecasts.append(f)

    # Given a list array, find the highest occuring value
    def _mostFrequent(self, array): 
        return max(set(array), key = array.count) 
        
    """
    humidity = l['main']['humidity']
    cloudsPct = l['clouds']['all']
    w=l['weather'][0]
    id=w['id']
    desc=w['description']
    icon=w['icon']
    windSpeed=l['wind']['speed']
    windDir=l['wind']['deg']
    try:
        rain=l['rain']
    except:
        rain={}
    try:
        snow=l['snow']
    except:
        snow={}
    """

"""
#test
w = Weather(4152890)  #Deland
w.update()
print(w.current)
print(w.forecasts)
"""
