#!/usr/bin/env python3
# Copyright 2016 Tero Karvinen & Kimmo Karvinen http://BotBook.com
"BotBook.com Python IoT server. "

import serial	# sudo apt-get -y install python3-serial # 
from time import sleep
from urllib.request import urlopen
from urllib.error import HTTPError

def serReadLine(ser):
	s = ser.readline(500)
	s = s.decode('ASCII')	# convert bytes b'foo' to string 'foo'
	assert type(s)==str

	if len(s)<=1:
		return None
	if not s.endswith('\n'):
		return 'ERROR: Serial: Unknown command "%s"' % s
	s = s.replace('\n', '');

	return s

def get(url):
	try:
		with urlopen(url, timeout=3) as resp:
			body=resp.read()
			body=body.decode('ASCII')
			#print("DEBUG: body: '%s'" % body)
			assert type(body)==str
			return body.split('\n')[0]
	except HTTPError as e:
		return 'ERROR: GET: HTTPError: %s' % e.code
	except Exception as e:
		return 'ERROR: Unspecified error in HTTP GET.'

def firstLine(s):
	return s.split('\n')[0]

def main():
	# port: "/dev/ttyUSB1", "COM1"
	ser = serial.Serial(port="/dev/ttyACM0", baudrate=115200, timeout=1)

	while True:
		s = serReadLine(ser)
		if s: 
			print(s)
			if s.startswith("HELLO"):
				ser.write(b'OK BotBookESP Python 0.0.1\n')
			elif s.startswith("GET"):
				# GET http://139.162.200.127/add/hw0ZcPe9p8Y/?x=2.6
				url=s.split()[1]
				body=get(url)
				body=firstLine(body)
				body=body.encode('ASCII')
				print(body.decode('ASCII'))
				ser.write(body)
			else:
				msg='ERROR: Python: unknown command "%s"' % s.replace('\n', '')
				ser.write(s.encode('ASCII'))
		# ser.flushInput()
		sleep(0.2) # seconds

if __name__ == '__main__':
	main()


