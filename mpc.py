import socket
import time
import threading
import sys

class MPC():

	def __init__(self,host='localhost'):
		self.host = host
		# Socket variables
		self.socket = None
		self.readch = None
		self.writech = None
		# Status variables - parsed from MPD responses
		self.artist = ""   #parsed from Title
		self.song = ""     #parsed from Title
		self.track = 0     #index of current playlist track
		self.volume = 0    #0 to 100
		self.state = None  #stop, play, or pause
		self.playing = False
		# Queues outbound commands to MPD, which are executed by _processor
		self.commandQue = []
		# Start the processor thread
		self._run = True  #While True, _processor will remain running
		self._proc = threading.Thread(target=self._processor)
		self._proc.start()
		
		
	# Connect to MPD and return socket and read/write channels.  Will retry indefinitely to connect.
	# Used exclusively by _processor()
	def _connect(self):
		while self.socket == None:
			try:
				self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM,socket.IPPROTO_TCP)
				self.socket.connect((self.host,6600))
				self.socket.settimeout(2)  #subsequent commands to the socket will timeout with timeout error
				self.readch = self.socket.makefile("rb")
				self.writech = self.socket.makefile("wb")
				# expect OK MPD response
				line = self._read()
				if line.startswith("OK MPD") <> True:
					print "Expected OK MPD response, but got " + line
					raise ioError
			except:
				if self.socket is not None:
					self.socket.close()
				err = sys.exc_info()[0]
				print "Socket failed to connect - retrying in 2 secs",err
				self.socket = None
				time.sleep(2)
				
        # Read a line from the MPD socket
	def _read(self):
		try:
			return self.readch.readline()
		except socket.timeout:
			pass
		except:
			print "Socket readline failed"
			raise


	# Send a command to MPD socket
	def _write(self,line):
		self.writech.write("%s\n" % line)
		self.writech.flush()
		
		
	# Processor will feed commands to MPD and constantly check status and song information.
	# As responses come in from MPD, the useful values are formatted and stored for reference.
	def _processor(self):
		while self._run:
			# create socket connection if not open
			if self.socket == None:
				self._connect()
			# process all commands that have been stacked up
			while len(self.commandQue)>0:
				command = self.commandQue.pop(0)
				self._process(command)
			# Routinely get MPD status updates
			self._process("status")
			self._process("currentsong")
			# Sit idle for a bit, unless a new command comes in
			hold = time.time() + 0.5
			while time.time() < hold and len(self.commandQue) == 0:
				time.sleep(0.1)


        # Send a command to MPD and process the response
	def _process(self,command):
                self._write(command)
                if command == "status":
                        self._parse_status()
                elif command == "currentsong":
                        self._parse_currentsong()
                else:
                        self._read_response()
                     

        # Read MPD responses from 'status'.
        # Updates self.track, self.volume, self.state, and self.playing 
	def _parse_status(self):
		line = self._read()
		while line <> "OK\n":
			# parse the returned line
			keyword, value = self._parse(line)
                        if keyword == "song":
                                self.track = int(value)
                        elif keyword == "volume":
                                self.volume = int(value)
                        elif keyword == "state":
                                self.state = value
                                if value == "play":
                                        self.playing = True
                                else:
                                        self.playing = False
			line = self._read()

	
        # Read MPD responses from 'currentsong', looking for Title:
        # Both self.artist and self.song are parsed from the title.
	def _parse_currentsong(self):
		line = self._read()
		artist = ""
		song = ""
		while line <> "OK\n":
			keyword, value = self._parse(line)
			# Parse Title info if it appears. 
                        if keyword == "Title":
                                split = value.split(" - ",1)
                                if len(split) == 2:
                                        artist = split[0]
                                        if artist.startswith("'"):
                                                artist = artist[1:] #drop leading apostrophe
                                        song = split[1]
                                        if song == "text":
                                                song = ""
			line = self._read()
			self.artist = artist
			self.song = song


	# Read MPD response to a command, just looking for OK or ACK.
	def _read_response(self):
		line = self._read()
		while line <> "OK\n" and line <> "OK MPD " and line <> "ACK ":
        		line = self._read()
        

        # Split response if a keyword/value pair separated with a ': '.  Returns tuple (field, value).
        # Value is "" if not a keyword/value pair.
        def _parse(self,line):
                split = line.split(": ",1)
                if len(split) > 0:
                        keyword = split[0]
                        if len(split) == 2:
                                value = split[1][:-1]  #drop trailing linefeed
                        else:
                                keyword = keyword[:-1] #drop trailing linefeed
                                value = ""
                return keyword,value


	# Command queue is used by _processor to send MPD commands sequentially
	def _queue(self,command):
		self.commandQue.append(command)

# COMMANDS		
	
	# Start playing 
	def play(self,track=0):
		self._queue("play %r" % track)
		
	def stop(self):
		self._queue("stop")
	
	# Empty playlist
	def clear(self):
		self._queue("clear")
		
	# Add URI to playlist
	def add(self,uri):
		self._queue("add %s" % uri)
		
	# Set volume (0 to 100)
	def setvol(self,volume):
		self._queue("setvol %r" % volume)
	
	# Shuts down the processor and closes the socket
	def close(self):
		self._run = False
		self.socket.close()
