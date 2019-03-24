import pygame
# Weather Icons to support OpenWeather ID codes for Day/Night and Large and Small

weatherIDs = {200: {'description': 'Thunderstorms', 'imageday': 'Thunderstorm.png', 'imagenight': 'Thunderstorm.png'},
    201: {'description': 'Thunderstorms', 'imageday': 'Thunderstorm.png', 'imagenight': 'Thunderstorm.png'},
    202: {'description': 'Severe thunderstorms', 'imageday': 'Thunderstorm.png', 'imagenight': 'Thunderstorm.png'},
    210: {'description': 'Thunderstorms', 'imageday': 'Thunderstorm.png', 'imagenight': 'Thunderstorm.png'},
    211: {'description': 'Thunderstorms', 'imageday': 'Thunderstorm.png', 'imagenight': 'Thunderstorm.png'},
    212: {'description': 'Severe thunderstorms', 'imageday': 'Thunderstorm.png', 'imagenight': 'Thunderstorm.png'},
    221: {'description': 'Scattered thunderstorms', 'imageday': 'Thunderstorm.png', 'imagenight': 'Thunderstorm.png'},
    230: {'description': 'Thunderstorms', 'imageday': 'Thunderstorm.png', 'imagenight': 'Thunderstorm.png'},
    231: {'description': 'Thunderstorms', 'imageday': 'Thunderstorm.png', 'imagenight': 'Thunderstorm.png'},
    232: {'description': 'Thunderstorms', 'imageday': 'Thunderstorm.png', 'imagenight': 'Thunderstorm.png'},
    300: {'description': 'Drizzle', 'imageday': 'LightRain.png', 'imagenight': 'LightRain.png'},
    301: {'description': 'Drizzle', 'imageday': 'LightRain.png', 'imagenight': 'LightRain.png'},
    302: {'description': 'Drizzle', 'imageday': 'LightRain.png', 'imagenight': 'LightRain.png'},
    310: {'description': 'Drizzle', 'imageday': 'LightRain.png', 'imagenight': 'LightRain.png'},
    311: {'description': 'Drizzle', 'imageday': 'LightRain.png', 'imagenight': 'LightRain.png'},
    312: {'description': 'Rain', 'imageday': 'LightRain.png', 'imagenight': 'LightRain.png'},
    313: {'description': 'Rain', 'imageday': 'LightRain.png', 'imagenight': 'LightRain.png'},
    314: {'description': 'Rain', 'imageday': 'LightRain.png', 'imagenight': 'LightRain.png'},
    321: {'description': 'Rain', 'imageday': 'LightRain.png', 'imagenight': 'LightRain.png'},
    500: {'description': 'Rain', 'imageday': 'LightRain.png', 'imagenight': 'LightRain.png'},
    501: {'description': 'Showers', 'imageday': 'HeavyRain.png', 'imagenight': 'HeavyRain.png'},
    502: {'description': 'Heavy Rain', 'imageday': 'HeavyRain.png', 'imagenight': 'HeavyRain.png'},
    503: {'description': 'Heavy Rain', 'imageday': 'HeavyRain.png', 'imagenight': 'HeavyRain.png'},
    504: {'description': 'Heavy Rain', 'imageday': 'HeavyRain.png', 'imagenight': 'HeavyRain.png'},
    511: {'description': 'Freezing rain', 'imageday': 'IcyRain.png', 'imagenight': 'IcyRain.png'},
    520: {'description': 'Showers', 'imageday': 'HeavyRain.png', 'imagenight': 'HeavyRain.png'},
    521: {'description': 'Showers', 'imageday': 'HeavyRain.png', 'imagenight': 'HeavyRain.png'},
    522: {'description': 'Heavy Rain', 'imageday': 'HeavyRain.png', 'imagenight': 'HeavyRain.png'},
    531: {'description': 'Scattered showers', 'imageday': 'HeavyRain.png', 'imagenight': 'HeavyRain.png'},
    600: {'description': 'Light snow', 'imageday': 'LightSnow.png', 'imagenight': 'LightSnow.png'},
    601: {'description': 'Snow', 'imageday': 'HeavySnow.png', 'imagenight': 'HeavySnow.png'},
    602: {'description': 'Heavy Snow', 'imageday': 'HeavySnow.png', 'imagenight': 'HeavySnow.png'},
    611: {'description': 'Sleet', 'imageday': 'Ice.png', 'imagenight': 'Ice.png'},
    612: {'description': 'Rain sleet mix', 'imageday': 'IcyRain.png', 'imagenight': 'IcyRain.png'},
    613: {'description': 'Rain sleet mix', 'imageday': 'IcyRain.png', 'imagenight': 'IcyRain.png'},
    615: {'description': 'Rain snow mix', 'imageday': 'SnowRain.png', 'imagenight': 'SnowRain.png'},
    616: {'description': 'Rain snow mix', 'imageday': 'SnowRain.png', 'imagenight': 'SnowRain.png'},
    620: {'description': 'Rain snow mix', 'imageday': 'SnowRain.png', 'imagenight': 'SnowRain.png'},
    621: {'description': 'Snow', 'imageday': 'HeavySnow.png', 'imagenight': 'HeavySnow.png'},
    622: {'description': 'Heavy Snow', 'imageday': 'HeavySnow.png', 'imagenight': 'HeavySnow.png'},
    701: {'description': 'Haze', 'imageday': 'FogDay.png', 'imagenight': 'FogNight.png'},
    711: {'description': 'Smoke', 'imageday': 'FogDay.png', 'imagenight': 'FogNight.png'},
    721: {'description': 'Haze', 'imageday': 'FogDay.png', 'imagenight': 'FogNight.png'},
    731: {'description': 'Dust', 'imageday': 'FogDay.png', 'imagenight': 'FogNight.png'},
    741: {'description': 'Fog', 'imageday': 'FogDay.png', 'imagenight': 'FogNight.png'},
    751: {'description': 'Dust', 'imageday': 'FogDay.png', 'imagenight': 'FogNight.png'},
    761: {'description': 'Dust', 'imageday': 'FogDay.png', 'imagenight': 'FogNight.png'},
    762: {'description': 'Dust', 'imageday': 'FogDay.png', 'imagenight': 'FogNight.png'},
    771: {'description': 'Windy', 'imageday': 'Windy.png', 'imagenight': 'Windy.png'},
    781: {'description': 'Tornado', 'imageday': 'MostlyCloudy.png', 'imagenight': 'MostlyCloudyNight.png'},
    800: {'description': 'Clear', 'imageday': 'Sunny.png', 'imagenight': 'ClearNight.png'},
    801: {'description': 'Fair', 'imageday': 'Fair.png', 'imagenight': 'FairNight.png'},
    802: {'description': 'Partly cloudy', 'imageday': 'PartlyCloudy.png', 'imagenight': 'PartlyCloudyNight.png'},
    803: {'description': 'Mostly cloudy', 'imageday': 'MostlyCloudy.png', 'imagenight': 'MostlyCloudyNight.png'},
    804: {'description': 'Cloudy', 'imageday': 'Cloudy.png', 'imagenight': 'Cloudy.png'}}

