import argparse
import datetime
<<<<<<< HEAD

=======
>>>>>>> fa81bffedc2fbdbc0c2e9d46b685c15cef21a497
import time
import cv2
import numpy as np
import google_cloud_platform_query as gc_query
import opencvTracking as tracker
import gestureEngine
from controlBrowser import Browser

#Validates the initial frame and returns original pan and tilt positions
def initFrame(camera):
    initPan = None
    #Compare subsequent calculations against the first frame captured
    #Make sure first frame is valid
    while not initPan:
        ret, initFrame = camera.read()
        cv2.imwrite("initialFrame.jpg", initFrame)
        initPan, initTilt = gc_query.getAnnotations("initialFrame.jpg")

    return (initPan, initTilt)

#Constant stream of video with browser actions and API calls based on gestures
def run(camera, browser, current_time):
    while(True):
        # capture frame-by-frame
        ret, frame = camera.read()
        delta = time.time() - current_time
        current_time = time.time()

        # Display the resulting frame
        cv2.imwrite("videoframe.jpg", frame)
        #pan, tilt = gc_query.getAnnotations("videoframe.jpg")
        #rect = annotations.bounding_poly.vertices
        try:
            rect = tracker.faceDetect(frame)
            gesture = gestureEngine.updateGesture(frame, rect)
            if gesture is not "":
                if gesture is "left" or gesture is "right":
                    browser.switchTabs(gesture)
                elif gesture is "up" or gesture is "down":
                    browser.scroll(gesture)
                #time.sleep(2)
        except Exception as e:
            print(e)
            print("face not in frame")

        cv2.imshow('frame', frame)
        #print ("fps: " + str(1/delta))

        #Quit with 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return

def close(camera):
    # When everything done, release the capture
    camera.release()
    cv2.destroyAllWindows()

def main():
    #open browser
    browser = Browser()
    current_time = time.time()
    camera = cv2.VideoCapture(0)
    initPan, initTilt = initFrame(camera)

    run(camera, browser, current_time)

    close(camera)

if __name__ == "__main__":
    main()
