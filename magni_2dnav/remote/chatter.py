#!/usr/bin/env python
import os
from Tkinter import *
#from Tkinter import scrolledtext
#from Tkinter import tkinter as tk 
#from Tkinter import ttk 
#from Tkinter import scrolledtext
from std_msgs.msg import String
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
global con_string
global san_string 


class command_publisher:
	def __init__(self):

		rospy.init_node('StartupGUI', anonymous=True)
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
	global con_string 
	global cp 
	#lbl1 = Label(window)
	cp.command = 'launch protocol'
	cp.publish_command()
	#lbl1.grid(column=3,row=7)
	#lbl1.config(font=("Comic Sans MS",20) )                       
	#lbl1.configure(text='Cleaning Cycle Initiated')
	con_string = "Cleaning Cycle Initiated"
	san_string = "Moving to Sanitation Zone 1"



# should launch the protocol file
def gohome_clicked():
	global con_string 
	global san_string 
	global cp
	cp.command = 'go home'
	cp.publish_command()
	#lbl2 = Label(window)
	#lbl2.grid(column=3,row=10)	
	#lbl2.config(font=("Comic Sans MS",20) )
	#lbl2.configure(text='Returning to Base Station')
	con_string = "Returning to Base Station"


	# should launch the protocol file
def openMap_clicked():
	global con_string 
	global cp
	cp.command = 'open map'
	cp.publish_command()
	#lbl3 = Label(window)
	#lbl3.grid(column=3,row=12)
	#lbl3.config(font=("Comic Sans MS",20) )	
	#lbl3.configure(text='map opened')
	con_string = "Opening Map"
	os.system('rviz')

		# should launch the protocol file
def shutdown_clicked():
	global con_string 
	global cp
	cp.command = 'shutdown'
	cp.publish_command()
	#lbl4 = Label(window)
	#lbl4.grid(column=3,row=13)
	#lbl4.config(font=("Comic Sans MS",20) )
	#lbl4.configure(text='shutdown initiated')
	con_string = "Shutdown Initiated"
	

def magniChecking(data):
#	print "callback called"
	global t_string
	global b_string 
	global v_string
	global p_string 
	global s_string 
	global con_string
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

header_lbl = Label(window, text = "Sanitization Robot")
header_lbl.config(font=("Comic Sans MS", 75, 'bold'), fg="#ff6d00")
header_lbl.grid(column=5,row=2, padx = (5,5), pady=10)

empty_lbl = Label(window,text = "  ")
empty_lbl.grid(column=0,row=6, padx = 1, pady = 30, columnspan = 20)


# create labels and buttons
#init_lbl = Label(window,text='Start Cleaning')
#init_lbl.config(font=("Comic Sans MS",20))
#init_lbl.grid(column=1,row=7, padx = (0,0))

btn = Button(window,text='Launch Sanitization Protocol',command=launch_clicked, bd=4, bg="orange",fg="white")
btn.config(font=("Comic Sans MS",20))
btn.grid(column=0,row=7, pady=5, padx = (10,1) )


#run_lbl = Label(window,text='Go Home')
#run_lbl.config(font=("Comic Sans MS",20))
#run_lbl.grid(column=1,row=10, padx = (2,1))

run_btn = Button(window,text='Return to Base Station',command=gohome_clicked,bd=4, bg="orange",fg="white")
run_btn.config(font=("Comic Sans MS",20))
run_btn.grid(column=0,row=10, pady = 5, padx =(10,1))

empty_lbl2 = Label(window,text = "  ")
empty_lbl2.grid(column=0,row=11, padx = 1, pady = 20, columnspan = 20)

#map_lbl = Label(window,text='Open Map')
#map_lbl.config(font=("Comic Sans MS",20))
#map_lbl.grid(column=1,row=12, padx = (2,1))

map_btn = Button(window,text='Vizualize Map',command=openMap_clicked,bd=4, bg="#0375be",fg="white")
map_btn.config(font=("Comic Sans MS",20))
map_btn.grid(column=0,row=12, pady = 5, padx =(10,1))

#shutdown_lbl = Label(window,text='Go Home')
#shutdown_lbl.config(font=("Comic Sans MS",20))
#shutdown_lbl.grid(column=1,row=13, padx = (2,1))

shutdown_btn = Button(window,text='Shutdown Robot',command=shutdown_clicked,bd=4, bg="red",fg="white")
shutdown_btn.config(font=("Comic Sans MS",20))
shutdown_btn.grid(column=0,row=13, pady = 5, padx =(10,1))


#add Icuro Image to GUI
img = PhotoImage(file = "ICURO-logo-49-original.png") 
img1 = img.subsample(3, 3) 
  

Label(window, image= img1).grid(row = 0, column = 0, columnspan = 5, rowspan = 5, padx = (5,5), pady = (18,1))


empty_lbl3 = Label(window,text = "  ")
empty_lbl3.grid(column=1,row=14, padx = 1, pady = 20)

#Initialize processing strings 
t_string = ''
b_string = ''
v_string = ''
p_string = ''
s_string = ''
con_string = ''
san_string = ''
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
 

status_lbl = Label(window,text="Control Log:")
status_lbl.config(font=("Comic Sans MS",20))
status_lbl.grid(column=6,row=18, padx = 1, pady = 5, sticky=E)


control_status = StringVar()
control_lbl = Label(window,textvariable=control_status)
control_lbl.config(font=("Comic Sans MS",20))
control_lbl.grid(column=7,row=18, padx = 1, pady = 5, sticky=W)

control_status.set("                       ") 

status2_lbl = Label(window,text="Sanitation Log:")
status2_lbl.config(font=("Comic Sans MS",20))
status2_lbl.grid(column=6,row=19, padx = 1, pady = 5, sticky=E)


sanitation_status = StringVar()
sanitation_lbl = Label(window,textvariable=sanitation_status)
sanitation_lbl.config(font=("Comic Sans MS",20))
sanitation_lbl.grid(column=7,row=19, padx = 1, pady = 5, sticky=W)
sanitation_status.set("                         ")

#

#Scolling Text Windows for Status Information

#scrolling_lbl = Label(window, text = "Scrolling Text Widget Example ", font = ("Comic Sans MS",15), fg = "#0375be")
#scrolling_lbl.grid(column = 11, row = 7)
#text_area = ScrolledText(window, wrap = tk.WORD, width = 40, height = 10, font = ("Comic Sans MS", 15))

#text_area.grid(column = 11, row = 8)


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
		
	control_status.set(con_string)
	sanitation_status.set(san_string)

	#Update GUI 
	window.update_idletasks()
	window.update()


if __name__ == '__main__':
	if __package__ is None:
		#print('package is none')
		from os import sys, path
		sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

