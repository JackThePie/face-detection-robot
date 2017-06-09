''' Code for Raspberry Pi robot. When it detects face using Raspberry camera it salutes.
by Jacek Bera '''


import io
import picamera
import cv2
import numpy
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)  		#relay
GPIO.setup(5,GPIO.OUT)  		#servo 1483 (upper)
GPIO.setup(7,GPIO.OUT)  		#servo 1472 (lower)
pwm1=GPIO.PWM(5,50)
pwm2=GPIO.PWM(7,50)

while True:
#camera stream
    stream = io.BytesIO()

#lowering resolution for faster calculation
    with picamera.PiCamera() as camera:
        camera.resolution = (160, 120)
        camera.capture(stream, format='jpeg')

#photo to array
    buff = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)

#openCV image creation
    image = cv2.imdecode(buff, 1)

#Include Haar method for detecting face
    face_cascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml')

#convert to greyscale
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

#search for face
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

#number of faces indication
    print "Found "+str(len(faces))+" face(s)"
#when Raspberry detects face:
    if (len(faces)) > 0:
		#relay off
        GPIO.cleanup(11)
		#time.sleep(1)

		#arm up
        pwm1.start(3)   
        pwm2.start(3)   
        time.sleep(1.7)

		#stop
        pwm1.ChangeDutyCycle(7.05)
        pwm2.ChangeDutyCycle(7.04)   
		
		#hand up
        pwm1.ChangeDutyCycle(11)   
        time.sleep(1.75)
		
		#stop
        pwm1.ChangeDutyCycle(7.05)    

		#lower arm
        pwm2.ChangeDutyCycle(11)
        time.sleep(1.2)
		
		#stop
        pwm2.ChangeDutyCycle(7.05)
        pwm2.ChangeDutyCycle(7.04) 

		#relay on
        GPIO.setup(11,GPIO.OUT)
        GPIO.output(11,False)
	
	#wait 2 sec
    time.sleep(2)


#rectangle over detected face
#for (x,y,w,h) in faces:
#    cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)

#saving detection result image
#cv2.imwrite('result.jpg',image)
