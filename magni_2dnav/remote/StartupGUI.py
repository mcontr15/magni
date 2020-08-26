#!/usr/bin/env python
import os
from Tkinter import *
from std_msgs.msg import String
from sensor_msgs.msg import BatteryState
from custom_msgs.msg import bat_and_sol
import rospy
import time

global cp
global sub_flag
global t_string
global b_string
global v_string
global p_string 
global s_string 


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
		now = rospy.Time.now()
		rospy.loginfo(self.command)
		#print('publishing...')
		self.pub.publish(self.command)
		#print('published!')

# create publisher class
cp = command_publisher()

# should launch lasers, camera, and teb_move_base
def launch_clicked():
	lbl1 = Label(window)
	cp.command = 'launch protocol'
	cp.publish_command()
	lbl1.grid(column=2,row=6)
	lbl1.configure(text='Cleaning Cycle Initiated')


# should launch the protocol file
def gohome_clicked():
	global cp
	cp.command = 'go home'
	cp.publish_command()
	lbl2 = Label(window)
	lbl2.grid(column=2,row=10)	
	lbl2.configure(text='Returning to Base Station')
	

def magniChecking(data):
	#print "callback called"
	global t_string
	global b_string 
	global v_string
	global p_string 
	global s_string 
	global sub_flag

	sub_flag = True
	t_string = "Time: " + data.runtime
	b_string = data.batStatus
	v_string = "Battery Voltage: " + str(data.voltage)[:5] + "V"
	p_string = "Battery Percentage: " + str(data.battery_percentage)[:5] + "%"
	s_string = data.solStatus
	#voltage_string.set("Hello World")
	#voltage_string.set(str(data.voltage) + "%")


print('starting application')
# run the GUI application
window = Tk()
# create instance command_publisher class 

window.geometry('1530x840')
window.title("ICURObot Startup Application")

header_lbl = Label(window, text = "Sanitization Robot UI")
header_lbl.config(font=("Comic Sans MS", 60, 'bold'), bg="#0375be", fg="white")
header_lbl.grid(column=0,row=1, columnspan = 10, rowspan = 4, padx = (20,50), pady=5)

empty_lbl = Label(window,text = "  ")
empty_lbl.grid(column=0,row=6, padx = 1, pady = 40, columnspan = 50)

# create labels and buttons
init_lbl = Label(window,text='Start Cleaning')
init_lbl.config(font=("Comic Sans MS",20))
init_lbl.grid(column=0,row=7, padx = (20,10))

btn = Button(window,text='Launch Sanitization Protocol',command=launch_clicked, bd=4, bg="orange",fg="white")
btn.config(font=("Comic Sans MS",20))
btn.grid(column=1,row=7, pady=5, padx = 5 )

run_lbl = Label(window,text='Go Home')
run_lbl.config(font=("Comic Sans MS",20))
run_lbl.grid(column=0,row=10, padx = (20,10))

run_btn = Button(window,text='Return to Base Station',command=gohome_clicked,bd=4, bg="orange",fg="white")
run_btn.config(font=("Comic Sans MS",20))
run_btn.grid(column=1,row=10, pady = 5, padx =5)

#add Icuro Image to GUI
img = PhotoImage(file = "/home/minotaur/catkin_ws/src/magni/magni_2dnav/remote/ICURO-logo-49-original.png") 
img1 = img.subsample(3, 3) 
  

Label(window, image= img1).grid(row = 0, column = 11, columnspan = 5, rowspan = 5, padx = (50,5), pady = (18,1))


empty_lbl2 = Label(window,text = "  ")
empty_lbl2.grid(column=1,row=14, padx = 1, pady = 110)

#Initialize processing strings 
t_string = ''
b_string = ''
v_string = ''
p_string = ''
s_string = ''
sub_flag = False


#Current Time
current_time = StringVar()
time_lbl = Label(window,textvariable=current_time)
time_lbl.config(font=("Comic Sans MS",20))
time_lbl.grid(column=0,row=15, padx = 1, pady = 5, sticky=W)

current_time.set("Time: ??? ")


# Battery Status
battery_status = StringVar()
battery_lbl = Label(window,textvariable=battery_status)
battery_lbl.config(font=("Comic Sans MS",20))
battery_lbl.grid(column=0,row=16, padx = 1, pady = 5, sticky=W)

battery_status.set("Battery Status Unknown ")


# Battery Voltage
voltage_level = StringVar()
voltage_lbl = Label(window,textvariable=voltage_level)
voltage_lbl.config(font=("Comic Sans MS",20))
voltage_lbl.grid(column=0,row=17, padx = 1, pady = 5, sticky=W)

voltage_level.set("Battery Voltage: ??? V")

# Battery Percentage 
battery_percentage = StringVar()
percentage_lbl = Label(window,textvariable=battery_percentage)
percentage_lbl.config(font=("Comic Sans MS",20))
percentage_lbl.grid(column=0,row=18, padx = 1, pady = 5, sticky=W)

battery_percentage.set("Battery Percentage: ??? %")

# Solution Status
solution_status = StringVar()
solution_lbl = Label(window,textvariable=solution_status)
solution_lbl.config(font=("Comic Sans MS",20))
solution_lbl.grid(column=0,row=19, padx = 1, pady = 5, sticky=W)

solution_status.set("Solution Status Unknown")
 


# execute window main loop
#window.mainloop()


while True:
	#update magni info through rostopic callback
	sub = rospy.Subscriber('/battery_and_solution', bat_and_sol, magniChecking)
	
	#update variable string paramters
	if(sub_flag):
		current_time.set(t_string)
		battery_status.set(b_string)
		voltage_level.set(v_string)
		battery_percentage.set(p_string)
		solution_status.set(s_string)

	#Update GUI 
	window.update_idletasks()
	window.update()


if __name__ == '__main__':
	if __package__ is None:
		#print('package is none')
		from os import sys, path
		sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))



