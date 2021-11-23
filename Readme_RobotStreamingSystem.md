This project realizes a complete Robot System based om an ESP32 Camera front end SERVER
which transmits video to a laptop running a python video streaming window. The ESP32 provides 
a separate port for an XBOX Controller. The video  window and a python GUI
for the XBOX Controller are used for human operator robot control(teleop). The Controller
exchanges data (control and sensor) withe the ESP32. The python video window program also 
runs OpenCV for autonomous control. Autonomous routines are preprogrammed using the
XBOX Controller. THE XBOX CONTROLLER PROGRAM AND THE WINDOW PROGRAM CAN COMMUNICATE WITH 
EACH OTHER!!!

The ESP32 (in turn) transmits control data to an Arduino Mega and receives sensor
from the Mega, via I2C. The Mega, in turn, can run the robot actuators and processes sensor inputs,
although these tasks are not part of the project and are left to an interested reader. The Mega also
drives an OLED display using an SPI interface and U8G2. The display shows the IP address of the ESP32.

If the Mega requires the SPI interface for other purposes, a dedicated Arduino Pro Mini is shown 
connected the the Mega I2C bus and drives a duplicate display, for demonstration purposes..

This is a multi program project involving C++, HTML,Javascript, AJAX, and Python. Because of the
breadth of the project, some part of almost every program is based on code found in the literature 
or in Github and referenced appropriately. All code original to this project can be used freely and 
for any purpose.

An extensive tutorial describing the system is in process of being written.

BRIEF OPERATING INSTRUCTIONS

0.INSTALL ESP32 LIBRARIES. USE ESP 32 WROVER MODULE, HUGE APP, FLASH FREQ 80Mhz, 115,200
  upload
  
00.INSTALL PYTHON 3.6.5 IDLE is very convenient for 2 and 3 below. 

1.Run ROBOT_STREAMING_SERVER_P after inserting your SSID and PASSWORD

2.Put the IP address shown in the Serial Monitor into ROBOT_STREAMINg_CLIENT_P.py and run.

3.Put the ip address into ROBOT_STREAMING_XBOX_P.py and run. INSTANCE GUI MUST BE ACTIVE
  TO ENTER COMMANDS INTO CONTROLLER.
 
4.Check out communication between the two py programs.