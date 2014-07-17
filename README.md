InfoCenter
==========

Raspberry Pi-based, touchscreen-enabled, information center that provides weather, time, hourly chimes, Google calendar with alarms and Internet radio.  

Python and Pygame were used to code the graphical user interface.  The screen is divided into two tiles, left and right.  Pressing the left or right edges of the screen swaps out the tile for one that is not showing.  Currently, 3 tiles exist--Radio, Weather, and Calendar.

The Radio tile uses music player daemon and client (MPD/MPC) to stream internet radio.  There are 8 presets stations presented as icons.  Artist and song title will appear in the top box of the tile, when available.  Volume can be adjusted by tapping on the left or right side of the volume level indicator at the bottom of the tile.

The Weather tile taps into Yahoo's weather api to provide current conditions as well as a 5-day forecast.  Over 20 custom-drawn weather icons provide a visual cue to weather conditions and vary for day or night.  Current conditions are detailed with temperature, condition text, wind speed, wind direction and wind chill.  The 5-day forecast provides an icon for condition and high and low temps. 

![](https://raw.githubusercontent.com/FRC4564/InfoCenter/master/screenshot1.jpg)

The calendar tile provide date, day of week, time, and Google calendar events.  The events can be from multiple calendars.  In this example, a personal calendar and a US holiday calendar are combined.  Events can have scheduled alarms, indicated by the bell icon.  Chimes sound on the hour and a code update is in the works to provide more flexible chime parameters. 

![](https://raw.githubusercontent.com/FRC4564/InfoCenter/master/screenshot2.jpg)

Infocenter has been developed to work on a Raspberry Pi running interfaced with an HDMI touchscreen display. I currently have this working on a 7" panel running at 1024 x 600 resolution using an eGalax resistive touch panel.  It's not quite finished, but all the electronics are housed nicely in custom made cabinet.  A single 12v wall adapter powers everything.

![](https://raw.githubusercontent.com/FRC4564/InfoCenter/master/infocenter.jpg)

While the code was written to run on the Pi, it was mostly developed on a Windows desktop in the Python Idle development environment using Python 2.7 and PyGame.  If you install Python, PyGame and Google's Python APIs on your Windows machine, you should be able to download and run this project.  First, however, you will need to edit calendartile.py and put in you gmail credentials in a couple of spots.  Once that is done, just launch main.py.  You won't have internet radio functionality, since MPC is not available for Windows, but you can see and play with the other tile funcions.  The mouse will work in place of the touchscreen, but as is, the calibration functions for the touchscreen invert the y axis.  It's on my list of to do's to automatically switch that off when the touchscreen isn't available.

This is very much a work in process.  I'm recoding the UI side of this and cleaning up the main.py code so that I can add some more cool functionality.  First off, I'm looking to do a fullscreen clock, that has a live slideshow background and uses the corners of the display to show weather, date and radio information.  I'd also like to develop other tiles, such as a twitter feed and an SMB network music player. 





