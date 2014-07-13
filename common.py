import pygame
import threading
import os

# CONSTANTS
DISPLAY_RES = (1024,600)
TILE_SIZE = (512,600)

BLACK   = (0,0,0)
WHITE   = (255,255,255)
GREY    = (150,150,150)
RED     = (255,0,0)
GREEN   = (0,255,0)
BLUE    = (0,0,255)
YELLOW  = (255,255,0)

LEFT   = 0
RIGHT  = 1
CENTER = 2


# RESOURCE DIRECTORIES
if os.name == "NT":
    DIR_DELIM = '\\'
else:
    DIR_DELIM = '/'

BACKGROUNDS_DIR = 'backgrounds' + DIR_DELIM
ICONS_DIR = 'icons' + DIR_DELIM
RADIO_DIR = 'radio' + DIR_DELIM
SOUNDS_DIR = 'sounds' + DIR_DELIM

# SOUNDS
SND_NOTIFICATION = SOUNDS_DIR + 'xylophone1.mp3'
SND_ALARM        = SOUNDS_DIR + 'xylophone2.mp3'
SND_HOURLY_CHIME = SOUNDS_DIR + 'hourlychimeshort.mp3'


# FONTS
pygame.font.init()
fontGiant  = pygame.font.Font('century.ttf',165)
fontHuge   = pygame.font.Font('century.ttf',90)
fontLarge  = pygame.font.Font('century.ttf',45)
fontMedium = pygame.font.Font('century.ttf',35)
fontSmall  = pygame.font.Font('century.ttf',28)
fontTiny = pygame.font.Font(None,32)

# THREADING
threadLock = threading.Lock()
# Creates a new thread object that will run the 'target' function with the provide argument list.
# Passing mutable objects (not variables) provides a means for communications with main thread.
# Global variables can be used at well.
# Use a threading.lock object along with 'with:' statement to safely coordinate changes to shared objects.
# Use thread.isActive() to know if thread is has completed.
#
class Thread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
 
    def run(self):
        self._target(*self._args)


# display at text string onto pygame surface at x,y location relative to alignment.
# returns ending x position and y position for next line adjusting for leading percent (1=100% of normal).
def textAt(x,y,text,surface,font,color=WHITE,align=LEFT,antialias=0,leading=1):
    txtImg = font.render(text,antialias,color)
    txtWidth = txtImg.get_width()
    txtHeight = txtImg.get_height() * leading
    if align == LEFT:
        surface.blit(txtImg,(x,y))
        return (x + txtWidth, y + txtHeight)
    elif align == RIGHT:
        surface.blit(txtImg,(x - txtWidth, y))
        return (x - txtWidth, y + txtHeight)
    else:
        surface.blit(txtImg,(x - (txtWidth/2), y))
        return (x - (txtWidth/2), y + txtHeight)

# draw alpha shaded rectangle filled with provided color    
def shade(x,y,w,h,surface,color,alpha):
    rec = pygame.surface.Surface((w,h))
    rec.fill(color)
    rec.set_alpha(alpha)
    surface.blit(rec,(x,y))
    return

# take 12hr time-formatted string and change to decimal hours since midnight
# ex params: 7:00 am    10:45pm
def time2hours(t):
    colon = t.find(':')
    if colon == 0 or colon > 2:
        print 'time2hours function expected ":" in time'
    else:
        h = int(t[0:colon])
        m = int(t[colon+1:colon+3])
    if t[-2:].lower() == 'pm':
        if h != 12:
            h = h + 12
    else:
        if h == 12:
            h=0
    return h + m / 60.0

# translate compass bearing to text heading
def compass(bearing):
    try:
        x = (int(bearing) + 22)
        if x >= 360:
            x = x - 360
        x = x / 45
        comp = ('North','NE','East','SE','South','SW','West','NW')
        direction = comp[x]
    except:
        direction = str(bearing)
    return direction

# play an mp3 file
def playMP3(file):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
