# USAGE
# python detect_mask_video.py

# Final Code Sameer Ahmed
# import the necessary packages
import pygame
from picamera.array import PiRGBArray
from picamera import PiCamera
import tensorflow
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2
import os
import serial # Serial port initialize 
from playsound import playsound
import RPi.GPIO as GPIO #Led blink
import pyttsx3
import pigpio
#Arduino to Respberry pi connection
#ser=serial.Serial("/dev/ttyACM0",9600)  #change ACM number as found from ls /dev/tty/ACM*

#ACMO to USBO
pi = pigpio.pi()

ser=serial.Serial("/dev/ttyUSB0",9600)  #change USB number as found from ls /dev/tty/USB* 9600 to 2000000
ser.baudrate=9600


GPIO.setmode(GPIO.BCM)

#IR Sensor
GPIO.setup(26, GPIO.IN)

#Ultrasonic Sensor
TRIG = 7
ECHO = 12
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)


#Iluminas Led
I_Led =16
GPIO.setup(I_Led,GPIO.OUT)

#RED Led
red_led =20
GPIO.setup(red_led,GPIO.OUT)

#Green Led
green_led =21
GPIO.setup(green_led,GPIO.OUT)


def detect_and_predict_mask(frame, faceNet, maskNet):
	# grab the dimensions of the frame and then construct a blob
	# from it
	(h, w) = frame.shape[:2]
	blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),
		(104.0, 177.0, 123.0))

	# pass the blob through the network and obtain the face detections
	faceNet.setInput(blob)
	detections = faceNet.forward()

	# initialize our list of faces, their corresponding locations,
	# and the list of predictions from our face mask network
	faces = []
	locs = []
	preds = []

	# loop over the detections
	for i in range(0, detections.shape[2]):
		# extract the confidence (i.e., probability) associated with
		# the detection
		confidence = detections[0, 0, i, 2]

		# filter out weak detections by ensuring the confidence is
		# greater than the minimum confidence
		if confidence > args["confidence"]:
			# compute the (x, y)-coordinates of the bounding box for
			# the object
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")

			# ensure the bounding boxes fall within the dimensions of
			# the frame
			(startX, startY) = (max(0, startX), max(0, startY))
			(endX, endY) = (min(w - 1, endX), min(h - 1, endY))
			# extract the face ROI, convert it from BGR to RGB channel
			# ordering, resize it to 224x224, and preprocess it
			face = frame[startY:endY, startX:endX]
			
			try:
				face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
				face = cv2.resize(face, (224, 224))
				face = img_to_array(face)
				face = preprocess_input(face)
				face = np.expand_dims(face, axis=0)

				# add the face and bounding boxes to their respective
				# lists
				faces.append(face)
				locs.append((startX, startY, endX, endY))

			except:
				pass

	# only make a predictions if at least one face was detected
	if len(faces) > 0:
		# for faster inference we'll make batch predictions on *all*
		# faces at the same time rather than one-by-one predictions
		# in the above `for` loop
		preds = maskNet.predict(faces)

	# return a 2-tuple of the face locations and their corresponding
	# locations
	return (locs, preds)

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--face", type=str,
	default="/home/pi/Mask_Detection_CV/face_detector",
	help="path to face detector model directory")
ap.add_argument("-m", "--model", type=str,
	default="mask_detector.model",
	help="path to trained face mask detector model")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

# load our serialized face detector model from disk
print("[INFO] loading face detector model...")
prototxtPath = os.path.sep.join([args["face"], "deploy.prototxt"])
weightsPath = os.path.sep.join([args["face"],
	"res10_300x300_ssd_iter_140000.caffemodel"])
faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

# load the face mask detector model from disk
print("[INFO] loading face mask detector model...")

# Changes
print("Args..")
print(args)
print("Args Model.. ")
print(args["model"])
#maskNet = load_model(args["model"])
maskNet = tensorflow.keras.models.load_model("/home/pi/Mask_Detection_CV/mask_detector.model")
#Changes Closed

# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")

#led iluminas on
GPIO.output(I_Led, True)

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 40
rawCapture = PiRGBArray(camera, size=(640, 480))
# allow the camera to warmup
time.sleep(0.1)

#Sound Play
def play_audio(path_of_audio):
    
    pygame.mixer.init()
    pygame.mixer.music.load(path_of_audio)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
    """engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()"""
	
label_details = ["Mask"]
temperature_detail = ["High"]
print(len(label_details))

