#!/usr/bin/env python
import os

nvidia_red = '10.0.0.143'; johnny_red = '10.0.0.141'

while True:
	os.system('nmap -sn 10.0.0.* > nmap.txt')
	f = open('nmap.txt', 'r')
	addresses = f.read()
	if (nvidia_red in addresses) and (johnny_red in addresses):
		break 
	elif nvidia_red in addresses:
		print('Waiting for Magni . . .')
	elif johnny_red in addresses:
		print('Waiting for nvidia . . .')
	else: 
		print('Waiting for systems to boot up. . .')
print('System is up.')
f.close()
