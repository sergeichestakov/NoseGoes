import io
import os
import google.cloud.vision

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./assets/nosegoes.json"

vision_client = google.cloud.vision.ImageAnnotatorClient()

#Iterates through GCP response and selects the largest face by area
def getBiggestFace(faces):
    biggestFace = None
    bigArea = 0
    #Search for correct face
    for face in faces:
        box = face.bounding_poly.vertices
        area = (box[2].x - box[0].x) * (box[2].y - box[0].y)
        if area > bigArea:
            bigArea = area
            biggestFace = face

    return biggestFace

#returns the pan angle and tilt angle of the largest face or (0,0) if there is none
def getAnnotations(image):
    with io.open(image, "rb") as upload_file:
        content = upload_file.read()
    googleImage = google.cloud.vision.types.Image(content=content)
    response = vision_client.face_detection(image=googleImage)
    faces = response.face_annotations

    bestFace = getBiggestFace(faces)
    if bestFace is None:
        return (0, 0)

    pan_angle = bestFace.pan_angle #side to side
    tilt_angle = bestFace.tilt_angle #up and down

    return (pan_angle, tilt_angle)
