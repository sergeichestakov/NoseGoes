import cv2
faceCascade = cv2.CascadeClassifier("./assets/faceCascade.xml")
class Vertex:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

def expand(face):
    x = face[0]
    y = face[1]
    w = face[2]
    h = face[3]
    topLeft = Vertex(x, y)
    topRight = Vertex(x + w, y)
    bottomLeft = Vertex(x, y + h)
    bottomRight = Vertex(x + w, y + h)
    return [topLeft, topRight, bottomRight, bottomLeft] #google syntax

def faceDetect(imageData):
    gray = cv2.cvtColor(imageData, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=4, minSize=(40, 40))
    biggest = [0, 0, 0, 0]
    for face in faces:
        if face[2] * face[3] > biggest[2] * biggest[3]:
            biggest = face
    ret = [expand(biggest)]
    return ret[0]
