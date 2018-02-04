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
initStats = gc_query.getAnnotations("initialFrame.jpg")[0]

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    delta = time.time() - current_time
    current_time = time.time()

    # Display the resulting frame
    cv2.imwrite("videoframe.jpg", frame)
    #annotations = gc_query.getAnnotations("videoframe.jpg")
    #rect = annotations.bounding_poly.vertices
    try:
<<<<<<< HEAD
        rect = tracker.faceDetect(frame)[0]
        print(rect[0].x)
        cv2.rectangle(frame, (int(rect[0].x), int(rect[0].y)), (int(rect[2].x), int(rect[2].y)), color=(0,255,0), thickness=2)
=======
        rect = tracker.faceDetect(gray)[0]
        gestureEngine.updateGesture(gray, rect)
>>>>>>> 6fe53e46204cc756e863b05cd64bb99e20f6607c
    except Exception:
        print("face not in frame")

    cv2.imshow('frame', frame)
    print ("fps: " + str(1/delta))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
