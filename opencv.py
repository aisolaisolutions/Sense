#import the necessary packages
from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2
# initialize the camera and grab a reference to the raw camera capture
vs = VideoStream(src=0).start()
time.sleep(1.0)
# capture frames from the camera
while True:
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
    frame = vs.read()
    frame = imutils.resize(frame, width=500)
	
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
	
	# clear the stream in preparation for the next frame
	#rawCapture.truncate(0)
	# if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
# # do a bit of cleanup
# cv2.destroyAllWindows()
# vs.stop()