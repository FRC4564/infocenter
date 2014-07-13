InfoCenter
==========

Raspberry Pi-based, touchscreen-enabled information center that provides weather, time, hourly chimes, Google calendar with alarms and Internet radio.  

Python and Pygame were used to code the graphical user interface.  The screen is divided into two tiles, left and right.  Pressing the left or right edges of the screen swaps out the tile for one that is not showing.  Currently, 3 tiles exist--Radio, Weather, and Calendar.

The Radio tile use music player daemon and client (MPD/MPC) to stream internet radio.  There are 8 presets stations presented as icons.  Artist and song title will appear in the top box of the tile, if available.  Volume can be adjusted up and down, using the volume level gauge.

The Weather tile taps into Yahoo's weather api to provide current conditions as well as a 5 day forecast.  Over 20 custom drawn wether icons provide a visual cue for weather conditions and time of day.  Current conditions are detailed with temperature, condition text, wind speed, wind direction and wind chill.  The 5-day forecast provides an icon for condition and high and low temps. 

![](https://raw.githubusercontent.com/FRC4564/InfoCenter/master/screenshot1.jpg)

The calendar tile provide date, time, and Google calendar events.  The events can be from multiple calendars.  In this example, a personal calendar and a US holiday calendar are combined. 

![](https://raw.githubusercontent.com/FRC4564/InfoCenter/master/screenshot2.jpg)
