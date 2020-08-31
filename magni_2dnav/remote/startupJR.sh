python check_ip_JR.py

parallel -u ::: 'rosrun magni_2dnav startupGUI2.py' 'roslaunch magni_2dnav remote_start_JR.launch'

#xterm -e rosrun magni_2dnav startupGUI.py 
#xterm -e roslaunch magni_2dnav remote_start.launch
