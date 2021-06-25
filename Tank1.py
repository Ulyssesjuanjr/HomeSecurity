from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy
import smtplib
from email.message import EmailMessage
import os
import imghdr

import RPi.GPIO as IO


#initialize cam instance & parameters
cam=PiCamera()
cam.resolution=(480,360)
cam.framerate=24
time.sleep(2)
Capture=PiRGBArray(cam, size=(480,360))

IO.setwarnings(False) #ignore warnings
IO.setmode(IO.BOARD) #initialize GPIO board on RPI
IO.setup(3,IO.OUT) #configure pin 3 on GPIO RPI
    

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
        
#creating parameters incase need to send email to multiple people
def send_email(subject,body,to):
    
    #create email message object to instantiate
    msg=EmailMessage()
    msg.set_content(body)
    msg['subject']=subject
    msg['to']=to
    
    #plug in message info: to,from,account info
    user = "tankycams@gmail.com"
    msg['from']= user
    password = 'nwprcsmmhohnjwjx'
    
     #read image file assign to variable
    with open('intruder.jpg', 'rb') as img:
        load=img.read()
        #optional to check what type of image file file is, I have set mine here to a JPEG
        img_type=imghdr.what(img.name)
        img_name=img.name
    
    #load image into message 
    msg.add_attachment(load, maintype='image', subtype=img_type, filename=img_name)
    
    
    #start server SMTP instance to begin email sends
    server=smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user,password)
    server.send_message(msg)
    
    server.quit()
    
#leaving paramters blank here, only 1 person will receive txt messages
def send_txt():
    msg=EmailMessage()
    
    #message info
    msg['Subject']='INTRUDER ALERT, HELP MUTHAFUCKA'
    #info retrieved from digital trends website. Particular carries info varies.
    msg['To']='2099144867@mms.att.net'
    msg.set_content('Picture Attached: ')
    
    user = "tankycams@gmail.com"
    msg['From']= user
    password = 'nwprcsmmhohnjwjx'
    
    #read image file assign to variable
    with open('intruder.jpg', 'rb') as img:
        load=img.read()
        #optional to check what type of image file file is, I have set mine here to a JPEG
        img_type=imghdr.what(img.name)
        img_name=img.name
    
    #load image into message 
    msg.add_attachment(load, maintype='image', subtype=img_type, filename=img_name)
    
    #start SMTP Service, login and send message
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login("tankycams@gmail.com",'nwprcsmmhohnjwjx')
        smtp.send_message(msg)
        
def LED_ON():
   
    IO.output(3,1) #send digital high signal (5V) on pin 3 ***Turn LED on
    
def LED_OFF():
    IO.output(3,0) # send digial low to pint 3 ***Turn LED off
    
def PIR_sensor():
    IO.setup(11,IO.IN) # read output from PIR
    
    while True:
        get=IO.input(11)
        if get==0:
            print('no motion detected')
            IO.output(3,0)
            time.sleep(1)
        elif get==1:
            print('motion detected')
            IO.output(3,1)
            time.sleep(1)

def main():
    
    get_camStream()
    PIR_sensor()
    while True:
        
        if get_camStream():
            LED_ON()
            send_email("Intruder Alert",
            "/nUnsuspected Indivudal in House Hallway, see picture", 
            "ulyssesjuanjr@Yahoo.com")
            time.sleep(4)
            send_txt()
            time.sleep(1)
            
        else:
            LED_OFF()
            continue
            
if __name__ == "__main__":
    main()
        

