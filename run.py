import argparse
import datetime
import time
import cv2
import numpy as np
import modules.google_cloud_platform_query as gc_query
import modules.opencvTracking as tracker
from modules.gestureEngine import updateGesture
from modules.controlBrowser import Browser
import modules.speech

#Constant stream of video with browser actions and API calls based on gestures
def run(camera, browser, current_time):
    prevDirection = ''
    horizontal = ['left', 'right']
    vertical = ['up', 'down']

    while(True):
        # capture frame-by-frame
        ret, frame = camera.read()
        delta = time.time() - current_time
        # Display the resulting frame
        cv2.imwrite("./assets/videoframe.jpg", frame)

        #Detect the face and look for changes in gestures
        try:
            rect = tracker.faceDetect(frame)
            direction = updateGesture(frame, rect)

            if prevDirection is "up" or prevDirection is "down":
                if delta > 0.5:
                    browser.scroll(prevDirection)
                    current_time = time.time()
            #Determine browser action based on gesture
            if direction is not prevDirection and direction is not "":
                if direction in horizontal:
                    browser.switchTabs(direction)
                elif direction in vertical:
                    browser.scroll(direction)
                    current_time = time.time()

            if direction is not "":
                prevDirection = direction

        except Exception as e:
            print('ERROR:', e)

        cv2.imshow('frame', frame)

        #Quit with 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return

def close(camera, browser):
    browser.close()
    camera.release()
    cv2.destroyAllWindows()

def main():
    #open browser
    browser = Browser()

    camera = cv2.VideoCapture(0)
    #modules.speech.main()
    run(camera, browser, time.time())

    close(camera, browser)

if __name__ == "__main__":
    main()
