import pygame
# Weather Icons to support Yahoo codes for Day/Night and Large and Small

# Seq number: Yahoo Code number, Text Desc, daytime icon file, nighttime icon file
# See icons at Yahoo - ex: icon 41 - http://l.yimg.com/a/i/us/we/52/41.gif 
WeatherCodes=[
[0, 'Tornado',                'MostlyCloudy.png',      'MostlyCloudyNight.png'    ],
[1, 'Tropical storm',         'Hurricane.png',         'Hurricane.png'            ],
[2, 'Hurricane',              'Hurricane.png',         'Hurricane.png'            ],
[3, 'Severe thunderstorms',   'Thunderstorm.png',      'Thunderstorm.png'         ],
[4, 'Thunderstorms',          'Thunderstorm.png',      'Thunderstorm.png'         ],
[5, 'Rain snow mix',          'SnowRain.png',          'SnowRain.png'             ], 
[6, 'Rain sleet mix',         'IcyRain.png',           'IcyRain.png'              ],
[7, 'Snow sleet mix',         'IceSnow.png',           'IceSnow.png'              ],
[8, 'Freezing drizzle',       'Ice.png',               'Ice.png'                  ],
[9, 'Drizzle',                'LightRain.png',         'LightRain.png'            ],
[10,'Freezing rain',          'IcyRain.png',           'IcyRain.png'              ],  
[11,'Showers',                'HeavyRain.png',         'HeavyRain.png'            ],
[12,'Showers',                'HeavyRain.png',         'HeavyRain.png'            ],
[13,'Snow flurries',          'LightSnow.png',         'LightSnow.png'            ],
[14,'Light snow',             'LightSnow.png',         'LightSnow.png'            ],
[15,'Blowing snow',           'HeavySnow.png',         'HeavySnow.png'            ],
[16,'Snow',                   'HeavySnow.png',         'HeavySnow.png'            ],
[17,'Hail',                   'Ice.png',               'Ice.png'                  ],
[18,'Sleet',                  'Ice.png',               'Ice.png'                  ],
[19,'Dust',                   'FogDay.png',            'FogNight.png'             ],
[20,'Foggy',                  'FogDay.png',            'FogNight.png'             ],
[21,'Haze',                   'FogDay.png',            'FogNight.png'             ],
[22,'Smoky',                  'FogDay.png',            'FogNight.png'             ],
[23,'Blustery',               'Windy.png',             'Windy.png'                ],
[24,'Windy',                  'Windy.png',             'Windy.png'                ],
[25,'Cold',                   'Cold.png',              'Cold.png'                 ],
[26,'Cloudy',                 'Cloudy.png',            'Cloudy.png'               ],
[27,'Mostly cloudy',          'MostlyCloudy.png',      'MostlyCloudyNight.png'    ],
[28,'Mostly cloudy',          'MostlyCloudy.png',      'MostlyCloudyNight.png'    ],
[29,'Partly cloudy',          'PartlyCloudy.png',      'PartlyCloudyNight.png'    ],
[30,'Partly cloudy',          'PartlyCloudy.png',      'PartlyCloudyNight.png'    ],
[31,'Clear',                  'Sunny.png',             'ClearNight.png'           ],
[32,'Sunny',                  'Sunny.png',             'ClearNight.png'           ],
[33,'Fair',                   'Fair.png',              'FairNight.png'            ],
[34,'Fair',                   'Fair.png',              'FairNight.png'            ],
[35,'Rain and hail mix',      'IcyRain.png',           'IcyRain.png'              ],
[36,'Hot',                    'Hot.png',               'Hot.png'                  ],
[37,'Isolated thunderstorms', 'Thunderstorm.png',      'Thunderstorm.png'         ],
[38,'Scattered thunderstorms','Thunderstorm.png',      'Thunderstorm.png'         ],
[39,'Scattered thunderstorms','Thunderstorm.png',      'Thunderstorm.png'         ],
[40,'Scattered showers',      'HeavyRain.png',         'HeavyRain.png'            ],
[41,'Heavy snow',             'HeavySnow.png',         'HeavySnow.png'            ],
[42,'Snow showers',           'LightSnow.png',         'LightSnow.png'            ],
[43,'Heavy snow',             'HeavySnow.png',         'HeavySnow.png'            ],
[44,'Partly cloudy',          'PartlyCloudy.png',      'PartlyCloudyNight.png'    ],
[45,'Thundershowers',         'Thunderstorm.png',      'Thunderstorm.png'         ],
[46,'Snow showers',           'LightSnow.png',         'LightSnow.png'            ],
[47,'Thundershowers',         'Thunderstorm.png',      'Thunderstorm.png'         ]]


def loadWeatherCodes(directory,images = {}):
    # Load image files
    images = {}
    # build a dictionary of unique image filenames and loaded image file.
    for code in WeatherCodes:
        for i in range(2,4):
            if code[i] != '':
                if not images.has_key(code[i]):
                    images[code[i]] = pygame.image.load(directory + code[i]).convert_alpha()
                    images["sml"+code[i]] = pygame.transform.scale(images[code[i]],(50,50))
             
    codes = []
    for code in WeatherCodes:
        # Choose image for day time
        if code[2] == '':
            dayimg = images['Sunny.png']
            smlimg = images['smlSunny.png']
        else:
            dayimg = images[code[2]]
            smlimg = images['sml'+code[2]]
        # Choose image for night time
        if code[3] == '':
            nightimg = images['ClearNight.png']
        else:
            nightimg = images[code[3]]
        # Add to icons list: Weather Code, Description, Daytime image, Nighttime image, Small image
        codes.append([code[0],code[1],dayimg,nightimg,smlimg])
    return images,codes
               
#imgIcons,weatherCodes = loadWeatherCodes('icons\\')
#print weatherCodes[2]


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
