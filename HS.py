# -*- coding: utf-8 -*-
"""
Created on Fri May 28 00:18:10 2021

@author: ulyss
"""
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy
import smtplib
from email.message import EmailMessage
import os
import imghdr
#initialize cam instance & parameters
cam=PiCamera()
cam.resolution=(480,360)
cam.framerate=24
time.sleep(2)
Capture=PiRGBArray(cam, size=(480,360))

def get_camStream():
    #Load a cascade file for detecting faces
    face_cascade = cv2.CascadeClassifier('/home/pi/Documents/8f51e58ac0813cb695f3733926c77f52-07eed8d5486b1abff88d7e34891f1326a9b6a6f5/haarcascade_frontalface_default.xml')

    for frame in cam.capture_continuous(Capture, format="bgr", use_video_port=True):

        #get NP array holding image
        image=frame.array

        #Convert to grayscale
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        #Look for faces in the image using the loaded cascade file
        faces = face_cascade.detectMultiScale(image, 1.1, 5,minSize=(30,30))

        #Draw a rectangle around every found face
        for (x,y,w,h) in faces:
            cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),2)
            cv2.imwrite("intruder.jpg",image)

        cv2.imshow("Frame", image)
        key=cv2.waitKey(1) & 0xFF
        Capture.truncate(0)
        if len(faces) > 0:
            return True
        else:
            return False


def send_email(subject,body,to):
    #print("Sending noti")
    msg=EmailMessage()
    msg.set_content(body)
    msg['subject']=subject
    msg['to']=to

    user = "tankycams@gmail.com"
    msg['from']= user
    password = 'nwprcsmmhohnjwjx'

    server=smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user,password)
    server.send_message(msg)

    server.quit()

def send_txt():
    msg=EmailMessage()

    msg['Subject']='INTRUDER ALERT, HELP MUTHAFUCKA'
    msg['To']='2099144867@mms.att.net'
    #msg['To']='ulyssesjuanjr@yahoo.com'

    msg.set_content('Picture Attached: ')

    user = "tankycams@gmail.com"
    msg['From']= user
    password = 'nwprcsmmhohnjwjx'

    with open('intruder.jpg', 'rb') as img:
        load=img.read()
        img_type=imghdr.what(img.name)
        img_name=img.name

    msg.add_attachment(load, maintype='image', subtype=img_type, filename=img_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login("tankycams@gmail.com",'nwprcsmmhohnjwjx')
        smtp.send_message(msg)


def main():

    get_camStream()
    while True:


        #time.sleep(3)
        if get_camStream():
            #print("Face func found face")
            #send_email("Intruder Alert",
            #"/nUnsuspected Indivudal in House Hallway, see picture", 
            #"2099144867@txt.att.net")
            time.sleep(10)
            send_txt()
            time.sleep(1)
            #send text here
        else:
            #print("No face was found")
            continue

if __name__ == "__main__":
    main()

#Convert the picture into a numpy array
#buff = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)

#Now creates an OpenCV image
#image = cv2.imdecode(buff, 1)

#Convert to grayscale
#gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)


#Save the result image
#cv2.imwrite('result3.jpg',image)