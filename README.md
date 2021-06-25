# HomeSecurity
This repo contains the software used to run my current indoor home security system.

--This code is written in python 3.x in a linux environment (Raspberry Pi)

--The camera is triggered by a motion sensor connected to the RP's GPIO pins. This triggers the camera to search and capture human outline in frame and send the notifications (email/text with images; image example attached). The cameras live feed is on 24/7 and can be accessed via Remote/SSH.

--The hardware includes: Raspberry Pi 3 Model B+, Raspberry Pi Ribbon Powered NightVision Camera(any will work), TP-LINK POE Splitter,  Symbol 802.3 POE, 3 Ethernet Cat6 cables, Raspberry Pi Motion Sensor(any will work), GPIO Female/Male cables, 16GB microSD card

***Learnings
its significantly difficult to process high fps on a condensed processing chip (i.e my old RP3). Initially, I had the live feed of the camera running 24/7, not only did the RP3 experience heatsoak, the processing speed took a toll (15/sec). To compensate, I added in a simple GPIO infrared external signal to trigger the camera to display live feed for "X" amount of time and search for a object/face. 
Not the most ideal solution, but nonetheless, enough for an old RP3.
