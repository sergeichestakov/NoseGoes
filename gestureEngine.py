import cv2
from collections import deque

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

def drawDebugUI(image, x, y, w, h):
    cv2.circle(image, center=(x, y), radius=2, color=(255,0,0))
    cv2.rectangle(image, (x - w / 2, y - h / 2), (h + w / 2, y + h / 2), color=(0,255,0), thickness=2)

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

def updateGesture(image, face):
    # face format is [topLeft, topRight, bottomRight, bottomLeft]
    # each face is a Vertex with properties x and y

    center = ((face[0].x + face[2].x) / 2, (face[0].y + face[2].y) / 2)
    width = face[2].x - face[0].x
    height = face[2].y - face[0].y
    (x, y, w, h) = updateSmoothers(center, width, height)
    drawDebugUI(image, x, y, w, h)
