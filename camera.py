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

#Compare subsequent calculations against the first frame captured
ret, initFrame = cap.read()
cv2.imwrite("initialFrame.jpg", initFrame)
initPan, initTilt = gc_query.getAnnotations("initialFrame.jpg")

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    delta = time.time() - current_time
    current_time = time.time()

    # Display the resulting frame
    cv2.imwrite("videoframe.jpg", frame)
    #pan, tilt = gc_query.getAnnotations("videoframe.jpg")
    #rect = annotations.bounding_poly.vertices
    try:
        rect = tracker.faceDetect(gray)[0]
        gestureEngine.updateGesture(gray, rect)
    except Exception:
        print("face not in frame")

    cv2.imshow('frame', frame)
    print ("fps: " + str(1/delta))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
