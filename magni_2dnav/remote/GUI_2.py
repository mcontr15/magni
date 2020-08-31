#!/usr/bin/env python3
import os
#from Tkinter import *
import tkinter as tk
import tkinter.scrolledtext as st
from tkinter import PhotoImage
from tkinter import StringVar
from sensor_msgs.msg import BatteryState
from nav_msgs.msg import Odometry
from std_msgs.msg import String
from custom_msgs.msg import bat_and_sol
import rospy
import time

global status_string1
global status_string2
global callback1_called
global callback2_called

global zString
global t
global current_time_now

class command_publisher:
        def __init__(self):
                rospy.init_node('StartupGUI2', anonymous=True)
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

#Helper Functions for Updating GUI Strings
#def updateStatus1(data):
    #global status_string1
    #global callback1_called
    #print(data)
    #print("call_back called")

    #status_string1 = str(data)
    #callback1_called = True
 

def updateStatus2(data):
	global status_string2
	global callback2_called
	global zString
	#print(data)
	#print("call_back called")

	# zones completed is just the first string
	for word in str(data).split():
		if word.isdigit():
			zString = 'Zones Completed: ' + word
			print('found a digit')
	status_string2 = current_time_now + str(data) + '\n'
	callback2_called = True 
	sanitation_file = open("sanitation_log_file.txt", "a")
	sanitation_file.write(status_string2)
	sanitation_file.close()

# launches the sanitation protocol
def launch_clicked():
        global status_string1
        global callback1_called
        #lbl1 = Label(window)
        cp.command = 'launch protocol'
        cp.publish_command()
        status_string1 = current_time_now + "Cleaning Cycle Initiated \n"
        callback1_called = True
        control_file = open("control_log_file.txt", "a")
        control_file.write(status_string1)
        control_file.close()



# runs the go home client
def gohome_clicked():
        global status_string1
        global callback1_called
        global cp
        cp.command = 'go home'
        cp.publish_command()
        status_string1 = current_time_now + "Returning to Base Station \n"
        callback1_called = True
        control_file = open("control_log_file.txt", "a")
        control_file.write(status_string1)
        control_file.close()

# Open RVIZ
def openMap_clicked():
        global status_string1
        global callback1_called
        cp.command = 'open map'
        cp.publish_command()
        status_string1 = current_time_now + "Opening Map \n"
        os.system('rviz')
        callback1_called = True
        control_file = open("control_log_file.txt", "a")
        control_file.write(status_string1)
        control_file.close()


#Clears text windows 
def clearwindow_clicked():
        global status_string1
        global callback1_called
        cp.command = 'Clearing Window 1'
        cp.publish_command()
        text_area.delete("1.0",tk.END)
        status_string1 = current_time_now + "Text Window 1 Cleared \n"
        callback1_called = True
        control_file = open("control_log_file.txt", "a")
        control_file.write(status_string1)
        control_file.close()

def clearwindow2_clicked():
        global status_string1
        global callback1_called
        cp.command = 'Clearing Window 2'
        cp.publish_command()
        text_area2.delete("1.0",tk.END)
        status_string1 = current_time_now + "Text Window 2 Cleared \n"
        callback1_called = True
        control_file = open("control_log_file.txt", "a")
        control_file.write(status_string1)
        control_file.close()


def magniChecking(data):
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
    

#Main Code
window = tk.Tk()

window.title("ICUROBot Application")

window.geometry('1530x840')

#Icuro Logo 
img = PhotoImage(file = "~/catkin_ws/src/magni/magni_2dnav/remote/ICURO-logo-49-original.png")
img1 = img.subsample(3, 3)

tk.Label(window, image= img1).grid(row = 0, column = 0, padx = 5, pady = 5)

#UI Title 
header_lbl = tk.Label(window, text = "Sanitization Robot", font = ("Comic Sans MS", 75, 'bold'), fg="#ff6d00").grid(column=1,row=0, columnspan = 2, padx = (20,10), pady = (35,10)) 

#UI Title
zoneString = StringVar()
zone_lbl = tk.Label(window, textvariable = zoneString, font = ("Comic Sans MS", 20, 'bold'), fg="#ff6d00").grid(column=1,row=6, rowspan = 2, padx = 5, pady = 5)
zoneString.set('Zones Completed: 0') 


#Launch Button
launch_btn = tk.Button(window, text= "Launch Sanitation Protocol", font = ("Comic Sans MS", 20), command = launch_clicked, bd = 4, bg = "#0375be", fg = "white").grid(column=0,row=2)


