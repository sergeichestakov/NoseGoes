# import the necessary packages
import argparse
import datetime
import imutils
import time
import cv2
import numpy as np
import google_cloud_platform_query as gc_query

current_time = time.time()

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    delta = time.time() - current_time
    current_time = time.time()
    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = frame
    # Display the resulting frame
    cv2.imwrite("videoframe.jpg", frame)
    annotations = gc_query.getCoordinatesOfFace("videoframe.jpg")[0]
    rect = annotations.bounding_poly.vertices
    cv2.rectangle(gray, (int(rect[0].x), int(rect[0].y)), (int(rect[2].x), int(rect[2].y)), color=(0,255,0), thickness=2)

    

    cv2.imshow('frame', gray)
    print ("fps: " + str(1/delta))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
