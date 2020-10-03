#!/usr/bin/env python
import os

nvidia_boy = '10.0.0.101'; johnny_boy = '10.0.0.100'

while True:
	os.system('nmap -sn 10.0.0.* > nmap.txt')
	f = open('nmap.txt', 'r')
	addresses = f.read()
	if (nvidia_boy in addresses) and (johnny_boy in addresses):
		break 
	elif nvidia_boy in addresses:
		print('Waiting for Magni . . .')
	elif johnny_boy in addresses:
		print('Waiting for nvidia . . .')
	else: 
		print('Waiting for systems to boot up. . .')
print('System is up.')
f.close()
