#!/usr/bin/env python
import os
from Tkinter import *
from std_msgs.msg import String
import rospy
import time

global cp

class command_publisher:
	def __init__(self):
		rospy.init_node('command_publisher', anonymous=True)
		self.pub = rospy.Publisher('launch_cmds',String,queue_size=10)
		print('initialized launch command_publisher')
		self.safe_init_sleep_time = 2.0		
		time.sleep(2) 
		print('woke up from initialization...')
		self.command = ''

	def publish_command(self):
		now = rospyTime.now()
		rospy.loginfo(self.command)
		#print('publishing...')
		self.pub.publish(self.command)
		#print('published!')

cp = command_publisher()

# should launch lasers, camera, and teb_move_base
def init_clicked():
	lbl = Label(window)
	cp.command = 'launch sensors'
	cp.publish_command()
	lbl.grid(column=2,row=0)
	lbl.configure(text='Launching Sensors')

# should launch the protocol file
def launch_clicked():
	global cp
	cp.command = 'launch sanitation protocol'
	cp.publish_command()
	lbl = Label(window)
	lbl.grid(column=2,row=1)
	lbl.configure(text='Starting Protocol')
	

# run the GUI application
window = Tk()
# create instance command_publisher class 

window.geometry('480x480')
window.title("ICURObot Startup Application")

# create labels and buttons
init_lbl = Label(window,text='Initialize Robot Sensors')
init_lbl.grid(column=0,row=0)

#frame1 = Frame(window, height=32, width=32, bg="red")
#frame1.pack()

btn = Button(window,text='Launch Initialization Script',command=init_clicked,bg="red")
btn.grid(column=1,row=0,)

run_lbl = Label(window,text='Click To Begin ')
run_lbl.grid(column=0,row=1)

run_btn = Button(window,text='Launch Sanitation Protocol',command=launch_clicked)
run_btn.grid(column=1,row=1)


# execute window main loop
window.mainloop()

if __name__ == '__main__':
	if __package__ is None:
		#print('package is none')
		from os import sys, path
		sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))