# loop over the frames from the video stream
for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
	frame = image.array
	# show the frame
	

	# detect faces in the frame and determine if they are wearing a
	# face mask or not
	(locs, preds) = detect_and_predict_mask(frame, faceNet, maskNet)

	# IR Initialize
	sensor = GPIO.input(26)
	#Ultrasonic Sensor Define

	GPIO.output(TRIG, 0)
	time.sleep(0.1)
	print("Starting Measurment...")
	GPIO.output(TRIG, 1)
	time.sleep(0.00001)
	GPIO.output(TRIG, 0)

	while GPIO.input(ECHO) == 0:
		pass
	start = time.time()

	while GPIO.input(ECHO) == 1:
		pass
	stop = time.time()
	ultrasonic_time = (stop - start) * 17000
	from decimal import Decimal
	ultrasonic_time = Decimal(ultrasonic_time)
	ultrasonic_time = round(ultrasonic_time,2)

	print("Ultrasonic Time :",ultrasonic_time)
	
	print("Unique File")
	print(label_details)
	if ultrasonic_time <= 25.0:
		if len(label_details) >= 3:
			if label_details.count("Mask") >= 3:
				play_audio('/home/pi/Mask_Detection_CV/Mask_Detected.mp3')
				#pi.set_PWM_dutycycle(22,255)#green
				GPIO.output(red_led, False)
				GPIO.output(green_led, True)
				label_details = ["Mask"]
				print("Mask Cell ma gaya ha")
				print("\n Detect Mask \n")
			elif label_details.count("No Mask") >= 3:
				play_audio('/home/pi/Mask_Detection_CV/Mask_Missing.mp3')
				GPIO.output(red_led, True)
				GPIO.output(green_led, False)
				#pi.set_PWM_dutycycle(17,255) #red
				#pi.set_PWM_dutycycle(22,0) #red
				label_details = ["No Mask"]
				print("No Mask waly cell ma gaya ha")
				print("\n Detect No Mask \n")
			else:

				pass
	
	# loop over the detected face locations and their corresponding
	# locations
	
	
	
	## Code edit for arduino Wired communication

	read_ser=ser.readline()
	command = read_ser.decode("utf-8").strip()#Convert byte to string ASCII utf-8
	print(command)
	print(type(command)) #Edit Sameer'
	#pi.set_PWM_dutycycle(17,0) #off
	#pi.set_PWM_dutycycle(22,0) #off
	#pi.set_PWM_dutycycle(23,0) #off

	

	"""
        #Arduino To respberry pi conncection
	read_ser=ser.readline()
	print(read_ser)

	#Ultrasonic Sensor Connection
	if (command.strip()=="Come Closer"):
		print("Your Distance is >20 cm \n Please Come Closer")
	
	else:
		#Arduino To respberry pi conncection
                        if(command.strip()=="Temperature Excide"):  # strip method to remove termination character
			print(command)
			prin("Temeperature > 40")
			#print(1)
			#Buzzur beep beep
			GPIO.output(23, True)#Temperature Excide
			time.sleep(.1)
			GPIO.output(23, False)#Temperature Excide
			time.sleep(.1)
			GPIO.output(23, True)#Temperature Excide
			time.sleep(.1)
			GPIO.output(23, False)#Temperature Excide
			time.sleep(.1)
			GPIO.output(23, True)#Temperature Excide
			time.sleep(.1)
			GPIO.output(23, False)#Temperature Excide
			time.sleep(.1)
			GPIO.output(23, True)#Temperature Excide
			time.sleep(.1)
			GPIO.output(23, False)#Temperature Excide
			time.sleep(.1)
			GPIO.output(23, True)#Temperature Excide
			time.sleep(.1)
			GPIO.output(23, False)#Temperature Excide
			time.sleep(.1)

		else:
			print(command)
			print("Temeperature < 40")
			#print(2)
			#Buzzur
			GPIO.output(23, False)#Temperature Normal"""

	
	
	for (box, pred) in zip(locs, preds):
            
		# unpack the bounding box and predictions
		(startX, startY, endX, endY) = box
		(mask, withoutMask) = pred
		#label = "Null"

		# determine the class label and color we'll use to draw
		# the bounding box and text
		#label = "Mask" if mask > withoutMask else "No Mask"
		if mask > withoutMask:
                    
			
			#global label
			label = "Mask"
			label_details.append(label)
			print("\n ***** Detect Mask ***** \n")
			# Led Declear
			#GPIO.output(18, False)
			#print(label_details)
			
		    
			"""
			#Arduino To respberry pi conncection
			if(command.strip()=="Temperature Excide"):  # strip method to remove termination character
				print("Temeperature > 40")
				#print(1)
				#Buzzur
				GPIO.output(23, True)#Temperature Excide
				
			else:
				print("Temeperature < 40")
				#print(2)
				#Buzzur
				GPIO.output(23, False)#Temperature Normal"""
		else:
                    
			
			#global label
			label = "No Mask"
			label_details.append(label)
			print("\n ***** Detect No Mask ***** \n")

			# Led Declear
			#GPIO.output(18, True)

			#Buzzur
			#GPIO.output(22, True)#Mask Not detect
			
			#Buzzur beep beep Mask Not detect
			
			
			#print(label_details)
			"""
			#Arduino To respberry pi conncection
			if(command.strip()=="Temperature Excide"):
				print("Temeperature > 40")
				#print(3)
				#Buzzur
				GPIO.output(23, True)#Temperature Excide
			else:
				print("Temeperature < 40")
				#print(4)
				#Buzzur
				GPIO.output(23, False)#Temperature Normal"""
				
		"""		
		#Arduino To respberry pi conncection
		if(command.strip()=="Temperature Excide"):  # strip method to remove termination character
			print("Temeperature > 40")
			#print(1)
			#Buzzur
			GPIO.output(23, True)#Temperature Excide
				
		else:
                        print("Temeperature < 40")
			#print(2)
			#Buzzur
			GPIO.output(23, False)#Temperature Normal """
			
			
			
		color = (0, 255, 0) if label == "Mask" else (0, 0, 255)

		#print(label_details)
		#print(len(label_details))


		# include the probability in the label
		label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)

		# display the label and bounding box rectangle on the output
		# frame
		cv2.putText(frame, label, (startX, startY - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
		cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

                
        #Ir Sensor Coniditon

	print(sensor)
	#Display Temperature and distance
	
	temp = "Temperature : "+command+" C "
	command = float(command)
	dist = "Distance : "+str(ultrasonic_time)+" cm"
	
	
	
    
	if ultrasonic_time >25.0:
            GPIO.output(red_led, False)
            GPIO.output(green_led, False)
            #print(label)
            dist = "Distance : Out Of Range"
            #play_a    udio('Come Closer')
            #pi.set_PWM_dutycycle(17,0) #off
            #pi.set_PWM_dutycycle(22,0) #off
            #pi.set_PWM_dutycycle(23,0) #off
            #temp = temp+" (Room Temperature) "
            """
            if command >=36.8:

                cv2.putText(frame, temp, (10,50),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

            else:
                cv2.putText(frame, temp, (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            """


            cv2.putText(frame, dist, (10,90),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
            
	
	elif ultrasonic_time <=25.0:
            #print(label)
            dist = "Distance : In Range"
            temp = "Temperature"
            if command >=36.0:
                GPIO.output(red_led, True)
                GPIO.output(green_led, False)
                temp = temp+" High"
                temperature_detail.append("High")
                if len(temperature_detail) >= 5:
                    if temperature_detail.count("High") == 5:
                        play_audio('/home/pi/Mask_Detection_CV/Temp_High.mp3')
                        temperature_detail = ["High"]


                cv2.putText(frame, temp, (10,50),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
                
            else:
                temp = temp+" Normal"
                #GPIO.output(red_led, False)
                #GPIO.output(green_led, True)
                #pi.set_PWM_dutycycle(22,255)#green
                if ultrasonic_time <= 25.0:
                    if len(label_details) >= 5:
                        if label_details.count("Mask") == 5:
                            GPIO.output(red_led, False)
                            GPIO.output(green_led, True)
                            play_audio('/home/pi/Mask_Detection_CV/Clear.mp3')
                            #pi.set_PWM_dutycycle(22,255)#green
                            label_details = ["Mask"]
                            print("Mask Cell ma gaya ha")
                            print("\n Detect Mask \n")
                    elif label_details.count("No Mask") == 5:
                            GPIO.output(red_led, True)
                            GPIO.output(green_led, False)
                            play_audio('/home/pi/Mask_Detection_CV/Mask_Missing.mp3')
                            #pi.set_PWM_dutycycle(17,255)
                            #pi.set_PWM_dutycycle(22,0) #red
                            label_details = ["No Mask"]
                            print("No Mask waly cell ma gaya ha")
                            print("\n Detect No Mask \n")
                    else:
                            pass
                    cv2.putText(frame, temp, (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    cv2.putText(frame, dist, (10, 90),
						cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)



# show the output frame
	cv2.imshow("Frame", frame)
	
	key = cv2.waitKey(1) & 0xFF
	rawCapture.truncate(0)

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
            break


GPIO.output(I_Led, False)
# do a bit of cleanup
cv2.destroyAllWindows()
#vs.stop()



