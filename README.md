InfoCenter
==========

Raspberry Pi-based, touchscreen-enabled, information center that provides weather, time, hourly chimes, Google calendar with alarms and Internet radio.  

Python and Pygame were used to code the graphical user interface.  The screen is divided into two tiles, left and right.  Pressing the left or right edges of the screen swaps out the tile for one that is not showing.  Currently, 3 tiles exist--Radio, Weather, and Calendar.  And more recently, I've added a full-screen mode which focuses on showing the time and in the corners show current information for weather, radio and date.  Pressing the top-center of the screen will switch between tiled and full-screen modes.

The Radio tile uses music player daemon and a custom-coded client to stream internet radio.  There are 8 presets stations presented as icons.  Artist and song title will appear in the top box of the tile, when available.  Volume can be adjusted by tapping on the left or right side of the volume level indicator at the bottom of the tile.

The Weather tile taps into Yahoo's weather api to provide current conditions as well as a 5-day forecast.  Over 20 custom-drawn weather icons provide a visual cue to weather conditions and vary for day or night.  Current conditions are detailed with temperature, condition text, wind speed, wind direction and wind chill.  The 5-day forecast provides an icon for condition and high and low temps. 

![](https://raw.githubusercontent.com/FRC4564/InfoCenter/master/screenshot1.jpg)

The calendar tile provides date, day of week, time, and Google calendar events.  The events can be from multiple calendars.  In this example, a personal calendar and a US holiday calendar are combined.  Events can have scheduled alarms, indicated by the bell icon.  Chimes can be set to sound on the hour, half-hour, or quarter-hour, with or without gongs to count of the hour. 

![](https://raw.githubusercontent.com/FRC4564/InfoCenter/master/screenshot2.jpg)

Infocenter has been developed to work on a Raspberry Pi interfaced with an touchscreen display. I currently have this working on a 7" HDMI panel running at 1024 x 600 resolution using an eGalax resistive touch panel.  It's not quite finished, but all the electronics are housed nicely in custom made cabinet.  A single 12v wall adapter powers everything.

![](https://raw.githubusercontent.com/FRC4564/InfoCenter/master/infocenter.jpg)

While the code was written to run on the RPi, it was mostly developed on a Windows desktop in the Python Idle development environment using Python 2.7 and PyGame.  If you install Python, PyGame and Google's Python APIs on your Windows machine, you can download and run this project.  First, however, you will need to edit calendartile.py and put in you gmail credentials.  Once that is done, just launch main.py. 

MPD server won't run on your PC, but to facilitate coding and testing, the Infocenter will connect to a networked MPD server whenever it detects that it is being launched from a Windows OS.  You'll need to get MPD server installed on your RPi first, so that Infocenter can connect to it.  For now main.py is hard-coded to look for "infocenter" as the hostname of the RPi, but you can change that to whatever hostname you have on your RPi.   I'll be publishing more details about MPD setup later.

When running the code from the PC the mouse will work in place of the touchscreen.  Also, the keyboard can be used to access all of Infocenter's functionality.

Left/Right Arrows - Toggle left/right tiles

F - Toggle full-screen/tiled modes

PgUp/PgDn - Change background image

Up/Down Arrows - Volume up/down

Spacebar -Play/Pause radio

1 to 8 - Select radio preset

Esc - Exit infocenter 

This is very much a work in process.  I'm still building new functionality and cleaning up code.  The next area of development is to setup a INI file for all configuration parameters.  I'm also thinking of building a photoframe option for the full-screen mode, which could access photos from a network share our other service.  I'd also like to develop other tiles, such as a twitter feed and an SMB network music player. 

I'm just starting to document this project.  Check out my blog at http://mypicorner.blogspot.com/.