#Go Home Button
home_btn = tk.Button(window,text='Return to Base Station',font=("Comic Sans MS",20), command=gohome_clicked,bd=4, bg="#0375be",fg="white").grid(column=1,row=2)

#Map Button
map_btn = tk.Button(window, text= "Open Map", font = ("Comic Sans MS", 20), command = openMap_clicked, bd = 4, bg = "#ff6d00", fg = "white").grid(column=0,row=3, rowspan = 2)

#Clear Button1
clear_btn = tk.Button(window,text='Clear Control Log',font=("Comic Sans MS",20), command=clearwindow_clicked,bd=4, bg="red",fg="white").grid(column=1,row=3)


#Clear Button2
clear_btn = tk.Button(window,text='Clear Sanitation Log',font=("Comic Sans MS",20), command=clearwindow2_clicked,bd=4, bg="red",fg="white").grid(column=1,row=4)





# Creating scrolled text area 1
status_string1 = "User Interface Initialization Complete \n"
status_lbl1 = tk.Label(window, text = "User Control Log", font = ("Comic Sans MS", 20, 'bold'), fg = "#0375be").grid(column = 2, row=1)

text_area = st.ScrolledText(window, width = 60, height = 12, font = ("Comic Sans MS", 12))
text_area.grid(column = 2, row = 2, rowspan = 2, pady = 5, sticky='E') 
text_area.insert(tk.INSERT,status_string1)

callback1_called = False


# Creating scrolled text area2
status_string2 = "Awaiting Sanitation Instructions... \n"
status_lbl2 = tk.Label(window, text = "Sanitation Log", font = ("Comic Sans MS", 20, 'bold'), fg = "#0375be").grid(column = 2, row=4)

text_area2 = st.ScrolledText(window, width = 60,height = 15,font = ("Comic Sans MS", 12)) 
text_area2.grid(column = 2, row = 5, pady = 5, rowspan = 5, sticky='E') 
text_area2.insert(tk.INSERT, status_string2)

callback2_called = False

sub = rospy.Subscriber('/battery_and_solution', bat_and_sol, magniChecking) 
sub2 = rospy.Subscriber('/spray_status', String, updateStatus2)


# Create Labels for Magni Info 
#Initialize processing strings
t_string = ''
b_string = ''
v_string = ''
p_string = ''
s_string = ''
zString = 'Zones Completed: 0'
sub_flag = False

#Current Time
current_time = StringVar()
time_lbl = tk.Label(window,textvariable=current_time,font=("Comic Sans MS",20)).grid(column=0,row=5, padx = 1, pady = 5, sticky='W')

current_time.set("Time: ??? ")


# Battery Status
battery_status = StringVar()
battery_lbl = tk.Label(window,textvariable=battery_status,font=("Comic Sans MS",20)).grid(column=0,row=6, padx = 1, pady = 5, sticky='W')

battery_status.set("Battery Status Unknown ")


# Battery Voltage
voltage_level = StringVar()
voltage_lbl = tk.Label(window,textvariable=voltage_level, font=("Comic Sans MS",20)).grid(column=0,row=7, padx = 1, pady = 5, sticky='W')

voltage_level.set("Battery Voltage: ??? V")

# Battery Percentage
battery_percentage = StringVar()
percentage_lbl = tk.Label(window,textvariable=battery_percentage,font=("Comic Sans MS",20)).grid(column=0,row=8, padx = 1, pady = 5, sticky='W')

battery_percentage.set("Battery Percentage: ??? %")

# Solution Status
solution_status = StringVar()
solution_lbl = tk.Label(window,textvariable=solution_status,font=("Comic Sans MS",20)).grid(column=0,row=9, padx = 1, pady = 5, sticky='W')

solution_status.set("Solution Status Unknown")


while True: 
    #Update GUI
    window.update_idletasks()
    window.update()
    
    
    t = time.localtime()
    current_time_now = time.strftime("%D-%H:%M:%S --- ",t)
  
    if(sub_flag):
            current_time.set(t_string)
            battery_status.set(b_string)
            voltage_level.set(v_string)
            battery_percentage.set(p_string)
            solution_status.set(s_string)
            zoneString.set(zString)

    if callback1_called:
        #print("updating1")
        text_area.insert(tk.INSERT, status_string1)
        callback1_called = False

    
    if callback2_called:
        #print ("updating2")
        text_area2.insert(tk.INSERT, status_string2)
        callback2_called = False
