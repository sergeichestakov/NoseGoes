# import the necessary packages
import argparse
import datetime
import imutils
import time
import cv2
import numpy as np
import google_cloud_platform_query as gc_query
import opencvTracking as tracker
import gestureEngine

current_time = time.time()

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    delta = time.time() - current_time
    current_time = time.time()
    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = frame # not really gray here
    # Display the resulting frame
    cv2.imwrite("videoframe.jpg", frame)
    # annotations = gc_query.getAnnotations("videoframe.jpg")[0]
    # rect = annotations.bounding_poly.vertices
    try:
        rect = tracker.faceDetect(gray)[0]
        print(rect[0].x)
        gestureEngine.updateGesture(gray, rect)
    except Exception, e:
        print(e)
        print("face not in frame")

    cv2.imshow('frame', gray)
    print ("fps: " + str(1/delta))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
