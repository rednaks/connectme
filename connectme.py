#! /usr/bin/python
import os
import sys
import time



def wakeUp():
	os.system('ifconfig wlan0 down')
	time.sleep(0.5)
	os.system('ifconfig wlan0 up')
	time.sleep(0.5)

def getChannels(essid):
	wakeUp()
	os.system('iwlist wlan0 scan essid %s | grep -i channel: > channels.txt' % essid)
	f = open('channels.txt')
	channels = []
	content = f.readlines()
	f.close()
	os.system('rm channels.txt')
	for c in content:
		channels.append(c.split(':')[1].replace('\n',''))

	print channels
	return channels
		

def gotIP():
	os.system('ifconfig wlan0 | grep -i adr: > ip.txt')
	f = open('ip.txt')
	c = f.readlines()
	print c
	f.close()
	os.system('rm ip.txt')
	return len(c) is not 0

def connectme(essid):
	os.system('ifconfig wlan0 up')
	channels = getChannels(essid)
	for c in channels:
		print 'channel %s selected ! connecting ...' % c
		os.system('iwconfig wlan0 essid %s channel %s' %(essid,c))
		print 'getting IP ...'
		os.system('dhclient wlan0')
		if gotIP():
			print 'YEEEEEH !!'
			break
		else:
			print 'Fail !'
	

if os.geteuid() != 0:
	print 'You must be root !'
	sys.exit()

if len(sys.argv) is 2:
	essid =  sys.argv[1]
	print 'trying to connect to "%s" ...' % essid
	connectme(essid)
else:
	print '''Usage : connectme.py essid
Ex : connectme.py my_access_point
Note : Access point musnt have and encryption key.
'''