# Load weather icons and build into dictionary of weather codes
def loadWeatherCodes(directory):
    # build a dictionary of unique image filenames and load the image files.
    # Both normal-sized and small-sized (50x50) icons files are loaed.  
    images = {}
    for id in weatherIDs:
        code = weatherIDs[id]
        for i in ['imageday', 'imagenight']:
            if not images.has_key(code[i]):
                images[code[i]] = pygame.image.load(directory + code[i]).convert_alpha()
                images["sml"+code[i]] = pygame.transform.scale(images[code[i]],(50,50))
    """# For each weather ID, create array of codes, descriptions,day image, night image, sml image         
    codes = []
    for id in weatherIDs:
        code = weatherIDs[id]
        # Select the image files to associate
        dayimg = images[code['imageday']]
        smlimg = images['sml'+code['imageday']]
        nightimg = images[code['imagenight']]
        # Add to icons list: Weather ID, Description, Daytime image, Nighttime image, Small image
        codes.append([id,code['description'],dayimg,nightimg,smlimg])
    return images,codes
    """
    return images

"""
# testing
pygame.init()
scr = pygame.display.set_mode([640,480])
imgIcons = loadWeatherCodes('icons\\')
print imgIcons

scr.blit(imgIcons['HeavyRain.png'],(20,20))
scr.blit(imgIcons['smlThunderstorm.png'],(0,0))
pygame.display.update()
"""

def loadRadioImages(directory):
    images = {}
    #
    images['UnselectedStation'] = pygame.image.load(directory + 'UnselectedStation.png').convert_alpha()
    images['SelectedStation'] = pygame.image.load(directory + 'SelectedStation.png').convert_alpha()
    images['PlayButton'] = pygame.image.load(directory + 'PlayButton.png').convert_alpha()
    images['StopButton'] = pygame.image.load(directory + 'StopButton.png').convert_alpha()
    #
    #images['Station1'] = pygame.image.load(directory + 'StationRadioParadise.png').convert_alpha()
    #images['Station2'] = pygame.image.load(directory + 'StationRTERadio1.png').convert_alpha()
    #images['Station3'] = pygame.image.load(directory + 'StationSmoothLounge.png').convert_alpha()
    #images['Station4'] = pygame.image.load(directory + 'StationRadioParadise.png').convert_alpha()
    #images['Station5'] = pygame.image.load(directory + 'StationBenFM.png').convert_alpha()
    #images['Station6'] = pygame.image.load(directory + 'StationBigClassicHits.png').convert_alpha()
    #images['Station7'] = pygame.image.load(directory + 'StationRadioParadise.png').convert_alpha()
    #images['Station8'] = pygame.image.load(directory + 'StationAcousticFM.png').convert_alpha()
    
    return images
