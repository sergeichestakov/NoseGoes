import cv2
from collections import deque
import time
from opencvTracking import Vertex
from google_cloud_platform_query import getAnnotations
from concurrent.futures import ThreadPoolExecutor

RESET_TIME = 1.5
DOWN_SCALE = 5
executor = ThreadPoolExecutor(max_workers=1)

class Box:
    def __init__(self, x, y, w, h):
        self.center = (x,y)
        self.w = w
        self.h = h
        self.topLeft = Vertex(x - w/2, y - h/2)
        self.topRight = Vertex(x + w/2, y - h/2)
        self.bottomLeft = Vertex(x - w/2, y + h/2)
        self.bottomRight = Vertex(x + w/2, y + h/2)

    def contains(self, point):
        return point.x > self.topLeft.x and point.x < self.topRight.x and point.y > self.topLeft.y and point.y < self.bottomLeft.y

    def right(self, point):
        return point.x < self.topLeft.x #and point.y < self.topLeft.y and point.y > self.bottomLeft.y
    def left(self, point):
        return point.x > self.topRight.x #and point.y < self.topRight.y and point.y > self.bottomRight.y
    def top(self, point):
        return point.y > self.topRight.y #and point.x < self.topRight.x and point.x > self.topLeft.x
    def bottom(self, point):
        return point.y < self.bottomLeft.y #and point.x < self.bottomRight.x and point.x > self.bottomLeft.x

class ExponentialSmoother:
    def __init__(self, x, a):
        self.s = x
        self.a = a
    def smooth(self, x):
        self.s = self.a * x + (1 - self.a) * self.s
        return self.s

class MovingAverageSmoother:
    def __init__(self, size):
        self.size = size
        self.data = deque()
    def smooth(self, x):
        self.data.append(x)
        if len(self.data) > self.size:
            self.data.popleft()
        return sum(self.data)/len(self.data)

smoothVar = {}
thresholdBox = None
currentTime = time.time()
future = None
retGesture = ""

def drawDebugUI(image, x, y, w, h):
    cv2.circle(image, center=(x, y), radius=2, color=(255,0,0))
    topLeft = Vertex(x - w / 2, y - h / 2)
    bottomRight = Vertex(x + w / 2, y + h / 2)
    cv2.rectangle(image, (topLeft.x, topLeft.y), (bottomRight.x, bottomRight.y), color=(0,255,0), thickness=2)

def setBox(x, y, w, h):
    global thresholdBox, currentTime
    thresholdBox = Box(x, y, int(w / DOWN_SCALE), int(h / DOWN_SCALE / 1.1))
    currentTime = time.time()

def updateThreshold(image, x, y, w, h):
    global thresholdBox, currentTime
    delta = time.time() - currentTime
    ret = ""
    if thresholdBox is not None:
        point = Vertex(x,y)

        #Point left the box: save direction and wait til it reenters
        if not thresholdBox.contains(point):
            if thresholdBox.left(point):
                currentTime = time.time()
                #print("looking left")
                ret = "left"
            elif thresholdBox.right(point):
                currentTime = time.time()
                #print("looking right")
                ret = "right"
            elif thresholdBox.top(point):
                currentTime = time.time()
                #print("looking down")
                ret = "down"
            elif thresholdBox.bottom(point):
                currentTime = time.time()
                #print("looking up")
                ret = "up"
        else:
            if delta > RESET_TIME:
                #setBox(x, y, w, h)
                pass
        cv2.rectangle(image, (thresholdBox.topLeft.x, thresholdBox.topLeft.y), (thresholdBox.bottomRight.x, thresholdBox.bottomRight.y), color=(255,255,0))
    else:
        if delta > RESET_TIME:
            setBox(x, y, w, h)
    return ret

def updateSmoothers(center, width, height):
    if "x" not in smoothVar:
        smoothVar["x"] = MovingAverageSmoother(3)
        smoothX = center[0]
    else:
        smoothX = int(smoothVar["x"].smooth(center[0]))
    if "y" not in smoothVar:
        smoothVar["y"] = MovingAverageSmoother(3)
        smoothY = center[1]
    else:
        smoothY = int(smoothVar["y"].smooth(center[1]))
    if "w" not in smoothVar:
        smoothVar["w"] = MovingAverageSmoother(5)
        smoothW = width
    else:
        smoothW = int(smoothVar["w"].smooth(width))
    if "h" not in smoothVar:
        smoothVar["h"] = MovingAverageSmoother(5)
        smoothH = height
    else:
        smoothH = int(smoothVar["h"].smooth(height))

    return (smoothX, smoothY, smoothW, smoothH)

def processAsyncGesture(answer):
    global future, retGesture
    (pan, tilt) = answer.result()
    future = None
    retGesture = "none"
    if pan < -15:
        retGesture = "right"
    elif pan > 15:
        retGesture = "left"
    elif tilt > 3:
        retGesture = "up"
    elif tilt < -4:
        retGesture = "down"

def updateGesture(image, face):
    # face format is [topLeft, topRight, bottomRight, bottomLeft]
    # each face is a Vertex with properties x and y
    global executor, future, retGesture, currentTime
    delta = time.time() - currentTime
    center = ((face[0].x + face[2].x) / 2, (face[0].y + face[2].y) / 2)
    width = face[2].x - face[0].x
    height = face[2].y - face[0].y
    (x, y, w, h) = updateSmoothers(center, width, height)
    retDirection = ""
    direction = updateThreshold(image, x, y, w, h)
    if direction is not "":
        cv2.imwrite("videocapture.jpg", image)
        if future is None:
            future = executor.submit(getAnnotations, "videocapture.jpg")
            future.add_done_callback(processAsyncGesture)
    if retGesture is not "":
        retDirection = retGesture
        if retGesture is "none":
            setBox(x, y, w, h)
        retGesture = ""
    if direction is "":
        retDirection = "none"
    drawDebugUI(image, x, y, w, h)
    return retDirection